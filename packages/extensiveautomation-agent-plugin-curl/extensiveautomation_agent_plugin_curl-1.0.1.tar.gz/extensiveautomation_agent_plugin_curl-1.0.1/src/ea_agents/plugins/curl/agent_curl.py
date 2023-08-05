#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------
# Copyright (c) 2010-2020 Denis Machard
# This file is part of the extensive automation project
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA
# -------------------------------------------------------------------


"""Curl agent"""

from ea_agents import agent as GenericTool
from ea_agents.libs import settings as Settings

import sys
import threading
import subprocess
import uuid
import os
import logging

def initialize (*args, **kwargs):
    """Wrapper to initialize agent"""
    return Curl(*args, **kwargs)
  
class Curl(GenericTool.Tool):
    """
    Curl agent class
    """
    def __init__(self, controllerIp, controllerPort, toolName, 
                       toolDesc, defaultTool, supportProxy=0,
                       proxyIp=None, proxyPort=None, sslSupport=True):
        """class agent"""
        GenericTool.Tool.__init__(self, controllerIp, controllerPort, 
                                    toolName, toolDesc, defaultTool, 
                                    supportProxy=supportProxy, proxyIp=proxyIp, 
                                    proxyPort=proxyPort, sslSupport=sslSupport)
        self.__mutex__ = threading.RLock()
        if sys.platform not in [ "win32", "linux2" ] :
            raise Exception( 'System %s not supported'   % sys.platform  )     

    def initAfterRegistration(self):
        """Called on successful registration"""
        pass

    def onAgentNotify(self, client, tid, request):
        """on agent notify"""
        self.__mutex__.acquire()
        if request['uuid'] in self.context():
            if request['source-adapter'] in self.context()[request['uuid']]:
                a = self.context()[request['uuid']][request['source-adapter']]
                a.putItem( lambda: self.execAction(request) )
            else:
                logging.error("Adapter context does not exists TestUuid=%s AdapterId=%s" % (request['uuid'],
                                                                                         request['source-adapter'] ) )
        else:
            logging.error("Test context does not exits TestUuid=%s" % request['uuid'])
        self.__mutex__.release()
        
    def execAction(self, request):
        """
        on execute action
        """
        logging.debug( "<< Begin curl command"  )

        if sys.platform == "win32" :
            infile = "%s\\req_%s" % (self.getTemp(), uuid.uuid4() )
            outfile = "%s\\rsp_%s" % (self.getTemp(), uuid.uuid4() )
        if sys.platform == "linux2":
            infile = "%s/req_%s" % (self.getTemp(), uuid.uuid4() )
            outfile = "%s/rsp_%s" % (self.getTemp(), uuid.uuid4() )
            
        __options = ' ' 
        try:
            if request["data"]["cmd"] == "send-http":
                if "host" not in request["data"] and "timeout-connect" not in request["data"] \
                    and "timeout-max" not in request["data"] :
                    logging.error("options missing in request")
                else:
                    logging.debug( "<< Curl Host=%s" % request["data"]["host"]  )

                    __options += ' --user-agent %s' % Settings.get('Common', 'acronym-server')
                    
                    if "method" in request["data"]:
                        __options += " -X %s" % request["data"]["method"]
                    if "headers" in request["data"]:
                        for hdr in request["data"]["headers"].splitlines():
                            __options += ' -H "%s"' % hdr
                    if "proxy-host" in request["data"]:
                        __options += ' -x %s' % request["data"]["proxy-host"]
                    if "more" in request["data"]:
                        __options += " %s" % request["data"]["more"]
                        
                    __options += ' -w '
                    __options += '"\\n%{time_connect},%{time_total},%{speed_download},'
                    __options += '%{time_appconnect}, %{time_namelookup},'
                    __options += '%{http_code},%{size_download},'
                    __options += '%{url_effective},%{remote_ip}\\n"'
                    
                    __options += ' --connect-timeout %s' % request["data"]["timeout-connect"]
                    __options += ' --max-time %s ' % int(request["data"]["timeout-max"])
                    
                    __options += ' -v %s -s ' % request["data"]["host"]
                    if "body" in request["data"]:
                        with open(infile, "w") as f:
                            f.write(request["data"]["body"])
                        __options += ' --data-binary "@%s"'  % infile
                    
                    __options += ' -o "%s"' % outfile
                    logging.debug("curl options: %s" % __options )
        except Exception as e:
            logging.error("Unable to init curl command - %s" % e)
     
        # windows support
        if sys.platform == "win32" :
            __curlexe = r'"%s\Plugins\curl\bin\curl.exe"' % (Settings.getDirExec() )
            __curlexe += __options
            logging.debug("curl command: %s" % __curlexe )
            try:
                command_process = subprocess.Popen(__curlexe, shell=True, 
                                                    stdin=subprocess.PIPE, 
                                                    stdout=subprocess.PIPE,
                                                    stderr=subprocess.STDOUT, 
                                                    bufsize=0 )
            except Exception as e:
                logging.error("Unable to start curl on windows- %s" % e)
                
        # linux support
        if sys.platform == "linux2":
            __curlexe = 'curl '
            __curlexe += __options
            logging.debug("curl command: %s" % __curlexe )
            try:
                command_process = subprocess.Popen(__curlexe, shell=True, 
                                                    stdin=subprocess.PIPE, 
                                                    stdout=subprocess.PIPE,
                                                    stderr=subprocess.STDOUT, 
                                                    bufsize=0 )
            except Exception as e:
                logging.error("Unable to start curl on linux - %s" % e)

        # read the response
        conn_info = []
        req_out = []
        rsp_in = []
        
        try:
        
            while True:
                line = command_process.stdout.readline()
                if sys.version_info < (3,):
                    line = line.decode('latin-1').encode("utf-8")
                if line != b'':
                    if line.startswith(b"*"):
                        conn_info.append(line[1:].strip())
                    elif line.startswith(b"> "):
                        req_out.append(line[2:].strip())
                    elif line.startswith(b"< "):
                        if not len(rsp_in):
                            # notify the server with the request
                            event = { "response-type": "http-request", 
                                       "headers": b"\n".join(req_out),
                                      "cmd": request["data"]["cmd"] }
                            if "body" in request["data"]:
                                event["body"] = request["data"]["body"]  
                            self.sendNotify( request=request, data=event )
                            
                        rsp_in.append(line[2:].strip())	
                    elif line.startswith(b"{"):
                        continue
                    elif line.startswith(b"}"):
                        continue
                    else:
                        conn_info.append(line.strip())
                else:
                    break

            
            
            rsp_body=None
            if len(rsp_in):
                with open(outfile, "rb") as f:
                    rsp_body = f.read()
                    
                # notify the server with the response
                event = { "response-type": "http-response", 
                          "headers": b"\n".join(rsp_in),
                          "cmd": request["data"]["cmd"] }
                if rsp_body is not None:
                    event["body"] = rsp_body 
                self.sendNotify( request=request, data=event )
            
            event = { "response-type": "http-info", 
                      "debug": b"\n".join(conn_info),
                      "cmd": request["data"]["cmd"] }
            self.sendNotify( request=request, data=event )
        except Exception as e:
            logging.error("Unable to parse curl output - %s" % e)
 
        # remove temps files
        try:
            os.remove(infile)
        except:
            pass
        try:
            os.remove(outfile)
        except:
            pass
            
        logging.debug( "<< Curl terminated")
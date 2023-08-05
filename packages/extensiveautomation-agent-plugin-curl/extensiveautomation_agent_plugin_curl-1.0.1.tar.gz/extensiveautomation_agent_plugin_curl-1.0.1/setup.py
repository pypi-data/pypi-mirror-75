#!/usr/bin/python

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

import setuptools

VERSION="1.0.1"

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

KEYWORDS = ('extensiveautomation agent plugin curl')

setuptools.setup(
    name="extensiveautomation_agent_plugin_curl",
    version=VERSION,
    author="Denis MACHARD",
    author_email="d.machard@gmail.com",
    description="Curl plugin for extensiveautomation agent",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://www.extensiveautomation.org/",
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
    include_package_data=True,
    platforms='any',
    keywords=KEYWORDS,
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Acceptance"
    ],
    install_requires=[
        "extensiveautomation_agent"
    ]
)

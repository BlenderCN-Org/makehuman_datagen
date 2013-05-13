#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Joel Palmius

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

This module dumps important debug information to a text file in the user's home directory
"""

import sys
import os
import re
import platform
import string
if sys.platform == 'win32':
    import _winreg
import log

class DebugDump(object):

    """
    A class that dumps relevant information to a text file in the user's home directory
    """
    def __init__(self):
        self.debugpath = None

    def open(self):
        if self.debugpath is None:
            self.home = os.path.expanduser('~')
            self.debugpath = self.home
            if sys.platform == 'win32':
                self.debugpath = os.path.join(os.environ['MYDOCUMENTS'],'makehuman')

            if sys.platform == 'linux2':
                self.debugpath = os.path.join(self.debugpath,"makehuman")

            if sys.platform.startswith("darwin"):
                self.debugpath = os.path.join(self.debugpath,"Documents")
                self.debugpath = os.path.join(self.debugpath,"MakeHuman")

            if not os.path.exists(self.debugpath):
                os.makedirs(self.debugpath)

            self.debugpath = os.path.join(self.debugpath, "makehuman-debug.txt")
            self.debug = open(self.debugpath, "w")
        else:
            self.debug = open(self.debugpath, "a")

    def write(self, msg, *args):
        self.debug.write((msg % args) + "\n")
        log.debug(msg, *args)

    def close(self):
        self.debug.close()
        self.debug = None

    def reset(self):
        self.open()

        self.write("SVN REVISION: %s [%s]", os.environ['SVNREVISION'], os.environ['SVNREVISION_SOURCE'])
        self.write("HOME LOCATION: %s", self.home)
        version = re.sub(r"[\r\n]"," ", sys.version)
        self.write("SYS.VERSION: %s", version)
        self.write("SYS.PLATFORM: %s", sys.platform)
        self.write("PLATFORM.MACHINE: %s", platform.machine())
        self.write("PLATFORM.PROCESSOR: %s", platform.processor())
        self.write("PLATFORM.UNAME.RELEASE: %s", platform.uname()[2])

        if sys.platform == 'linux2':
            self.write("PLATFORM.LINUX_DISTRIBUTION: %s", string.join(platform.linux_distribution()," "))
            
        if sys.platform.startswith("darwin"):
            self.write("PLATFORM.MAC_VER: %s", platform.mac_ver()[0])
            
        if sys.platform == 'win32':
            self.write("PLATFORM.WIN32_VER: %s", string.join(platform.win32_ver()," "))

        import numpy
        self.write("NUMPY.VERSION: %s", numpy.__version__)

        from qtui import getQtVersionString
        self.write("PYQT.VERSION: %s", getQtVersionString())
        self.close()

    def appendGL(self):
        import OpenGL
        self.open()
        self.write("PYOPENGL.VERSION: %s", OpenGL.__version__)
        self.close()

    def appendMessage(self,message):
        self.open()
        self.write(message)
        self.close()

dump = DebugDump()

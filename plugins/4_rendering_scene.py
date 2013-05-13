#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           ...none yet

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

Scene library.
"""

import gui
import gui3d

import os
import scene

class SceneLibraryTaskView(gui3d.TaskView):
    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Scene')
        self.scene = scene.Scene()

                
def load(app):
    category = app.getCategory('Rendering')
    taskview = SceneLibraryTaskView(category)
    taskview.sortOrder = 1.0
    category.addTask(taskview)

def unload(app):
    pass

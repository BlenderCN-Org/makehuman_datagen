#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Manuel Bastioni, Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

import mh
import gui3d
import geometry3d
import gui
import log

import numpy as np
np.set_printoptions(precision=6, suppress=True)

class CensorTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Censor')
        
        self.mouseBox = self.addLeftWidget(gui.GroupBox('Censor'))
        self.enableCensor = self.mouseBox.addWidget(gui.CheckBox("Enable", gui3d.app.settings.get('censor', False)))
        
        human = gui3d.app.selectedHuman

        self.breastVertices = human.mesh.getVerticesForGroups(['l-torso-nipple', 'r-torso-nipple'])
        mesh = geometry3d.RectangleMesh(100, 100)
        self.breastCensorship = gui3d.app.addObject(gui3d.Object([0, 0, 9], mesh))
        mesh.setColor([0, 0, 0, 255])
        mesh.setPickable(False)
        mesh.setShadeless(True)
        mesh.setDepthless(True)
        mesh.priority = 80

        self.genitalVertices = human.mesh.getVerticesForGroups(['pelvis-genital-area'])
        mesh = geometry3d.RectangleMesh(100, 100)
        self.genitalCensorship = gui3d.app.addObject(gui3d.Object([0, 0, 9], mesh))
        mesh.setColor([0, 0, 0, 255])
        mesh.setPickable(False)
        mesh.setShadeless(True)
        mesh.setDepthless(True)
        mesh.priority = 80
        
        if gui3d.app.settings.get('censor', False):
            self.updateCensor()
        else:
            self.breastCensorship.hide()
            self.genitalCensorship.hide()
            
        @self.enableCensor.mhEvent
        def onClicked(event):
            gui3d.app.settings['censor'] = self.enableCensor.selected
            if self.enableCensor.selected:
                self.updateCensor()
                self.breastCensorship.show()
                self.genitalCensorship.show()
            else:
                self.breastCensorship.hide()
                self.genitalCensorship.hide()
        
    def calcProjectedBBox(self, vertices):
    
        human = gui3d.app.selectedHuman
        box = human.mesh.calcBBox(vertices)
        box = [[box[(i>>j)&1,j]
                for j in xrange(3)]
               for i in xrange(8)]
        
        for i, v in enumerate(box):
            v = gui3d.app.modelCamera.convertToScreen(v[0], v[1], v[2], human.mesh.object3d)
            v = gui3d.app.guiCamera.convertToWorld3D(v[0], v[1], v[2])
            box[i] = v
            
        return min([v[0] for v in box]), min([v[1] for v in box]), max([v[0] for v in box]), max([v[1] for v in box])
        
    def updateCensor(self):
        if not gui3d.app.settings.get('censor', False):
            return

        x1, y1, x2, y2 = self.calcProjectedBBox(self.breastVertices)
        self.breastCensorship.setPosition([x1, y1, 9])
        self.breastCensorship.mesh.resize(x2 - x1, y2 - y1)
        
        x1, y1, x2, y2 = self.calcProjectedBBox(self.genitalVertices)
        self.genitalCensorship.setPosition([x1, y1, 9])
        self.genitalCensorship.mesh.resize(x2 - x1, y2 - y1)
    
    def onShow(self, event):
        
        gui3d.TaskView.onShow(self, event)
        self.enableCensor.setFocus()
    
    def onHide(self, event):

        gui3d.TaskView.onHide(self, event)
        gui3d.app.saveSettings()
        
    def onResized(self, event):
        
        self.updateCensor()
        
    def onHumanChanged(self, event):
    
        self.updateCensor()
        
    def onHumanChanging(self, event):
    
        self.updateCensor()
            
    def onHumanTranslated(self, event):
    
        self.updateCensor()
            
    def onHumanRotated(self, event):
    
        self.updateCensor()

    def onHumanShown(self, event):
    
        if gui3d.app.settings.get('censor', False):
            self.breastCensorship.show();
            self.genitalCensorship.show();
            
    def onHumanHidden(self, event):
    
        if gui3d.app.settings.get('censor', False):
            self.breastCensorship.hide();
            self.genitalCensorship.hide();

    def onCameraChanged(self, event):

        self.updateCensor()

def load(app):
    return  # Disabled because currently not working
    category = app.getCategory('Settings')
    taskview = category.addTask(CensorTaskView(category))

def unload(app):
    pass

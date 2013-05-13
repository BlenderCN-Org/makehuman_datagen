#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

import os
import numpy as np
import gui3d
import module3d
import mh
import gui
import log

import armature as amtpkg
import transformations as tm
import warpmodifier


#
#   Dynamic buttons
#

class PoseRadioButton(gui.RadioButton):
    def __init__(self, group, label, selected, view):
        super(PoseRadioButton, self).__init__(group, label, selected)
        self.view = view
        self.name = label
        self.file = os.path.join(mh.getPath(''), "data", "poses", label+".bvh")
        
        @self.mhEvent
        def onClicked(event):
            self.view.armature.readBvhFile(self.file, gui3d.app.selectedHuman)
            self.view.updateAll()
            self.view.poseBox.hide()


class BoneRadioButton(gui.RadioButton):
    def __init__(self, group, label, selected, view):
        super(BoneRadioButton, self).__init__(group, label, selected)
        self.view = view
        self.name = label
        
        @self.mhEvent
        def onClicked(event):
            bone = self.view.armature.bones[self.name]
            if self.view.activeBone:
                self.view.armatureObject.setColor(self.view.activeBone, [255, 255, 255, 255])
            self.view.armatureObject.setColor(bone, [0, 255, 0, 255])
            self.view.activeBone = bone
            self.view.status.setText(bone.name)
            self.view.updateSliders(bone)


class LayerCheckBox(gui.CheckBox):
    def __init__(self, label, selected, view):
        super(LayerCheckBox, self).__init__(label, selected)
        self.view = view
        self.name = label
        
        @self.mhEvent
        def onClicked(event):
            self.view.updateLayers()

#
#   Pose Window
#

class PoseArmatureTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Pose tuning')            

        self.zone = ""
        self.rigtype = None
        self.armature = None
        self.armatureObject = None
        self.objects = []
        self.activeBone = None
        self.poseModifier = None
        
        cubeLayer = CLayerObject("Cube", 'CUBE')
        cubeLayer.buildCube((-8,8,0), 1.0)
        cubeLayer.finishBuild((0,0,0))
        self.cube = cubeLayer.object
        self.cube.hide()

        # Main box
        self.mainBox = self.addLeftWidget(gui.GroupBox('Rotation'))
        self.eulerBox = self.addLeftWidget(gui.GroupBox('Euler'))
        self.quatBox = self.addLeftWidget(gui.GroupBox('Quaternion'))

        self.QWslider = self.quatBox.addWidget(gui.Slider(value = 1000.0, min = -1000.0, max = 1000.0, label = "W: %d"))
        self.QXslider = self.quatBox.addWidget(gui.Slider(value = 0.0, min = -1000.0, max = 1000.0, label = "X: %d"))
        self.QYslider = self.quatBox.addWidget(gui.Slider(value = 0.0, min = -1000.0, max = 1000.0, label = "Y: %d"))
        self.QZslider = self.quatBox.addWidget(gui.Slider(value = 0.0, min = -1000.0, max = 1000.0, label = "Z: %d"))

        self.EXslider = self.eulerBox.addWidget(gui.Slider(value = 0.0, min = -180, max = 180, label = "X: %d"))
        self.EYslider = self.eulerBox.addWidget(gui.Slider(value = 0.0, min = -180, max = 180, label = "Y: %d"))
        self.EZslider = self.eulerBox.addWidget(gui.Slider(value = 0.0, min = -180, max = 180, label = "Z: %d"))

        self.rotSlider = self.mainBox.addWidget(gui.Slider(value = 0.0, min = -180, max = 180, label = "Rotation: %d"))
        self.rotWorld = self.mainBox.addWidget(gui.CheckBox("World Rotation", False))
        rots = []
        self.rotX = self.mainBox.addWidget(gui.RadioButton(rots, "X", True)) 
        self.rotY = self.mainBox.addWidget(gui.RadioButton(rots, "Y", False)) 
        self.rotZ = self.mainBox.addWidget(gui.RadioButton(rots, "Z", False)) 
        
        self.showMesh = self.mainBox.addWidget(gui.CheckBox("Show Mesh", True))
        self.showRig = self.mainBox.addWidget(gui.CheckBox("Show Rig", False))
        self.restPosition = self.mainBox.addWidget(gui.CheckBox("Rest Position", False))
        
        #self.updateButton = self.mainBox.addWidget(gui.Button("Update"))
        self.reloadCharacterButton = self.mainBox.addWidget(gui.Button("Reload Character"))
        self.zeroBoneButton = self.mainBox.addWidget(gui.Button("Zero Bone"))
        self.zeroAllButton = self.mainBox.addWidget(gui.Button("Zero All"))
        self.poseButton = self.mainBox.addWidget(gui.Button("Pose"))
        self.testButton = self.mainBox.addWidget(gui.Button("Test bones"))
        # self.mainBox.hide()
        # self.quatBox.hide()
        # self.eulerBox.hide()

        # Rig select box        
        self.rigBox = self.addLeftWidget(gui.GroupBox('Rig'))

        prisms = []
        self.prismButtons = {}
        first = True
        for type in ['Prism', 'Box', 'Line']:
            self.prismButtons[type] = self.rigBox.addWidget(gui.RadioButton(prisms, type, first))
            first = False

        self.selectRigButton = self.rigBox.addWidget(gui.Button("SelectRig"))

        rigs = []
        self.rigButtons = {}
        self.rigButtons["mhx"] = self.rigBox.addWidget(gui.RadioButton(rigs, "Mhx", False))
        path = "data/rigs"
        if not os.path.exists(path):
            log.notice("Did not find directory %s", path)
        else:
            buttons = []
            for name in ["game", "simple", "rigid"]:
            #for fname in os.listdir(path):
            #    (name, ext) = os.path.splitext(fname)
            #    if ext == ".rig":
                    self.rigButtons[name] = self.rigBox.addWidget(gui.RadioButton(rigs, name.capitalize(), False)) 
        self.rigBox.show()                    
        
        # Bone select box        
        self.boneBox = self.addRightWidget(gui.GroupBox('Bone'))
        self.boneButtons = {}
        self.boneBox.hide()
        
        # Pose select box        
        self.poseBox = self.addRightWidget(gui.GroupBox('Pose'))
        self.poseButtons = {}
        self.poseBox.hide()
        
        # Layer select box
        self.layerBox = self.addRightWidget(gui.GroupBox('Layers'))
        self.layerButtons = {}
        self.layerBox.hide()
        
         
        @self.selectRigButton.mhEvent
        def onClicked(event):     
            for name,button in self.prismButtons.items():
                if button.selected:
                    prismType = name
            for name,button in self.rigButtons.items():
                if button.selected:
                    rigtype = name
            if rigtype:
                self.selectRig(prismType, rigtype)                   
            
        @self.testButton.mhEvent
        def onClicked(event):
            listBones = doTest1(self.armature.bones)
            self.updateAll()
            doTest2(listBones)
                
        @self.poseButton.mhEvent
        def onClicked(event):
            if not self.poseButtons:
                radio = []
                self.poseButtons = {}
                path = os.path.join(mh.getPath(''), "data", "poses")
                if not os.path.exists(path):
                    os.makedirs(path)
                for file in os.listdir(path):
                    (pose, ext) = os.path.splitext(file)
                    if ext.lower() == ".bvh":
                        button = PoseRadioButton(radio, pose, False, self)
                        self.poseButtons[pose] = self.poseBox.addWidget(button)
            self.poseBox.show()
                       
        @self.showMesh.mhEvent
        def onClicked(event):
            self.updateAll()                        

        @self.showMesh.mhEvent
        def onClicked(event):
            self.updateAll()                        

        @self.showRig.mhEvent
        def onClicked(event):
            self.updateAll()                        

        @self.restPosition.mhEvent
        def onClicked(event):
            self.updateAll()                        

        @self.zeroBoneButton.mhEvent
        def onClicked(event):
            bone = self.getSelectedBone()
            bone.zeroTransformation()
            self.zeroSliders()
            self.updateAll()

        @self.zeroAllButton.mhEvent
        def onClicked(event):
            self.zeroSliders()
            for bone in self.armature.controls:
                bone.zeroTransformation()
            self.updateAll()

        @self.reloadCharacterButton.mhEvent
        def onClicked(event):
            self.zeroSliders()
            human = gui3d.app.selectedHuman
            amt = self.getArmature()
            self.armatureObject = None
            if amt:
                #amt.hide()
                gui3d.app.removeObject(amt)
            if self.armature:
                self.armature.rebuild()
            else:
                self.armature = amtpkg.rigdefs.createPoseRig(human, self.armature.rigtype)
            self.updateAll()

        @self.rotSlider.mhEvent
        def onChange(value):
            bone = self.getSelectedBone()
            if self.rotX.selected:
                axis = 0
            elif self.rotY.selected:
                axis = 1
            elif self.rotZ.selected:
                axis = 2
            bone.rotate(value, axis, self.rotWorld.selected)
            self.updateSliders(bone)
                                                       
        @self.QXslider.mhEvent
        def onChange(value):
            bone = self.getSelectedBone()
            bone.setRotationIndex(1, value, True)
            self.updateSliders(bone)
                
        @self.QYslider.mhEvent
        def onChange(value):
            bone = self.getSelectedBone()
            bone.setRotationIndex(2, value, True)
            self.updateSliders(bone)
                
        @self.QZslider.mhEvent
        def onChange(value):
            bone = self.getSelectedBone()
            bone.setRotationIndex(3, value, True)
            self.updateSliders(bone)
                
        @self.EXslider.mhEvent
        def onChange(value):
            bone = self.getSelectedBone()
            bone.setRotationIndex(1, value, False)
            self.updateSliders(bone)
                
        @self.EYslider.mhEvent
        def onChange(value):
            bone = self.getSelectedBone()
            bone.setRotationIndex(2, value, False)
            self.updateSliders(bone)
        
        @self.EZslider.mhEvent
        def onChange(value):
            bone = self.getSelectedBone()
            bone.setRotationIndex(3, value, False)
            self.updateSliders(bone)

        @self.cube.mhEvent
        def onMouseEntered(event):            
            gui3d.TaskView.onMouseEntered(self, event)
            mh.redraw()

        @self.cube.mhEvent
        def onMouseDragged(event):        
            gui3d.app.selectedHuman.show()
            self.getArmature().hide()
        
            gui3d.TaskView.onMouseDragged(self, event)

            if not self.showMesh.selected:
                gui3d.app.selectedHuman.hide()
            if self.showRig.selected:
                self.getArmature().show()
        
        @self.cube.mhEvent
        def onMouseWheel(event):        
            gui3d.app.selectedHuman.show()
            self.getArmature().hide()
        
            gui3d.TaskView.onMouseWheel(self, event)
            
            if not self.showMesh.selected:
                gui3d.app.selectedHuman.hide()
            if self.showRig.selected:
                self.getArmature().show()
        
    def selectRig(self, prismType, rigtype):     
        self.prismType = prismType
        self.rigtype = rigtype
        if self.armature:
            self.armature.rebuild()
        else:
            self.armature = amtpkg.rigdefs.createPoseRig(gui3d.app.selectedHuman, self.rigtype)
        self.armatureObject = None
        
        self.mainBox.show()
        self.quatBox.show()
        self.eulerBox.show()
        
        first = True
        radio = []
        self.boneButtons = {}
        for bone in self.armature.controls:
            log.debug("bone: %s", bone.name)
            button = BoneRadioButton(radio, bone.name, first, self)
            self.boneButtons[bone.name] = self.boneBox.addWidget(button)
            first = False    
            
        self.boneBox.show()
        
        if self.rigtype == "mhx":
            self.layerButtons = []
            for bit,lname in amtpkg.rigdefs.LayerNames:
                check = LayerCheckBox(lname, self.armature.visible & bit, self)
                self.layerButtons.append(self.layerBox.addWidget(check))
            self.layerBox.show()
        else:
            self.layerBox.hide()
            
        self.rigBox.hide()
        self.cube.show()
        self.updateAll()
 
 
    def updateSliders(self, bone):
        angles = bone.getRotation()
        self.setSliders(angles)
        self.updateAll()
        mh.redraw()
    
    def zeroSliders(self):
        self.setSliders((1000,0,0,0,0,0,0))
        
    def setSliders(self, angles):
        qw,qx,qy,qz,ax,ay,az = angles
        self.rotSlider.setValue(0)
        self.QWslider.setValue(qw)
        self.QXslider.setValue(qx)
        self.QYslider.setValue(qy)
        self.QZslider.setValue(qz)
        self.EXslider.setValue(ax)
        self.EYslider.setValue(ay)
        self.EZslider.setValue(az)            
                        

    def getSelectedBone(self):
        for (name,button) in self.boneButtons.items():
            if button.selected:
                #print "Bone", name, "selected"
                return self.armature.bones[name]
        log.notice("BUG: No bone selected")
        return None

   
    def updateBones(self):
        bone = self.getSelectedBone()
        self.updateSliders(bone)

   
    def updateLayers(self):
        if not self.layerButtons:
            return
        vis = 0
        for n,button in enumerate(self.layerButtons):
            if button.selected:
                bit,lname = amtpkg.rigdefs.LayerNames[n]
                vis |= bit
        self.armature.visible = vis
        self.updateAll()                


    def onShow(self, event):
        # if not self.rigtype:
        #     self.selectRig("Prism", "rigid")       
        if self.armature:
            self.cube.show()
        self.activeBone = None
        #self.status.setText("")
        gui3d.TaskView.onShow(self, event)
        
     
    def onHide(self, event):
        self.cube.hide()
        self.activeBone = None
        #self.status.setText("")
        gui3d.TaskView.onHide(self, event)
        
     
    def updateAll(self):    
        if not self.armature:
            return
        self.armature.restPosition = self.restPosition.selected
        human = gui3d.app.selectedHuman
        self.armature.update()
        amt = self.getArmature()

        if self.showMesh.selected:
            human.show()
        else:
            human.hide()
        #human.storeMesh()
            
        if not amt:
            pass
        elif self.showRig.selected:
            amt.show()
        else:
            amt.hide()        
        
        bone = self.getSelectedBone()

        
    def onHide(self, event):

        gui3d.TaskView.onHide(self, event)

        human = gui3d.app.selectedHuman
        human.show()
        if self.armature:
            amt = self.getArmature()
            if amt:
                amt.hide()
        #human.restoreMesh()
        human.meshData.calcNormals()
        human.meshData.update()
        
    
    def getArmature(self):
        
        human = gui3d.app.selectedHuman
        #self.armature.update()
        
        if not self.armatureObject:            
            self.armatureObject = CArmatureObject(self.armature, self)
            self.armatureObject.build(human)
            self.armatureObject.setRotation(human.getRotation())        
        else:            
            self.armatureObject.update()
            self.armatureObject.setPosition(human.getPosition())             
            self.armatureObject.setRotation(human.getRotation())        
        return self.armatureObject
        
     
    def loadHandler(self, human, values):
        log.debug("loadHandler: %s", values)
        filepath = values[1]
        self.loadBvhFile(filepath)
       

    def saveHandler(self, human, file):
        return

     
        
#
#   Armature Object
#

class CArmatureObject:
    def __init__(self, amtpkg, view):
        self.armature = amtpkg
        self.view = view
        self.layers = {}
        for n in range(self.armature.last):
            self.layers[n] = None


    def getLayers(self, mask):
        layers = []
        bit = 1
        for n in range(self.armature.last):
            if bit & mask:
                layers.append(n)
            bit <<= 1
        return layers
        
        
    def setColor(self, bone, value):
        log.debug("setColor: %s %s", bone.name, value)
        for layer in self.layers.values():
            if layer:
                layer.setColor(bone, value)
        
        
    def build(self, human):
        for bone in self.armature.boneList:
            for n in self.getLayers(bone.layers):
                if not self.layers[n]:
                    self.layers[n] = CLayerObject('Layer%2d' % n, self.view.prismType)
                self.layers[n].buildBoneMesh(bone)
            
        for layer in self.layers.values():
            if layer:
                ob = layer.finishBuild(human.getPosition())            
                    
                    
    def update(self):
        change = False
        for bone in self.armature.boneList:
            for n in self.getLayers(bone.layers & self.armature.visible):
                layer = self.layers[n]
                change |= layer.updateBoneMesh(bone)
            
        for n in self.getLayers(self.armature.visible):
            layer = self.layers[n]
            if layer:
                layer.update(change)
                    
                    
    def setRotation(self, rot):
        for layer in self.layers.values():
            if layer:
                layer.object.setRotation(rot)
                        

    def setPosition(self, pos):
        for layer in self.layers.values():
            if layer:
                layer.object.setPosition(pos)   
                       

    def show(self): 
        bit = 1
        for n in range(self.armature.last):
            layer = self.layers[n]
            if layer:
                if bit & self.armature.visible:
                    layer.object.show()
                else:
                    layer.object.hide()
            bit <<= 1

                        
    def hide(self): 
        for layer in self.layers.values():
            if layer:
                layer.object.hide()    


#
#   Visual representation of amtpkg
#

class CLayerObject:
    def __init__(self, name, prismType):
        self.mesh = None
        self.object = None
        self.prisms = {}
        self.prismType = prismType
        self.nVerts = 0
        self.coords = None
        self._data = []

        self.mesh = module3d.Object3D(name)

        """
        dummy = module3d.Object3D('Dummy%2d' % self.index)
         gui3d.app.addObject(gui3d.Object([0.0, 0.0, 0.0], dummy))  
        
        @self.object.mhEvent
        def onMouseEntered(self, event):
            print "Emtered", event

        @self.object.mhEvent
        def onMouseDown(self, event):
            print "Dpwm", event

        @self.object.mhEvent
        def onMouseDragged(self, event):
            print "Dragged", event

        @self.object.mhEvent
        def onMouseMoved(self, event):
            print "Moved", event

        @self.object.mhEvent
        def onMouseUp(self, event):
            print "Up", event
        """

    
    def finishBuild(self, location):
        coord = []
        faces = []
        group = []
        for name, p, f in self._data:
            fg = self.mesh.createFaceGroup(name)
            coord.append(p)
            faces.append(f)
            group.append(np.zeros(len(f), dtype=np.uint16) + fg.idx)
        del self._data

        self.coords = np.vstack(coord)
        log.debug("finishBuild: %d %d", len(coord), len(self.coords))
        self.mesh.setCoords(self.coords)
        self.mesh.setUVs(np.zeros((1, 2), dtype=np.float32))
        self.mesh.setFaces(np.vstack(faces), None, np.hstack(group))

        self.mesh.setCameraProjection(0)
        self.mesh.setShadeless(0)
        self.mesh.setSolid(0)
        self.mesh.calcNormals()
        self.mesh.updateIndexBuffer()
        self.mesh.priority = 30

        self.object = gui3d.app.addObject( gui3d.Object(location, self.mesh) )  
        
        for fg in self.mesh.faceGroups:
            if not fg.parent:
                log.debug("finishBuild: %s %s", fg, fg.parent)
                halt
        return self.object

    
    def setColor(self, bone, value):
        for fg in self.mesh.faceGroups:
            if fg.name == bone.name:
                fg.setColor(value)
                return
                
    
    def buildBoneMesh(self, bone):    
        points, faces = bone.prismPoints(self.prismType)
        p,n = self.addPrism(bone.name, points, faces)
        self.prisms[bone.name] = (p, self.nVerts)
        self.nVerts += n
        
        
    def buildCube(self, location, scale):
        offsets = amtpkg.rigdefs.CBone.PrismVectors['Cube']
        points = []
        for dx in offsets:
            points.append( location + scale*dx[:3] )
        faces = amtpkg.rigdefs.CBone.PrismFaces['Box']
        p,n = self.addPrism('Cube', points, faces)
        self.prisms['Cube'] = (p, 0)
        self.nVerts = n       
            
            
    def update(self, change):
        if 0 and change:
            log.message("Armature has changed")
            #gui3d.app.removeObject(self.armatureObject)
            self.armatureObject.hide()
            self.armatureObject = None
            self.mesh = None
            self.getArmature()
        else:
            self.mesh.setCoords(self.coords)
            self.mesh.calcNormals()
            self.mesh.update()

        
    def updateBoneMesh(self, bone):
        try:
            prism,index = self.prisms[bone.name]
        except KeyError:
            return True
        self.updatePrism(bone, index)
        return False


    def addPrism(self, name, points, faces):
        p = np.asarray(points, dtype=np.float32)
        f = np.asarray(faces, dtype=np.uint32)
        self._data.append((name, p, f + self.nVerts))
        return points[0], len(points)
            
       
    def updatePrism(self, bone, index):            
        points, faces = bone.prismPoints(self.prismType)
        for n,p in enumerate(points):
            self.coords[index+n] = p
            
            


#
#   Testing poses
#

thePoseBoneFile = os.path.expanduser("~/documents/makehuman/posebones.txt")
thePosesFile = os.path.expanduser("~/documents/makehuman/poses_mh.txt")
 
def doTest1(bones):            
    try:
        fp = open(thePoseBoneFile)
    except:
        log.warning("Did not find %s", thePoseBoneFile)
        return
    readBones = []
    setBones = []
    for line in fp:
        words = line.split()
        if len(words) == 0:
            continue
        elif len(words) == 1:
            bone = bones[words[0]]
            readBones.append((bone,[]))
        elif len(words) == 4:
            bone = bones[words[0]]   
            coords = (float(words[1]), float(words[2]), float(words[3]))
            setBones.append((bone, coords))
    fp.close()
    
    for bone, coords in setBones:        
        bone.setRotationIndex(1, coords[0], False)
        bone.setRotationIndex(2, coords[1], False)
        bone.setRotationIndex(3, coords[2], False)
        #bone.setRotation(coords)
        angles = bone.getRotation()
    return setBones+readBones
    

def doTest2(listBones):            
    fp = open(thePosesFile, "w")
    for bone,coords in listBones:
        fp.write("\n%s %.4f\n" % (bone.name, bone.roll)) 
        writeMat(fp, "Rest", bone.matrixRest)
        writeMat(fp, "Global", bone.matrixGlobal)
        pose = bone.getPoseFromGlobal()
        writeMat(fp, "Pose", pose)
        xyz = tm.euler_from_matrix(pose, axes='sxyz')
        fp.write("XYZ %.4g %.4g %.4g\n" % tuple(xyz))
        zyx = tm.euler_from_matrix(pose, axes='szyx')
        fp.write("ZYX %.4g %.4g %.4g\n" % tuple(zyx))
        #writeMat(fp, "Pose0", bone.matrixPose)
    fp.close()
    

def writeMat(fp, string, mat):
    fp.write("%s\n[" % string)
    for n in range(4):
        row = mat[n]
        fp.write( "( %.4f, %.4f, %.4f, %.4f)\n" % (row[0], row[1], row[2], row[3]) )
        

def printArray(array):
    log.debug("[")
    for row in array:
        log.debug(" %s", row)
    log.debug("]")

#
#   Loading
#

category = None
taskview = None

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements
def load(app):
    return
    
    category = app.getCategory('Pose/Animate')
    taskview = PoseArmatureTaskView(category)
    taskview.sortOrder = 1.9
    category.addTask(taskview)

    app.addLoadHandler('poses', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)
            
    @taskview.mhEvent
    def onMouseDown(event):
        part = app.getSelectedFaceGroup()
        log.debug("PoseArmatureTaskView.onMouseDown: %s", part.name)

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements

def unload(app):  
    pass

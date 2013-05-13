#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Jonas Hauquier, Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO

"""

__docformat__ = 'restructuredtext'

import os
import gui3d
import mh
import download
import gui
import filechooser as fc
import log
import subtextures

class Action(gui3d.Action):
    def __init__(self, name, human):
        super(Action, self).__init__(name)
        self.human = human

class SkinAction(Action):

    def __init__(self, human, before, after):
        super(SkinAction, self).__init__('Change skin texture', human)
        self.before = before
        self.after = after

    def do(self):
        self.human.setTexture(self.after)
        self.human.mesh.setShadeless(False)
        return True

    def undo(self):
        self.human.setTexture(self.before)
        return True


class HairAction(Action):

    def __init__(self, human, before, after):
        super(HairAction, self).__init__('Change hair texture', human)
        self.before = before
        self.after = after

    def do(self):
        if self.human.hairObj:
            self.human.hairObj.mesh.setTexture(self.after)
        return True

    def undo(self):
        if self.human.hairObj:
            self.human.hairObj.mesh.setTexture(self.before)
        return True


class ClothesAction(Action):

    def __init__(self, human, library, clothesUuid, before, after):
        super(ClothesAction, self).__init__('Change clothes texture', human)
        self.before = before
        self.after = after
        self.uuid = clothesUuid
        self.library = library

    def do(self):
        self.library.applyClothesTexture(self.uuid, self.after)
        return True

    def undo(self):
        if self.before:
            self.library.applyClothesTexture(self.uuid, self.before)
        return True


class TextureTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Texture', label='Skin/Material')

        self.systemSkins = os.path.join('data', 'skins')
        self.systemTextures = os.path.join('data', 'clothes', 'textures')

        self.userSkins = os.path.join(mh.getPath(''), 'data', 'skins')
        self.userTextures = os.path.join(mh.getPath(''), 'data', 'clothes', 'textures')
        if not os.path.exists(self.userSkins):
            os.makedirs(self.userSkins)
        if not os.path.exists(self.userTextures):
            os.makedirs(self.userTextures)

        self.defaultTextures = [self.systemTextures, self.userTextures]  
        self.textures = self.defaultTextures
        self.activeClothing = None
        self.eyeTexture = None

        #self.filechooser = self.addTopWidget(fc.FileChooser(self.userSkins, 'png', ['thumb', 'png'], 'data/skins/notfound.thumb'))
        self.filechooser = self.addRightWidget(fc.IconListFileChooser(self.userSkins, 'png', ['thumb', 'png'], 'data/skins/notfound.thumb', 'Texture'))
        self.filechooser.setIconSize(50,50)
        self.addLeftWidget(self.filechooser.createSortBox())

        self.update = self.filechooser.sortBox.addWidget(gui.Button('Check for updates'))
        self.mediaSync = None
        self.mediaSync2 = None

        @self.filechooser.mhEvent
        def onFileSelected(filename):
            human = gui3d.app.selectedHuman
            if self.skinRadio.selected:
                gui3d.app.do(SkinAction(human,
                    human.getTexture(),
                    filename))
            elif self.hairRadio.selected:
                gui3d.app.do(HairAction(human,
                    human.hairObj.getTexture(),
                    filename))
            elif self.eyesRadio.selected:
                # TODO make undoable action 
                self.setEyes(gui3d.app.selectedHuman, filename)
            else: # Clothes
                if self.activeClothing:
                    uuid = self.activeClothing
                    gui3d.app.do(ClothesAction(human,
                        self,
                        uuid,
                        self.getClothesTexture(uuid),
                        filename))

        @self.update.mhEvent
        def onClicked(event):
            self.syncMedia()

        self.objectSelector = []
        self.humanBox = self.addLeftWidget(gui.GroupBox('Human'))
        self.skinRadio = self.humanBox.addWidget(gui.RadioButton(self.objectSelector, "Skin", selected=True))
        self.hairRadio = self.humanBox.addWidget(gui.RadioButton(self.objectSelector, "Hair", selected=False))
        self.eyesRadio = self.humanBox.addWidget(gui.RadioButton(self.objectSelector, "Eyes", selected=False))

        @self.skinRadio.mhEvent
        def onClicked(event):
            if self.skinRadio.selected:
                self.reloadTextureChooser()

        @self.hairRadio.mhEvent
        def onClicked(event):
            if self.hairRadio.selected:
                self.reloadTextureChooser()

        @self.eyesRadio.mhEvent
        def onClicked(event):
            if self.eyesRadio.selected:
                self.reloadTextureChooser()

        self.clothesBox = self.addLeftWidget(gui.GroupBox('Clothes'))
        self.clothesSelections = []


    def onShow(self, event):

        # When the task gets shown, set the focus to the file chooser
        gui3d.TaskView.onShow(self, event)
        human = gui3d.app.selectedHuman

        self.skinRadio.setChecked(True)
        self.reloadTextureChooser()

        if human.hairObj:
            self.hairRadio.setEnabled(True)
        else:
            self.hairRadio.setEnabled(False)

        self.populateClothesSelector()

        # Offer to download skins if none are found    
        self.numSkin = len([filename for filename in os.listdir(os.path.join(mh.getPath(''), 'data', 'skins')) if filename.lower().endswith('png')])
        if self.numSkin < 1:    
            gui3d.app.prompt('No skins found', 'You don\'t seem to have any skins, download them from the makehuman media repository?\nNote: this can take some time depending on your connection speed.', 'Yes', 'No', self.syncMedia)


    def populateClothesSelector(self):
        """
        Builds a list of all available clothes.
        """
        human = gui3d.app.selectedHuman
        # Only keep first 3 radio btns (human body parts)
        for radioBtn in self.objectSelector[3:]:
            radioBtn.hide()
            radioBtn.destroy()
        del self.objectSelector[3:]

        self.clothesSelections = []
        theClothesList = human.clothesObjs.keys()
        self.activeClothing = None
        for i, uuid in enumerate(theClothesList):
            if i == 0:
                self.activeClothing = uuid
            radioBtn = self.clothesBox.addWidget(gui.RadioButton(self.objectSelector, human.clothesProxies[uuid].name, selected=False))
            self.clothesSelections.append( (radioBtn, uuid) )

            @radioBtn.mhEvent
            def onClicked(event):
                for radio, uuid in self.clothesSelections:
                    if radio.selected:
                        self.activeClothing = uuid
                        log.debug( 'Selected clothing "%s" (%s)' % (radio.text(), uuid) )
                        self.reloadTextureChooser()
                        return

    def applyClothesTexture(self, uuid, filename):
        human = gui3d.app.selectedHuman
        if uuid not in human.clothesObjs.keys():
            log.warning("Cannot set texture for clothes with UUID %s, no such item", uuid)
            return False
        clo = human.clothesObjs[uuid]
        clo.mesh.setTexture(filename)
        return True

    def getClothesTexture(self, uuid):
        """
        Get the currently set texture for clothing item with specified UUID.
        """
        human = gui3d.app.selectedHuman
        if uuid not in human.clothesObjs.keys():
            return None
        clo = human.clothesObjs[uuid]
        return clo.getTexture()

    def setEyes(self, human, mhstx):
        # TODO this will change, for now eyes might only be compatible with the original skin
        texture = mh.getTexture(human.getTexture())
        texture.loadSubImage(
            subtextures.combine(mh.Image(human.getTexture()),mhstx), 0, 0)
        self.eyeTexture = mhstx

    def reloadTextureChooser(self):
        human = gui3d.app.selectedHuman
        # TODO this is temporary, until new eye texturing approach
        if 'data/eyes' in self.filechooser.paths:
            self.filechooser.setPreviewExtensions(['thumb', 'png'])
            self.filechooser.extension = 'png'

        selectedTex = None
        if self.skinRadio.selected:
            self.textures = [self.systemSkins, self.userSkins, os.path.join('data', 'textures')]
            selectedTex = human.getTexture()
        elif self.hairRadio.selected:
            proxy = human.hairProxy
            self.textures = [os.path.dirname(proxy.file)]
            selectedTex = hairObj.getTexture()
        elif self.eyesRadio.selected:
            self.filechooser.setPreviewExtensions('png')
            self.filechooser.extension = 'mhstx'
            self.textures = ['data/eyes']
        else: # Clothes
            if self.activeClothing:
                uuid = self.activeClothing
                clo = human.clothesObjs[uuid]
                filepath = human.clothesProxies[uuid].file
                self.textures = [os.path.dirname(filepath)] + self.defaultTextures
                selectedTex = clo.getTexture()
            else:
                # TODO maybe dont show anything?
                self.textures = self.defaultTextures            
                
                filec = self.filechooser
                log.debug("fc %s %s %s added", filec, filec.children.count(), str(filec.files))

        # Reload filechooser
        self.filechooser.deselectAll()
        self.filechooser.setPaths(self.textures)
        self.filechooser.refresh()
        if selectedTex:
            selectedTex = os.path.relpath(selectedTex)
            self.filechooser.selectItem(selectedTex)
        self.filechooser.setFocus()

    def onHide(self, event):
        gui3d.TaskView.onHide(self, event)
        
    def onHumanChanging(self, event):
        pass
        
    def loadHandler(self, human, values):
        
        if values[0] == 'skinTexture':
            (fname, ext) = os.path.splitext(values[1])
            if fname != "texture":
                path = os.path.join(os.path.join(mh.getPath(''), 'data', 'skins', values[1]))
                if os.path.isfile(path):                    
                    human.setTexture(path)
                elif ext == ".tif":
                    path = path.replace(".tif", ".png")
                    human.setTexture(path)
        elif values[0] == 'textures':
            uuid = values[1]
            filepath = values[2]
            if human.hairProxy and human.hairProxy.getUuid() == uuid:
                if not os.path.dirname(filepath):
                    proxy = human.hairProxy
                    hairPath = os.path.dirname(proxy.file)
                    filepath = os.path.join(hairPath, filepath)
                human.hairObj.mesh.setTexture(filepath)
                return
            elif not uuid in human.clothesProxies.keys():
                log.error("Could not load texture for object with uuid %s!" % uuid)
                return
            proxy = human.clothesProxies[uuid]
            if not os.path.dirname(filepath):
                proxy = human.clothesProxies[uuid]
                clothesPath = os.path.dirname(proxy.file)
                filepath = os.path.join(clothesPath, filepath)
            self.applyClothesTexture(uuid, filepath)
            return
        elif values[0] == 'eyeTexture':
            self.setEyes(human, values[1])
       
    def saveHandler(self, human, file):
        
        file.write('skinTexture %s\n' % os.path.basename(human.getTexture()))
        for name, clo in human.clothesObjs.items():
            if clo:
                proxy = human.clothesProxies[name]
                if clo.mesh.texture != proxy.texture[0]+"/"+proxy.texture[1]:
                    clothesPath = os.path.dirname(proxy.file)
                    if os.path.dirname(clo.mesh.texture) == clothesPath:
                        texturePath = os.path.basename(clo.mesh.texture)
                    else:
                        texturePath = clo.mesh.texture
                    file.write('textures %s %s\n' % (proxy.getUuid(), texturePath))
        if human.hairObj and human.hairProxy:
            file.write('textures %s %s\n' % (human.hairProxy.getUuid(), human.hairObj.mesh.texture))
        if self.eyeTexture:
            file.write('eyeTexture %s\n' % self.eyeTexture)

    def syncMedia(self):
        
        if self.mediaSync:
            return
        if not os.path.isdir(self.userSkins):
            os.makedirs(self.userSkins)
        self.mediaSync = download.MediaSync(gui3d.app, self.userSkins, 'http://download.tuxfamily.org/makehuman/skins/', self.syncMediaFinished)
        self.mediaSync.start()
        self.mediaSync2 = None
        
    def syncMediaFinished(self):
        '''
        if not self.mediaSync2:
            if not os.path.isdir(self.userTextures):
                os.makedirs(self.userTextures)
            self.mediaSync2 = download.MediaSync(gui3d.app, self.userTextures, 'http://download.tuxfamily.org/makehuman/clothes/textures/', self.syncMediaFinished)
            self.mediaSync2.start()
            self.mediaSync = None
        else:
            self.mediaSync = None
            self.filechooser.refresh()
        '''

        self.mediaSync = None
        self.filechooser.refresh()
        
# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Textures')
    taskview = TextureTaskView(category)
    taskview.sortOrder = 0
    category.addTask(taskview)

    app.addLoadHandler('textures', taskview.loadHandler)
    app.addLoadHandler('skinTexture', taskview.loadHandler)
    app.addLoadHandler('eyeTexture', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)



# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    pass

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

__docformat__ = 'restructuredtext'

import math
import numpy
from operator import mul
import mh
import os

import algos3d
from algos3d import theHuman, NMHVerts
import warp
import humanmodifier
import log
from core import G

shadowCoords = None

#----------------------------------------------------------
#   class WarpTarget
#----------------------------------------------------------

class WarpTarget(algos3d.Target):

    def __init__(self, modifier, human):
        
        algos3d.Target.__init__(self, human.meshData, modifier.warppath)
        
        self.human = human
        self.modifier = modifier
        self.isWarp = True
        self.isDirty = True
        self.isObsolete = False
        

    def __repr__(self):
        return ( "<WarpTarget %s d:%s o:%s>" % (os.path.basename(self.modifier.warppath), self.isDirty, self.isObsolete) )
        
        
    def reinit(self):
    
        if self.isObsolete:
            halt
        if self.isDirty:
            shape = self.modifier.compileWarpTarget(self.human)
            saveWarpedTarget(shape, self.modifier.warppath)
            self.__init__(self.modifier, self.human)
            self.isDirty = False
        

    def apply(self, obj, morphFactor, update=True, calcNormals=True, faceGroupToUpdateName=None, scale=(1.0,1.0,1.0)):
    
        self.reinit()
        algos3d.Target.apply(self, obj, morphFactor, update, calcNormals, faceGroupToUpdateName, scale)


def saveWarpedTarget(shape, path): 
    slist = list(shape.items())
    slist.sort()
    fp = open(path, "w")
    for (n, dr) in slist:
        fp.write("%d %.4f %.4f %.4f\n" % (n, dr[0], dr[1], dr[2]))
    fp.close()
         
#----------------------------------------------------------
#   class WarpModifier
#----------------------------------------------------------

theModifierTypes = {
    "GenderAge" : [
        ('macrodetails', None, 'Gender'),
        ('macrodetails', None, 'Age'),
    ],
    "GenderAgeEthnic" : [
        ('macrodetails', None, 'Gender'),
        ('macrodetails', None, 'Age'),
        ('macrodetails', None, 'African'),
        ('macrodetails', None, 'Asian'),
    ],
    "GenderAgeToneWeight" : [
        ('macrodetails', None, 'Gender'),
        ('macrodetails', None, 'Age'),
        ('macrodetails', 'universal', 'Tone'),
        ('macrodetails', 'universal', 'Weight'),
        #('macrodetails', 'universal-stature', 'Height'),
    ],
}


class BaseSpec:
    def __init__(self, path, factors):
        self.path = path
        self.factors = factors
        self.value = -1
    
    def __repr__(self):
        return ("<BaseSpec %s %.4f %s>" % (self.path, self.value, self.factors))
    
    
class TargetSpec:
    def __init__(self, path, factors):
        self.path = path
        self.factors = factors
    
    def __repr__(self):
        return ("<TargetSpec %s %s>" % (self.path, self.factors))
    
    
class WarpModifier (humanmodifier.SimpleModifier):

    def __init__(self, template, bodypart, modtype):
        global theModifierTypes, theBaseCharacterParts
                
        string = template.replace('$','').replace('{','').replace('}','')                
        warppath = os.path.join(mh.getPath(""), "warp", string)
        if not os.path.exists(os.path.dirname(warppath)):
            os.makedirs(os.path.dirname(warppath))
        if not os.path.exists(warppath):
            fp = open(warppath, "w")
            fp.close()
            
        humanmodifier.SimpleModifier.__init__(self, warppath)
        self.eventType = 'warp'
        self.warppath = warppath
        self.template = template
        self.isWarp = True
        self.bodypart = bodypart
        self.slider = None
        self.refTargets = {}
        self.refTargetVerts = {}        
        self.modtype = modtype
        
        self.fallback = None
        for (tlabel, tname, tvar) in theModifierTypes[modtype]:
            self.fallback = humanmodifier.MacroModifier(tlabel, tname, tvar)
            break
            
        self.bases = {}
        self.targetSpecs = {}
        if modtype == "GenderAge":            
            self.setupBaseCharacters("Gender", "Age", "NoEthnic", "NoUniv", "NoUniv")
        elif modtype == "GenderAgeEthnic":            
            self.setupBaseCharacters("Gender", "Age", "Ethnic", "NoUniv", "NoUniv")
        elif modtype == "GenderAgeToneWeight":
            self.setupBaseCharacters("Gender", "Age", "NoEthnic", "Tone", "Weight")


    def setupBaseCharacters(self, genders, ages, ethnics, tones, weights):
    
        baseCharacterParts = {
            "Gender" : ("male", "female"),
            "Age" : ("child", "young", "old"),
            "Ethnic" : ("caucasian", "african", "asian"),
            "NoEthnic" : [None],
            "Tone" : ("flaccid", None, "muscle"),
            "Weight" : ("light", None, "heavy"),
            "NoUniv" : [None]
        }

        for gender in baseCharacterParts[genders]:
            for age in baseCharacterParts[ages]:
                for ethnic1 in baseCharacterParts[ethnics]:                    
                    path1 = self.template
                    
                    if ethnic1 is None:
                        base1 = "data/targets/macrodetails/neutral-%s-%s.target" % (gender, age)    
                        key1 = "%s-%s" % (gender, age)                      
                        factors1 = [gender, age]
                    else:
                        if ethnic1 == "caucasian":
                            ethnic2 = "neutral"
                        else:
                            ethnic2 = ethnic1
                        base1 = "data/targets/macrodetails/%s-%s-%s.target" % (ethnic2, gender, age)    
                        key1 = "%s-%s-%s" % (ethnic1, gender, age)  
                        factors1 = [ethnic1, gender, age]
                        path1 = path1.replace("${ethnic}", ethnic1)

                    self.bases[key1] = BaseSpec(base1, factors1)
                    path1 = path1.replace("${gender}", gender).replace("${age}",age)
                    
                    for tone in baseCharacterParts[tones]:
                        for weight in baseCharacterParts[weights]:            
                            if tone and weight:    
                                base2 = "data/targets/macrodetails/universal-%s-%s-%s-%s.target" % (gender, age, tone, weight)
                                key2 = "universal-%s-%s-%s-%s" % (gender, age, tone, weight)
                                factors2 = factors1 + [tone, weight]
                                self.bases[key2] = BaseSpec(base2, factors2)
                                path2 = path1.replace("${tone}", tone).replace("${weight}", weight)
                                self.targetSpecs[key2] = TargetSpec(path2, factors2)
                                
                            elif tone:    
                                base2 = "data/targets/macrodetails/universal-%s-%s-%s.target" % (gender, age, tone)
                                key2 = "universal-%s-%s-%s" % (gender, age, tone)
                                factors2 = factors1 + [tone, 'averageWeight']
                                self.bases[key2] = BaseSpec(base2, factors2)
                                path2 = path1.replace("${tone}", tone).replace("-${weight}", "")
                                self.targetSpecs[key2] = TargetSpec(path2, factors2)
                        
                            elif weight:    
                                base2 = "data/targets/macrodetails/universal-%s-%s-%s.target" % (gender, age, weight)
                                key2 = "universal-%s-%s-%s" % (gender, age, weight)
                                factors2 = factors1 + ['averageTone', weight]
                                self.bases[key2] = BaseSpec(base2, factors2)
                                path2 = path1.replace("-${tone}", "").replace("${weight}", weight)
                                self.targetSpecs[key2] = TargetSpec(path2, factors2)
                                
                            else:                            
                                factors2 = factors1 + ['averageTone', 'averageWeight']
                                path2 = path1.replace("-${tone}", "").replace("-${weight}", "")
                                self.targetSpecs[key1] = TargetSpec(path2, factors2)




    def __repr__(self):
        return ("<WarpModifier %s>" % (os.path.basename(self.template)))
            

    def setValue(self, human, value):
        humanmodifier.SimpleModifier.setValue(self, human, value)
        human.warpNeedReset = False


    def updateValue(self, human, value, updateNormals=1):        
        target = self.getWarpTarget(theHuman)    
        if not target:
            return
        target.reinit()
        humanmodifier.SimpleModifier.updateValue(self, human, value, updateNormals)
        human.warpNeedReset = False
        

    def clampValue(self, value):
        return max(0.0, min(1.0, value))


    def compileWarpTarget(self, human):
        global shadowCoords
        log.message("Compile %s", self)
        landmarks = theLandMarks()[self.bodypart]
        objectChanged = self.getRefObject(human)
        self.getRefTarget(human, objectChanged)    
        if self.refTargetVerts and _theRefObjectVerts[self.modtype] is not None:
            shape = warp.warp_target(self.refTargetVerts, _theRefObjectVerts[self.modtype], shadowCoords, landmarks)
        else:
            shape = {}
        log.message("...done")
        return shape


    def getRefTarget(self, human, objectChanged):       
        targetChanged = self.getBases(human)
        if targetChanged or objectChanged:
            log.message("Reference target changed")
            if not self.makeRefTarget(human):
                log.message("Updating character")
                human.applyAllTargets()
                self.getBases(human)
                if not self.makeRefTarget(human):
                    raise NameError("Character is empty")
                    
    
    def getBases(self, human):
        targetChanged = False
        for key,base in self.bases.items():
            verts = self.getRefObjectVerts(base.path)
            if verts is None:            
                base.value = 0
                continue
    
            cval1 = human.getDetail(base.path)    
            if base.value != cval1:
                base.value = cval1
                targetChanged = True
        return targetChanged
        

    def makeRefTarget(self, human):
        self.refTargetVerts = {}
        madeRefTarget = False
        factors = self.fallback.getFactors(human, 1.0)
        
        for target in self.targetSpecs.values():        
            cval = reduce(mul, [factors[factor] for factor in target.factors])
            if cval > 0:
                log.debug("  reftrg %s %s", target.path, cval)
                madeRefTarget = True
                verts = self.getTargetInsist(target.path)
                if verts is not None:
                    addVerts(self.refTargetVerts, cval, verts)
        return madeRefTarget                            
    

    def getTargetInsist(self, path):
        verts = self.getTarget(path)
        if verts is not None:
            self.refTargets[path] = verts
            return verts
            
        for string in ["flaccid", "muscle", "light", "heavy"]:
            if string in path:
                log.message("  Did not find %s", path)
                return None
    
        path1 = path.replace("asian", "caucasian").replace("neutral", "caucasian").replace("african", "caucasian")
        path1 = path1.replace("cauccaucasian", "caucasian")
        verts = self.getTarget(path1)
        if verts is not None:
            self.refTargets[path] = verts
            log.message("   Replaced %s\n  -> %s", path, path1)
            return verts
            
        path2 = path1.replace("child", "young").replace("old", "young")
        verts = self.getTarget(path2)
        if verts is not None:
            self.refTargets[path] = verts
            log.message("   Replaced %s\n  -> %s", path, path2)
            return verts
            
        path3 = path2.replace("male", "female")
        path3 = path3.replace("fefemale", "female")
        verts = self.getTarget(path3)
        self.refTargets[path] = verts
        if verts is None:
            log.message("Warning: Found none of:\n    %s\n    %s\n    %s\n    %s", path, path1, path2, path3)
        else:
            log.message("   Replaced %s\n  -> %s", path, path3)        
        return verts


    def getTarget(self, path):
        try:
            verts = self.refTargets[path]
        except KeyError:
            verts = None
        if verts is None:
            verts = readTarget(path)
        return verts            
          

    def getWarpTarget(self, human):
        try:
            target = algos3d.targetBuffer[self.warppath]
        except KeyError:
            target = None
    
        if target:
            if not hasattr(target, "isWarp"):
                log.message("Found non-warp target: %s. Deleted", target.name)
                del algos3d.targetBuffer[self.warppath]
                return None
                #raise NameError("%s should be warp" % target)
            return target
            
        target = WarpTarget(self, human)
        algos3d.targetBuffer[self.warppath] = target
        return target    
        
        
    def removeTarget(self):
        try:
            target = algos3d.targetBuffer[self.warppath]
        except KeyError:
            return        
        del algos3d.targetBuffer[self.warppath]
        
        
    def getRefObject(self, human):
        global _theRefObjectVerts
    
        if _theRefObjectVerts[self.modtype] is not None:
            return False
        else:
            log.message("Reset warps")
            refverts = numpy.array(G.app.selectedHuman.meshData.orig_coord)
            for char in theRefObjects().keys():
                cval = human.getDetail(char)
                if cval:
                    log.debug("  refobj %s %s", os.path.basename(char), cval)
                    verts = self.getRefObjectVerts(char)
                    if verts is not None:
                        addVerts(refverts, cval, verts)
            _theRefObjectVerts[self.modtype] = refverts                
            return True


    def getRefObjectVerts(self, path):
        refObjects = theRefObjects()
    
        if refObjects[path]:
            return refObjects[path]
        else:
            verts = readTarget(path)
            if verts is not None:
                refObjects[path] = verts
            return verts            
    

def removeAllWarpTargets(human):
    log.message("Removing all warp targets")
    for target in algos3d.targetBuffer.values():
        if hasattr(target, "isWarp"):
            log.message("  %s", target)
            target.isDirty = True
            target.isObsolete = True
            human.setDetail(target.name, 0)
            target.morphFactor = 0
            target.modifier.setValue(human, 0)
            if target.modifier.slider:
                target.modifier.slider.update()     
            del algos3d.targetBuffer[target.name]


def getWarpedCoords(human):
    global shadowCoords

    if shadowCoords == None:
        shadowCoords = human.meshData.coord.copy()
    coords = shadowCoords.copy()
    for target in algos3d.targetBuffer.values():
        if hasattr(target, "isWarp") and not hasattr(target, "isPose"):
            verts = algos3d.targetBuffer[target.name].verts
            coords[verts] += target.morphFactor * target.data
    return coords                
            

#----------------------------------------------------------
#   Call from exporter
#----------------------------------------------------------

def compileWarpTarget(template, fallback, human, bodypart):
    mod = WarpModifier(template, bodypart, fallback)
    return mod.compileWarpTarget(human)
                
#----------------------------------------------------------
#   Read target
#----------------------------------------------------------                

def readTarget(path):
    try:        
        fp = open(path, "r")
    except:
        fp = None
    if fp:
        target = {}
        for line in fp:
            words = line.split()
            if len(words) >= 4:
                n = int(words[0])
                if n < NMHVerts:
                    target[n] = numpy.array([float(words[1]), float(words[2]), float(words[3])])
        fp.close()
        return target
    else:
        log.message("Could not find %s" % os.path.realpath(path))
        return None

#----------------------------------------------------------
#   For testing numpy
#----------------------------------------------------------

"""    
import numpy
 
def addVerts(targetVerts, cval, verts):     
    return targetVerts + cval*verts
    
""" 
def addVerts(targetVerts, cval, verts):                    
    for n,v in verts.items():
        dr = cval*v
        try:
            targetVerts[n] += dr
        except KeyError:
            targetVerts[n] = dr
    
#----------------------------------------------------------
#   Init globals
#----------------------------------------------------------

def clearRefObject():
    global _theRefObjectVerts
    _theRefObjectVerts = {}
    for mtype in theModifierTypes.keys():
        _theRefObjectVerts[mtype] = None
    

def theLandMarks():
    global _theLandMarks

    if _theLandMarks is not None:
        return _theLandMarks

    _theLandMarks = {}
    folder = "data/landmarks"
    for file in os.listdir(folder):
        (name, ext) = os.path.splitext(file)
        if ext != ".lmk":
            continue
        path = os.path.join(folder, file)
        with open(path, "r") as fp:
            landmark = []
            for line in fp:
                words = line.split()    
                if len(words) > 0:
                    m = int(words[0])
                    landmark.append(m)

        _theLandMarks[name] = landmark

    return _theLandMarks


def theRefObjects():
    global _theRefObjects

    if _theRefObjects is not None:
        return _theRefObjects

    clearRefObject()
    _theRefObjects = {}

    for ethnic in ["african", "asian", "neutral"]:
        for age in ["child", "young", "old"]:
            for gender in ["female", "male"]:
                path = "data/targets/macrodetails/%s-%s-%s.target" % (ethnic, gender, age)
                _theRefObjects[path] = None

    for age in ["child", "young", "old"]:
        for gender in ["female", "male"]:
            for tone in ["flaccid", "muscle"]:
                path = "data/targets/macrodetails/universal-%s-%s-%s.target" % (gender, age, tone)
                _theRefObjects[path] = None
                for weight in ["light", "heavy"]:
                    path = "data/targets/macrodetails/universal-%s-%s-%s-%s.target" % (gender, age, tone, weight)
                    _theRefObjects[path] = None
            for weight in ["light", "heavy"]:
                path = "data/targets/macrodetails/universal-%s-%s-%s.target" % (gender, age, weight)
                _theRefObjects[path] = None

    return _theRefObjects


_theRefObjectVerts = None    
_theLandMarks = None
_theRefObjects = None

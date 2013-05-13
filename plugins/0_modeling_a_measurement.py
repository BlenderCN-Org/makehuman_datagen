#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

import os
import math
import numpy as np
import gui3d
import module3d
import humanmodifier
import mh
import gui
import log

class MeasurementValueConverter(object):

    def __init__(self, task, measure, modifier):

        self.task = task
        self.measure = measure
        self.modifier = modifier
        self.value = 0.0
        self.units = 'cm' if gui3d.app.settings['units'] == 'metric' else 'in'

    def dataToDisplay(self, value):
        self.value = value
        return self.task.getMeasure(self.measure)

    def displayToData(self, value):
        goal = float(value)
        measure = self.task.getMeasure(self.measure)
        minValue = -1.0
        maxValue = 1.0
        if math.fabs(measure - goal) < 0.01:
            return self.value
        else:
            tries = 10
            while tries:
                if math.fabs(measure - goal) < 0.01:
                    break;
                if goal < measure:
                    maxValue = self.value
                    if value == minValue:
                        break
                    self.value = minValue + (self.value - minValue) / 2.0
                    self.modifier.updateValue(gui3d.app.selectedHuman, self.value, 0)
                    measure = self.task.getMeasure(self.measure)
                else:
                    minValue = self.value
                    if value == maxValue:
                        break
                    self.value = self.value + (maxValue - self.value) / 2.0
                    self.modifier.updateValue(gui3d.app.selectedHuman, self.value, 0)
                    measure = self.task.getMeasure(self.measure)
                tries -= 1
        return self.value

class GroupBoxRadioButton(gui.RadioButton):
    def __init__(self, task, group, label, groupBox, selected=False):
        super(GroupBoxRadioButton, self).__init__(group, label, selected)
        self.groupBox = groupBox
        self.task = task

    def onClicked(self, event):
        self.task.groupBox.showWidget(self.groupBox)
        self.task.onSliderFocus(self.groupBox.children[0])

class MeasureSlider(humanmodifier.ModifierSlider):
    def __init__(self, label, task, measure, modifier):

        humanmodifier.ModifierSlider.__init__(self, value=0.0, min=-1.0, max=1.0,
            label=label, modifier=modifier, valueConverter=MeasurementValueConverter(task, measure, modifier))
        self.measure = measure
        self.task = task

    def onChange(self, value):
        super(MeasureSlider, self).onChange(value)
        self.task.syncSliderLabels()

    def onFocus(self, event):
        super(MeasureSlider, self).onFocus(event)
        self.task.onSliderFocus(self)

    def onBlur(self, event):
        super(MeasureSlider, self).onBlur(event)
        self.task.onSliderBlur(self)

class MeasureTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Measure')

        self.ruler = Ruler()

        self.measureMesh = module3d.Object3D('measure', 2)
        fg = self.measureMesh.createFaceGroup('measure')

        count = max([len(vertIdx) for vertIdx in self.ruler.Measures.values()])

        self.measureMesh.setCoords(np.zeros((count, 3), dtype=np.float32))
        self.measureMesh.setUVs(np.zeros((1, 2), dtype=np.float32))
        self.measureMesh.setFaces(np.arange(count).reshape((-1,2)))

        self.measureMesh.setCameraProjection(0)
        self.measureMesh.setShadeless(True)
        self.measureMesh.setDepthless(True)
        self.measureMesh.setColor([255, 255, 255, 255])
        self.measureMesh.setPickable(0)
        self.measureMesh.updateIndexBuffer()
        self.measureMesh.priority = 50

        self.measureObject = self.addObject(gui3d.Object([0, 0, 0], self.measureMesh))

        measurements = [
            ('neck', ['neckcirc', 'neckheight']),
            ('upperarm', ['upperarm', 'upperarmlength']),
            ('lowerarm', ['lowerarmlength', 'wrist']),
            ('torso', ['frontchest', 'bust', 'underbust', 'waist', 'napetowaist', 'waisttohip', 'shoulder']),
            ('hips', ['hips']),
            ('upperleg', ['upperlegheight', 'thighcirc']),
            ('lowerleg', ['lowerlegheight', 'calf']),
            ('ankle', ['ankle']),
        ]

        metric = gui3d.app.settings['units'] == 'metric'

        sliderLabel = {
            'neckcirc':'Neck circum',
            'neckheight':'Neck height',
            'upperarm':'Upper arm circum',
            'upperarmlength':'Upperarm length',
            'lowerarmlength':'Lowerarm length',
            'wrist':'Wrist circum',
            'frontchest':'Front chest dist',
            'bust':'Bust circum',
            'underbust':'Underbust circum',
            'waist':'Waist circum',
            'napetowaist':'Nape to waist',
            'waisttohip':'Waist to hip',
            'shoulder':'Shoulder dist',
            'hips':'Hips circum',
            'upperlegheight':'Upperleg height',
            'thighcirc':'Thigh circ.',
            'lowerlegheight':'Lowerleg height',
            'calf':'Calf circum',
            'ankle':'Ankle circum'
        }

        self.groupBoxes = {}
        self.radioButtons = []
        self.sliders = []
        self.active_slider = None

        self.modifiers = {}

        measureDataPath = "data/targets/measure/"

        self.categoryBox = self.addRightWidget(gui.GroupBox('Category'))
        self.groupBox = self.addLeftWidget(gui.StackedBox())

        for name, subnames in measurements:
            # Create box
            box = self.groupBox.addWidget(gui.SliderBox(name.capitalize()))
            self.groupBoxes[name] = box

            # Create radiobutton
            box.radio = self.categoryBox.addWidget(GroupBoxRadioButton(self, self.radioButtons, name.capitalize(), box, selected=len(self.radioButtons) == 0))

            # Create sliders
            for subname in subnames:
                modifier = humanmodifier.Modifier(
                    os.path.join(measureDataPath, "measure-%s-decrease.target" % subname),
                    os.path.join(measureDataPath, "measure-%s-increase.target" % subname))
                self.modifiers[subname] = modifier
                slider = box.addWidget(MeasureSlider(sliderLabel[subname], self, subname, modifier))
                self.sliders.append(slider)

        self.statsBox = self.addRightWidget(gui.GroupBox('Statistics'))
        self.height = self.statsBox.addWidget(gui.TextView('Height: '))
        self.chest = self.statsBox.addWidget(gui.TextView('Chest: '))
        self.waist = self.statsBox.addWidget(gui.TextView('Waist: '))
        self.hips = self.statsBox.addWidget(gui.TextView('Hips: '))

        self.braBox = self.addRightWidget(gui.GroupBox('Brassiere size'))
        self.eu = self.braBox.addWidget(gui.TextView('EU: '))
        self.jp = self.braBox.addWidget(gui.TextView('JP: '))
        self.us = self.braBox.addWidget(gui.TextView('US: '))
        self.uk = self.braBox.addWidget(gui.TextView('UK: '))

        self.groupBox.showWidget(self.groupBoxes['neck'])

    def showGroup(self, name):
        self.groupBoxes[name].radio.setSelected(True)
        self.groupBox.showWidget(self.groupBoxes[name])
        self.groupBoxes[name].children[0].setFocus()

    def getMeasure(self, measure):

        human = gui3d.app.selectedHuman
        measure = self.ruler.getMeasure(human, measure, gui3d.app.settings['units'])
        #if gui3d.app.settings['units'] == 'metric':
        #    return '%.1f cm' % measure
        #else:
        #    return '%.1f in' % measure
        return measure

    def hideAllBoxes(self):

        for box in self.groupBoxes.values():
            box.hide()

    def onShow(self, event):

        gui3d.TaskView.onShow(self, event)
        self.groupBoxes['neck'].children[0].setFocus()
        self.syncSliders()
        human = gui3d.app.selectedHuman
        self.cloPickableProps = dict()
        for uuid, clo in human.clothesObjs.items():
            self.cloPickableProps[uuid] = clo.mesh.pickable
            clo.mesh.setPickable(False)

    def onHide(self, event):
        human = gui3d.app.selectedHuman
        for uuid, pickable in self.cloPickableProps.items():
            clo = human.clothesObjs[uuid]
            clo.mesh.setPickable(pickable)

    def onSliderFocus(self, slider):
        self.active_slider = slider
        self.updateMeshes()
        self.measureObject.show()

    def onSliderBlur(self, slider):
        if self.active_slider is slider:
            self.active_slider = None
        self.measureObject.hide()

    def updateMeshes(self):
        if self.active_slider is None:
            return

        human = gui3d.app.selectedHuman

        vertidx = self.ruler.Measures[self.active_slider.measure]

        coords = human.meshData.coord[vertidx]
        self.measureMesh.coord[:len(vertidx),:] = coords
        self.measureMesh.coord[len(vertidx):,:] = coords[-1:]
        self.measureMesh.markCoords(coor = True)
        self.measureMesh.update()

    def onHumanChanged(self, event):

        self.updateMeshes()

    def onHumanTranslated(self, event):

        self.measureObject.setPosition(gui3d.app.selectedHuman.getPosition())

    def onHumanRotated(self, event):

        self.measureObject.setRotation(gui3d.app.selectedHuman.getRotation())

    def syncSliders(self):

        for slider in self.sliders:
            slider.update()

        self.syncStatistics()
        self.syncBraSizes()

    def syncSliderLabels(self):

        self.syncStatistics()
        self.syncBraSizes()

    def syncStatistics(self):

        human = gui3d.app.selectedHuman

        height = 10 * max(human.meshData.coord[8223,1] - human.meshData.coord[12361,1],
                          human.meshData.coord[8223,1] - human.meshData.coord[13155,1])
        if gui3d.app.settings['units'] == 'metric':
            height = '%.2f cm' % height
        else:
            height = '%.2f in' % (height * 0.393700787)

        self.height.setTextFormat('Height: %s', height)
        self.chest.setTextFormat('Chest: %s', self.getMeasure('bust'))
        self.waist.setTextFormat('Waist: %s', self.getMeasure('waist'))
        self.hips.setTextFormat('Hips: %s', self.getMeasure('hips'))

    def syncBraSizes(self):

        human = gui3d.app.selectedHuman

        bust = self.ruler.getMeasure(human, 'bust', 'metric')
        underbust = self.ruler.getMeasure(human, 'underbust', 'metric')

        eucups = ['AA', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']

        mod = int(underbust)%5
        band = underbust - mod if mod < 2.5 else underbust - mod + 5
        cup = max(0, int(round(((bust - underbust - 10) / 2))))
        self.eu.setText('EU: %d%s' % (band, eucups[cup]))

        jpcups = ['AAA', 'AA', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']

        mod = int(underbust)%5
        band = underbust - mod if mod < 2.5 else underbust - mod + 5
        cup = max(0, int(round(((bust - underbust - 5) / 2.5))))
        self.jp.setText('JP: %d%s' % (band, jpcups[cup]))

        uscups = ['AA', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']

        band = underbust * 0.393700787
        band = band + 5 if int(band)%2 else band + 4
        cup = max(0, int(round((bust - underbust - 10) / 2)))
        self.us.setText('US: %d%s' % (band, uscups[cup]))

        ukcups = ['AA', 'A', 'B', 'C', 'D', 'DD', 'E', 'F', 'FF', 'G', 'GG', 'H']

        self.uk.setText('UK: %d%s' % (band, ukcups[cup]))

    def loadHandler(self, human, values):

        modifier = self.modifiers.get(values[1], None)
        if modifier:
            modifier.setValue(human, float(values[2]))

    def saveHandler(self, human, file):

        for name, modifier in self.modifiers.iteritems():
            value = modifier.getValue(human)
            if value:
                file.write('measure %s %f\n' % (name, value))

def load(app):
    """
    Plugin load function, needed by design.
    """
    category = app.getCategory('Modelling')
    taskview = category.addTask(MeasureTaskView(category))

    app.addLoadHandler('measure', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)

    @taskview.mhEvent
    def onMouseDown(event):
        part = app.getSelectedFaceGroup()
        bodyZone = app.selectedHuman.getPartNameForGroupName(part.name)
        log.message("body zone %s", bodyZone)
        if bodyZone in app.selectedHuman.bodyZones:
            if bodyZone == "neck":
                taskview.showGroup('neck')
            elif (bodyZone == "r-upperarm") or (bodyZone == "l-upperarm"):
                taskview.showGroup('upperarm')
            elif (bodyZone == "r-lowerarm") or (bodyZone == "l-lowerarm"):
                taskview.showGroup('lowerarm')
            elif (bodyZone == "torso") or (bodyZone == "pelvis"):
                taskview.showGroup('torso')
            elif bodyZone == "hip":
                taskview.showGroup('hips')
            elif (bodyZone == "l-upperleg") or (bodyZone == "r-upperleg"):
                taskview.showGroup('upperleg')
            elif (bodyZone == "l-lowerleg") or (bodyZone == "r-lowerleg"):
                taskview.showGroup('lowerleg')
            elif (bodyZone == "l-foot") or (bodyZone == "r-foot"):
                taskview.showGroup('ankle')

    taskview.showGroup('neck')

def unload(app):
    pass

class Ruler:

    """
  This class contains ...
  """

    def __init__(self):

    # these are tables of vertex indices for each body measurement of interest

        self.Measures = {}
        self.Measures['thighcirc'] = [7066,7205,7204,7192,7179,7176,7166,6886,7172,6813,7173,7101,7033,7032,7041,7232,7076,7062,7063,7229,7066]
        self.Measures['neckcirc'] = [3131,3236,3058,3059,2868,2865,3055,3137,5867,2857,3483,2856,3382,2916,2915,3417,8186,10347,10786,
                                    10785,10373,10818,10288,10817,9674,10611,10809,10806,10674,10675,10515,10614,3131]
        self.Measures['neckheight'] = [8184,8185,8186,8187,7463]
        self.Measures['upperarm']=[10701,10700,10699,10678,10337,10334,10333,10330,10280,10331,10702,10708,9671,10709,10329,10328,10701]
        self.Measures['wrist']=[9894,9895,9607,9606,9806,10512,10557,9807,9808,9809,9810,10565,9653,9682,9681,9832,10507,9894]
        self.Measures['frontchest']=[2961,10764]
        self.Measures['bust']=[6908,3559,3537,3556,3567,3557,4178,3558,4193,3561,3566,3565,3718,3563,2644,4185,2554,4169,2553,3574,2634,2653,3466,3392,
                2942,3387,4146,4433,2613,10997,9994,10078,10368,10364,10303,10380,10957,10976,10218,11055,10060,11054,10044,10966,10229,10115,
                10227,10226,10231,10036,10234,10051,10235,10225,10236,10255,10233,6908]
        self.Measures['napetowaist']=[7463,7472]
        self.Measures['waisttohip']=[4681,6575]
        self.Measures['shoulder'] = [10819,10816,10021,10821,10822,10693,10697]
        self.Measures['underbust'] = [7245,3583,6580,3582,3705,3581,3411,3401,3467,4145,2612,10998,10080,10302,10366,10356,10352,10362,10361,10350,10260,10349,7259,7245]
        self.Measures['waist'] = [6853,4682,3529,2950,3702,3594,3405,5689,3587,4466,6898,9968,10086,9970,10359,10197,10198,10130,10771,10263,6855,6853]
        self.Measures['upperlegheight'] = [6755,7026]
        self.Measures['lowerlegheight'] = [6866,13338]
        self.Measures['calf'] = [7141,7142,7137,6994,6989,6988,6995,6997,6774,6775,6999,6803,6974,6972,6971,7002,7140,7139,7141]
        self.Measures['ankle'] = [6938,6937,6944,6943,6948,6784,6935,6766,6767,6954,6799,6955,6958,6949,6952,6941,6938]
        self.Measures['upperarmlength'] = [9945,10696]
        self.Measures['lowerarmlength'] = [9696,9945]
        self.Measures['hips'] = [7298,2936,3527,2939,2940,3816,3817,3821,4487,3822,3823,3913,3915,4506,5688,4505,4504,4503,6858,6862,6861,6860,
                                            6785,6859,7094,7096,7188,7189,6878,7190,7194,7195,7294,7295,7247,7300,7298]

    def getMeasure(self, human, measurementname, mode):
        measure = 0
        vindex1 = self.Measures[measurementname][0]
        for vindex2 in self.Measures[measurementname]:
            vec = human.meshData.coord[vindex1] - human.meshData.coord[vindex2]
            measure += math.sqrt(vec.dot(vec))
            vindex1 = vindex2

        if mode == 'metric':
            return 10.0 * measure
        else:
            return 10.0 * measure * 0.393700787

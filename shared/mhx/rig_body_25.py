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

Body bone definitions 
"""


from .flags import *
from . import posebone
from posebone import addPoseBone

BodyJoints = [
    ('root-tail',      'o', ('spine3', [0,-1,0])),
    ('hips-tail',      'o', ('pelvis', [0,-1,0])),
    ('mid-uplegs',     'l', ((0.5, 'l-upper-leg'), (0.5, 'r-upper-leg'))),
    ('spine-pt',       'o', ('spine2', [0,0,-10])),

    ('r-breast',       'vl', ((0.4, 3559), (0.6, 2944))),
    ('r-tit',          'v', 3718),
    ('l-breast',       'vl', ((0.4, 10233), (0.6, 10776))),
    ('l-tit',          'v', 10115),

    ('neck2',          'vl', ((0.5, 6531), (0.5, 8253))),

    ('rib-top',        'vl', ((0.8, 6857), (0.2, 7457))),
    ('stomach-top',    'vl', ((0.8, 6909), (0.2, 7460))),
    ('stomach-bot',    'vl', ((0.8, 7359), (0.2, 7186))),

    ('penis-top',      'vl', ((0.5, 2791), (0.5, 7449))),
    ('penis-mid',      'vl', ((0.5, 2844), (0.5, 7369))),
    ('penis-tip',      'v', 7415),
    ('pubis',          'l', ((1.5, 'penis-top'), (-0.5, 'penis-mid'))),
    ('scrotum-tip',    'v', 7444),
    ('scrotum-root',   'vl', ((0.5, 2807), (0.5, 7425))),
]

if MuscleBones:
    BodyJoints = [
    #('stomach-mid',    'vl', ((0.9, 7315), (0.1, 7489))),    
    ('stomach-end',    'l', ((0.1, 'rib-bot'), (0.9, 'stomach-bot'))),
    ('stomach-mid',    'l', ((0.3, 'rib-bot'), (0.7, 'stomach-end'))),

    ('r-waist-up',     'vl', ((0.9, 3408), (0.1, 10356))),
    ('l-waist-up',     'vl', ((0.1, 3408), (0.9, 10356))),
    ('r-waist-down',   'vl', ((0.9, 2931), (0.1, 7305))),
    ('l-waist-down',   'vl', ((0.1, 2931), (0.9, 7305))),

]

BodyHeadsTails = [
    ('MasterFloor',    'floor', ('floor', zunit)),

    ('Root',           'root-tail', 'spine3'),
    ('Shoulders',      'neck', ('neck', [0,-1,0])),

    # Up spine
    ('Pelvis',         'root-tail', 'spine3'),
    ('Hips',           'spine3', 'root-tail'),
    ('Spine1',         'spine3', 'spine2'),
    ('Spine2',         'spine2', 'spine1'),
    ('Spine3',         'spine1', 'neck'),
    ('Neck',           'neck', 'neck2'),
    ('Head',           'neck2', 'head-end'),

    ('SpinePT',        'spine-pt', ('spine-pt', yunit)),
    ('SpineLinkPT',    'spine2', 'spine-pt'),

    # Down spine    
    ('DownRoot',       'root-tail', 'spine3'),
    ('DownHips',       'spine3', 'root-tail'),
    ('DownSpine1',     'spine2', 'spine3'),
    ('DownSpine2',     'spine1', 'spine2'),
    ('DownSpine3',     'neck', 'spine1'),
    ('DownNeck',       'neck', 'neck2'),
    
    ('DownPT0',        ('root-tail', [0,0,-1]), ('root-tail', [0,0.5,-1])),
    ('DownPT1',        ('spine3', [0,0,-1]), ('spine3', [0,0.5,-1])),
    ('DownPT2',        ('spine2', [0,0,-1]), ('spine2', [0,0.5,-1])),
    ('DownPT3',        ('spine1', [0,0,-1]), ('spine1', [0,0.5,-1])),

    # Deform spine
    ('DfmPelvis',      'root-tail', 'spine3'),
    ('DfmHips',        'spine3', 'root-tail'),
    ('DfmSpine1',      'spine3', 'spine2'),
    ('DfmSpine2',      'spine2', 'spine1'),
    ('DfmSpine3',      'spine1', 'neck'),
    ('DfmNeck',        'neck', 'neck2'),
    ('DfmHead',        'neck2', 'head-end'),

    ('Breast_L',       'r-breast', 'r-tit'),
    ('Breast_R',       'l-breast', 'l-tit'),

    ('DfmRib',         'rib-top', 'stomach-top'),
    ('DfmStomach',     'stomach-top', 'stomach-bot'),
    ('StomachTrg',     'root-tail', 'stomach-bot'),

    # Male genitalia
    ('Penis1',         'pubis', 'penis-mid'),
    ('Penis2',         'penis-mid', 'penis-tip'),
    ('Scrotum',        'scrotum-root', 'scrotum-tip'),
]

if MuscleBones:
    BodyHeadsTails += [
    # Deform torso
    ('DfmStomach1',    'rib-bot', 'stomach-mid'),
    ('Stomach',        'stomach-mid', ('stomach-mid', ysmall)),
    ('DfmStomach2',    'stomach-mid', 'stomach-bot'),
    ('StomachStretch', 'rib-bot', 'stomach-bot'),

    ('DfmWaist_L',     'r-waist-up', 'r-waist-down'),
    ('DfmWaist_R',     'l-waist-up', 'l-waist-down'),
    ('WaistTrg_L',     'r-waist-down', ('r-waist-down', yunit)),
    ('WaistTrg_R',     'l-waist-down', ('l-waist-down', yunit)),

    ('Pubis',          'pubis', ('pubis', ysmall)),
    ('Pubis_L',        'r-pubis', ('r-pubis', yunit)),
    ('Pubis_R',        'l-pubis', 'r-pubis'),

]

L_UPSPN = L_UPSPNFK+L_UPSPNIK
L_DNSPN = L_DNSPNFK+L_DNSPNIK

BodyArmature1 = [
    ('MasterFloor',        0, None, F_WIR, L_MAIN, NoBB),

    ('Root',               0, Master, F_WIR, L_MAIN+L_UPSPN+L_DNSPNIK, NoBB),
    ('Shoulders',          0, Master, F_WIR, L_UPSPNIK+L_DNSPN, NoBB),

    # Up spine
    ('Hips',               0, 'Root', F_WIR, L_UPSPN, NoBB),
    ('Pelvis',             0, 'Root', F_WIR, L_UPSPNFK, NoBB),
    ('Spine1',             0, 'Pelvis', F_WIR, L_UPSPNFK, NoBB),
    ('Spine2',             0, 'Spine1', F_WIR, L_UPSPNFK, NoBB),
    ('Spine3',             0, 'Spine2', F_WIR, L_UPSPNFK, NoBB),
    ('Neck',               0, 'Spine3', F_WIR, L_UPSPN+L_HEAD, NoBB),
]    

BodyArmature2Simple = [
    ('DfmPelvis',          0, 'Pelvis', 0, L_HELP, NoBB),
    ('DfmHips',            0, 'Hips', F_DEF, L_DEF, NoBB),
]

BodyArmature2Advanced = [
    ('DfmPelvis',          0, None, 0, L_HELP, NoBB),
    ('DfmHips',            0, 'DfmPelvis', F_DEF, L_DEF, NoBB),
]

BodyArmature3 = [
    # Deform spine    
    ('DfmSpine1',          0, 'DfmPelvis', F_DEF+F_CON, L_DEF, (1,1,3) ),
    ('DfmSpine2',          0, 'DfmSpine1', F_DEF+F_CON, L_DEF, (1,1,3) ),
    ('DfmSpine3',          0, 'DfmSpine2', F_DEF+F_CON, L_DEF, NoBB ),
    ('DfmNeck',            0, 'DfmSpine3', F_DEF+F_CON, L_DEF, (1,1,3) ),
]

BodyArmature4Simple = [
    ('Hip_L',             0, 'Hips', F_WIR, L_TWEAK, NoBB),
    ('Hip_R',             0, 'Hips', F_WIR, L_TWEAK, NoBB),
    ('Head',               0, 'Neck', F_WIR, L_UPSPN+L_DNSPN+L_HEAD, NoBB),
]

BodyArmature4Advanced = [
    ('Hip_L',             0, 'DfmHips', F_WIR, L_TWEAK, NoBB),
    ('Hip_R',             0, 'DfmHips', F_WIR, L_TWEAK, NoBB),
    ('Head',               0, 'DfmNeck', F_WIR, L_UPSPN+L_DNSPN+L_HEAD, NoBB),

    ('SpinePT'   ,         0, 'Shoulders', F_WIR, L_UPSPNIK, NoBB),
    ('SpineLinkPT',        0, 'Spine2', F_RES, L_UPSPNIK, NoBB),

    # Down spine
    ('DownNeck',           0, 'Shoulders', F_WIR, L_DNSPN, NoBB),
    ('DownSpine3',         0, 'Shoulders', F_WIR, L_DNSPNFK, NoBB),
    ('DownSpine2',         0, 'DownSpine3', F_WIR, L_DNSPNFK, NoBB),
    ('DownSpine1',         0, 'DownSpine2', F_WIR, L_DNSPNFK, NoBB),
    ('DownHips',           0, 'DownSpine1', F_WIR, L_DNSPN, NoBB),
    
    ('DownPT1',            0, 'DownSpine1', 0, L_HELP2, NoBB),
    ('DownPT2',            0, 'DownSpine2', 0, L_HELP2, NoBB),
    ('DownPT3',            0, 'DownSpine3', 0, L_HELP2, NoBB),

    #('DownSpinePT'   ,     0, 'Root', F_WIR, L_DNSPNIK, NoBB),
    #('DownSpineLinkPT',    0, 'DownSpine2', F_RES, L_DNSPNIK, NoBB),
]
 
BodyArmature5 = [
    ('DfmHead',            0, 'DfmNeck', F_DEF+F_CON, L_DEF, NoBB),

    # Stomach    
    ('DfmRib',             0, 'DfmSpine3', F_DEF, L_DEF, NoBB ),
    ('StomachTrg',         0, 'DfmHips', 0, L_HELP, NoBB),
    ('DfmStomach',         0, 'DfmRib', F_DEF+F_CON, L_DEF, (1,1,5) ),
    
    # Breast
    ('Breast_L',           -45*D, 'DfmSpine3', F_DEF+F_WIR, L_TWEAK, NoBB),
    ('Breast_R',           45*D, 'DfmSpine3', F_DEF+F_WIR, L_TWEAK, NoBB),
]
 

if MuscleBones:
    BodyArmature += [
    # Deform torso
    ('DfmRib',             0, 'DfmSpine3', F_DEF, L_DEF, NoBB),
    ('StomachPar',         0, 'DfmRib', 0, L_HELP, NoBB),
    ('DfmStomach1',        0, 'DfmRib', F_DEF+F_CON, L_DEF, (1,1,5) ),
    ('Stomach',            0, 'StomachPar', F_WIR, L_TWEAK, NoBB),
    ('DfmStomach2',        0, 'DfmStomach1', F_DEF+F_CON, L_DEF, (1,1,4) ),
    ('StomachTrg',         0, 'DfmHips', 0, L_HELP, NoBB),

    ('DfmWaist_L',         0, 'DfmRib', F_DEF, L_MSCL, NoBB),
    ('DfmWaist_R',         0, 'DfmRib', F_DEF, L_MSCL, NoBB),
    ('WaistTrg_L',         0, 'DfmHips', 0, L_HELP, NoBB),
    ('WaistTrg_R',         0, 'DfmHips', 0, L_HELP, NoBB),

    ('Pubis',              0, 'DfmHips', F_WIR+F_DEF, L_TWEAK+L_MSCL, NoBB ),
]

MaleArmature = [
    ('Penis1',             0, 'DfmHips', F_DEF+F_WIR, L_TWEAK+L_MSCL, NoBB ),
    ('Penis2',             0, 'Penis1', F_DEF+F_WIR+F_CON, L_TWEAK+L_MSCL, NoBB ),
    ('Scrotum',            0, 'DfmHips', F_DEF+F_WIR, L_TWEAK+L_MSCL, NoBB),
]

#
#    BodyControlPoses(fp, amt, config):
#

limHips = (-50*D,40*D, -45*D,45*D, -16*D,16*D)
limSpine1 = (-60*D,90*D, -60*D,60*D, -60*D,60*D)
limSpine2 = (-90*D,70*D, -20*D,20*D, -50*D,50*D)
limSpine3 = (-20*D,20*D, 0,0, -20*D,20*D)
limNeck = (-60*D,40*D, -45*D,45*D, -60*D,60*D)

def BodyControlPoses(fp, amt, config):
    addPoseBone(fp, amt,  'MasterFloor', 'GZM_Root', 'Master', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

    addPoseBone(fp, amt,  'Root', 'MHCrown', 'Master', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, 
        [('LimitRot', C_OW_LOCAL, 0, ['LimitRot', (0,0, -45*D,45*D, 0,0), (1,1,1)]) ])

    addPoseBone(fp, amt,  'Shoulders', 'MHCrown', 'Master', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0,
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (0,0, -45*D,45*D, 0,0), (1,1,1)]),
         #('LimitDist', 0, 1, ['LimitDist', 'Root', 'LIMITDIST_INSIDE'])
        ])

    # Up spine

    addPoseBone(fp, amt,  'Hips', 'GZM_CircleHips', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
         [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limHips, (1,1,1)])])

    addPoseBone(fp, amt,  'Pelvis', 'MHCircle15', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

    addPoseBone(fp, amt,  'Spine1', 'GZM_CircleSpine', 'Spine', (1,1,1), (0,0,0), (1,1,1), 
        ((1,1,1), (0.2,0.2,0.2), 0.05, None), 0, 
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limSpine1, (1,1,1)])])

    addPoseBone(fp, amt,  'Spine2', 'GZM_CircleSpine', 'Spine', (1,1,1), (0,0,0), (1,1,1), 
        ((1,1,1), (0.2,0.2,0.2), 0.05, None), 0,
        [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limSpine2, (1,1,1)])])

    addPoseBone(fp, amt,  'Spine3', 'GZM_CircleChest', 'Spine', (1,1,1), (0,0,0), (1,1,1), 
        ((1,1,1), (0.96,0.96,0.96), 0.01, None), 0,
         [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limSpine3, (1,1,1)]),
          ('IK', 0, 0, ['IK', 'Shoulders', 3, (-90*D, 'SpinePT'), (1,0,1)]),
         ])
         
    addPoseBone(fp, amt,  'Neck', 'MHNeck', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
         [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limNeck, (1,1,1)])])
         

    if config.advancedSpine:
        # Spine IK
        addPoseBone(fp, amt, 'SpinePT', 'MHCube025', 'Spine', (0,0,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

        addPoseBone(fp, amt, 'SpineLinkPT', None, 'Spine', (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
            [('StretchTo', 0, 1, ['Stretch', 'SpinePT', 0, 1])])

        # Down spine

        addPoseBone(fp, amt,  'DownHips', 'GZM_CircleHips', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
             [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limSpine1, (1,1,1)])])

        addPoseBone(fp, amt,  'DownSpine1', 'GZM_CircleInvSpine', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, 
            [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limSpine2, (1,1,1)])])

        addPoseBone(fp, amt,  'DownSpine2', 'GZM_CircleInvSpine', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, 
            [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limSpine3, (1,1,1)])])

        addPoseBone(fp, amt,  'DownSpine3', 'GZM_CircleInvChest', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, 
            [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limNeck, (1,1,1)]),
            ])
         
        addPoseBone(fp, amt,  'DownNeck', 'MHNeck', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
            [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limNeck, (1,1,1)])])
    
   
        # Deform spine    
        addPoseBone(fp, amt, 'DfmPelvis', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
          [('CopyLoc', 0, 1, ['UpLoc', 'Pelvis', (1,1,1), (0,0,0), False, False]),
           ('CopyRot', 0, 1, ['UpRot', 'Pelvis', (1,1,1), (0,0,0), False]),
           ('CopyLoc', 0, 0, ['DownLoc', 'DownHips', (1,1,1), (0,0,0), 1, False]),
           ('IK', 0, 0, ['DownIK', 'DownHips', 0, (-90*D, 'DownPT1'), (True, False,True)])
           ])
       
        addPoseBone(fp, amt, 'DfmHips', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
          [('CopyLoc', 0, 1, ['UpLoc', 'Hips', (1,1,1), (0,0,0), False, False]),
           ('CopyRot', 0, 1, ['UpRot', 'Hips', (1,1,1), (0,0,0), False]),
           ('CopyLoc', 0, 0, ['DownLoc', 'DownHips', (1,1,1), (0,0,0), 0, False]),
           ('CopyRot', 0, 0, ['DownRot', 'DownHips', (1,1,1), (0,0,0), False]) ])
       
        addPoseBone(fp, amt, 'DfmSpine1', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
          [('CopyLoc', 0, 1, ['UpLoc', 'Spine1', (1,1,1), (0,0,0), False, False]),
           ('CopyRot', 0, 1, ['UpRot', 'Spine1', (1,1,1), (0,0,0), False]),
           ('CopyLoc', 0, 0, ['DownLoc', 'DownSpine1', (1,1,1), (0,0,0), 1, False]),
           ('IK', 0, 0, ['DownIK', 'DownSpine1', 1, (-90*D, 'DownPT1'), (True, False,True)]),
           ('StretchTo', 0, 1, ['Stretch', 'Spine2', 0, 1]) ])

        addPoseBone(fp, amt, 'DfmSpine2', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
          [('CopyRot', 0, 1, ['UpRot', 'Spine2', (1,1,1), (0,0,0), False]),
           ('CopyLoc', 0, 0, ['DownLoc', 'DownSpine2', (1,1,1), (0,0,0), 1, False]),
           ('IK', 0, 0, ['DownIK', 'DownSpine2', 1, (-90*D, 'DownPT2'), (True, False,True)]),
           ('StretchTo', 0, 1, ['Stretch', 'Spine3', 0, 1]) ])

        addPoseBone(fp, amt, 'DfmSpine3', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
          [('CopyRot', 0, 1, ['UpRot', 'Spine3', (1,1,1), (0,0,0), False]),
           ('CopyLoc', 0, 0, ['DownLoc', 'DownSpine3', (1,1,1), (0,0,0), 1, False]),
           ('IK', 0, 0, ['DownIK', 'DownSpine3', 1, (-90*D, 'DownPT3'), (True, False,True)]) ])
        
        addPoseBone(fp, amt, 'DfmNeck', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
          [('CopyLoc', 0, 1, ['UpLoc', 'Neck', (1,1,1), (0,0,0), False, False]),
           ('CopyRot', 0, 1, ['UpRot', 'Neck', (1,1,1), (0,0,0), False]),
           ('CopyLoc', 0, 0, ['DownLoc', 'DownNeck', (1,1,1), (0,0,0), 0, False]),
           ('CopyRot', 0, 0, ['DownRot', 'DownNeck', (1,1,1), (0,0,0), False]) ])
           
    else:           
        # Deform spine    
        addPoseBone(fp, amt, 'DfmPelvis', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
          [('CopyTrans', 0, 1, ['CopyTrans', 'Pelvis', 0])])
       
        addPoseBone(fp, amt, 'DfmHips', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
          [('CopyTrans', 0, 1, ['CopyTrans', 'Hips', 0])])
       
        addPoseBone(fp, amt, 'DfmSpine1', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
          [('CopyTrans', 0, 1, ['CopyTrans', 'Spine1', 0])])

        addPoseBone(fp, amt, 'DfmSpine2', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
          [('CopyTrans', 0, 1, ['CopyTrans', 'Spine2', 0])])

        addPoseBone(fp, amt, 'DfmSpine3', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
          [('CopyTrans', 0, 1, ['CopyTrans', 'Spine3', 0])])           
        
        addPoseBone(fp, amt, 'DfmNeck', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
          [('CopyTrans', 0, 1, ['CopyTrans', 'Neck', 0])])
           

    # Head
    addPoseBone(fp, amt,  'Head', 'MHHead', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
         [('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-60*D,40*D, -60*D,60*D, -45*D,45*D), (1,1,1)])])

    addPoseBone(fp, amt, 'DfmHead', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0, 
         [('CopyTrans', 0, 1, ['CopyTrans', 'Head', 0])])
 
    addPoseBone(fp, amt,  'DfmStomach',None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'StomachTrg', 1, 1]),
        ])

    limBreastRot = (-45*D,45*D, -10*D,10*D, -20*D,20*D)
    limBreastScale =  (0.5,1.5, 0.2,2.0, 0.5,1.5)

    addPoseBone(fp, amt,  'Breast_L', 'MHEndCube01', None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0, [])

    addPoseBone(fp, amt,  'Breast_R', 'MHEndCube01', None, (0,0,0), (0,0,0), (0,0,0), (1,1,1), 0, [])

    if not MuscleBones:
        return

    # Stomach
    addPoseBone(fp, amt,  'Stomach', 'MHBall025', None, (0,0,0), (1,1,1), (0,0,0), (1,1,1), 0, [])

    addPoseBone(fp, amt,  'DfmStomach1',None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'Stomach', 0, 1]),
        ])

    addPoseBone(fp, amt,  'DfmStomach2',None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'StomachTrg', 1, 1]),
        ])

    addPoseBone(fp, amt,  'StomachPar',None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('StretchTo', 0, 0.5, ['Stretch', 'StomachTrg', 1, 1])])


    addPoseBone(fp, amt,  'DfmWaist_L',None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'WaistTrg_L', 0, 1])])

    addPoseBone(fp, amt,  'DfmWaist_R',None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'WaistTrg_R', 0, 1])])

    # Pubis
    
    addPoseBone(fp, amt,  'Pubis_R',None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
        [('StretchTo', 0, 1, ['Stretch', 'Pubis_L', 0, 1]),
        ])
    #print(amt.locations.keys())
    addPoseBone(fp, amt,  'Pubis', 'MHBall025', None, (0,0,0), (1,1,1), (0,0,0), (1,1,1), 0, 
        [('CopyLoc', 0, 1, ['MidPoint', 'Pubis_R', (1,1,1), (0,0,0), 0.5, False]),
        ])

    return

#
#   BodyDynamicLocations():    
#

def BodyDynamicLocations():    
    if not MuscleBones:
        return
    locs = amt.locations
    p = locs['pubis']
    x0 = locs['r-upper-leg']
    x1 = locs['r-upleg1']
    eps = (p[1]-x0[1])/(x1[1]-x0[1])
    locs['r-pubis'] = [ (1-eps)*x0[0]+eps*x1[0], p[1], p[2] ]
    x0 = locs['l-upper-leg']
    x1 = locs['l-upleg1']
    eps = (p[1]-x0[1])/(x1[1]-x0[1])
    locs['l-pubis'] = [ (1-eps)*x0[0]+eps*x1[0], p[1], p[2] ]
    return

#
#   MaleControlPoses(fp, amt):
#

def MaleControlPoses(fp, amt):
    addPoseBone(fp, amt,  'Penis1', 'MHCircle05', None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0, [])

    addPoseBone(fp, amt,  'Penis2', 'MHCircle05', None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0, [])

    addPoseBone(fp, amt,  'Scrotum', 'MHCircle05' , None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0, [])

    return

#
#   BodyPropDrivers
#   (Bone, Name, Props, Expr)
#

BodyPropDriversAdvanced = [
    ('DfmPelvis', 'UpRot', ['SpineInvert'], '1-x1'),
    ('DfmPelvis', 'UpLoc', ['SpineInvert'], '1-x1'),
    ('DfmPelvis', 'DownLoc', ['SpineInvert'], 'x1'),
    ('DfmPelvis', 'DownIK', ['SpineInvert'], 'x1'),

    ('DfmHips', 'UpRot', ['SpineInvert'], '1-x1'),
    ('DfmHips', 'UpLoc', ['SpineInvert'], '1-x1'),
    ('DfmHips', 'DownLoc', ['SpineInvert'], 'x1'),
    ('DfmHips', 'DownRot', ['SpineInvert'], 'x1'),

    ('DfmSpine1', 'Stretch', ['SpineIk', 'SpineInvert'], 'x1*(1-x2)'),
    ('DfmSpine1', 'UpLoc', ['SpineInvert'], '1-x1'),
    ('DfmSpine1', 'UpRot', ['SpineInvert'], '1-x1'),
    ('DfmSpine1', 'DownLoc', ['SpineInvert'], 'x1'),
    ('DfmSpine1', 'DownIK', ['SpineInvert'], 'x1'),

    ('DfmSpine2', 'Stretch', ['SpineIk', 'SpineInvert'], 'x1*(1-x2)'),
    ('DfmSpine2', 'UpRot', ['SpineInvert'], '1-x1'),
    ('DfmSpine2', 'DownLoc', ['SpineInvert'], 'x1'),
    ('DfmSpine2', 'DownIK', ['SpineInvert'], 'x1'),

    ('DfmSpine3', 'UpRot', ['SpineInvert'], '1-x1'),
    ('DfmSpine3', 'DownLoc', ['SpineInvert'], 'x1'),
    ('DfmSpine3', 'DownIK', ['SpineInvert'], 'x1'),

    ('DfmNeck', 'UpLoc', ['SpineInvert'], '1-x1'),
    ('DfmNeck', 'UpRot', ['SpineInvert'], '1-x1'),
    ('DfmNeck', 'DownLoc', ['SpineInvert'], 'x1'),
    ('DfmNeck', 'DownRot', ['SpineInvert'], 'x1'),

    ('Root', 'LimitRot', ['SpineInvert'], 'x1'),
    ('Shoulders', 'LimitRot', ['SpineInvert'], '1-x1'),
    #('Shoulders', 'LimitDist', ['SpineStretch', 'SpineInvert'], '(1-x1)*(1-x2)'),
    
    ('Spine3', 'IK', ['SpineIk', 'SpineInvert'], 'x1*(1-x2)'),

    ('DownHips', 'LimitRot', ['RotationLimits'], 'x1'),    
    ('DownSpine1', 'LimitRot', ['RotationLimits'], 'x1'),    
    ('DownSpine2', 'LimitRot', ['RotationLimits'], 'x1'),    
    ('DownSpine3', 'LimitRot', ['RotationLimits'], 'x1'),    
    ('DownNeck', 'LimitRot', ['RotationLimits'], 'x1'),    
]

BodyPropDrivers = [
    ('Hips', 'LimitRot', ['RotationLimits'], 'x1'),    
    ('Spine1', 'LimitRot', ['RotationLimits'], 'x1'),    
    ('Spine2', 'LimitRot', ['RotationLimits'], 'x1'),    
    ('Spine3', 'LimitRot', ['RotationLimits'], 'x1'),    
    ('Neck', 'LimitRot', ['RotationLimits'], 'x1'),    
    ('Head', 'LimitRot', ['RotationLimits'], 'x1'),    
]

if MuscleBones:
    BodyPropDrivers += [    
    ('Pubis', 'MidPoint', ['FreePubis'], '1-x1'),
]

#
#   BodyShapes
#

BodyShapes = [ 
    'Breathe' 
]

#
#    BodyShapeKeyScale = {
#

BodyShapeKeyScale = {
    'Breathe'            : ('spine1', 'neck', 1.89623),
}

BodySpines = [
    ('Spine', ['Spine1IK', 'Spine2IK', 'Spine3IK', 'Spine4IK', 'Shoulders'])
]




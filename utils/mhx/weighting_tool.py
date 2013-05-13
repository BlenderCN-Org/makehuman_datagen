""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         GPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
Bone weighting utility

"""

bl_info = {
    "name": "Weighting Tools",
    "author": "Thomas Larsson",
    "version": "1.0",
    "blender": (2, 6, 5),
    "location": "View3D > Properties > MH Weighting Tools",
    "description": "MakeHuman Utilities",
    "warning": "",
    'wiki_url': "http://www.makehuman.org",
    "category": "MakeHuman"}

#
#
#

import bpy, os, mathutils
import math
from mathutils import *
from bpy.props import *

NBodyVertices = 15340

def getFaces(me):
    try:
        return me.polygons
    except:
        return me.faces
    
#
#    printVertNums(context):
#    class VIEW3D_OT_PrintVnumsButton(bpy.types.Operator):
#
 
class VIEW3D_OT_PrintVnumsButton(bpy.types.Operator):
    bl_idname = "mhw.print_vnums"
    bl_label = "Print vnums"

    def execute(self, context):
        ob = context.object
        print("Verts in ", ob)
        for v in ob.data.vertices:
            if v.select:
                print("  ", v.index)
        print("End")
        return{'FINISHED'}    
     

class VIEW3D_OT_PrintVnumsToFileButton(bpy.types.Operator):
    bl_idname = "mhw.print_vnums_to_file"
    bl_label = "Print Vnums To File"

    def execute(self, context):
        ob = context.object
        scn = context.scene
        path = os.path.expanduser(scn.MhxVertexGroupFile)
        fp = open(path, "w")
        fp.write("  [")
        for v in ob.data.vertices:
            if v.select:
                fp.write("%d, " % v.index)
        fp.write("]\n")
        fp.close()
        print(path, "written")
        return{'FINISHED'}    
        
        
class VIEW3D_OT_ReadVNumsButton(bpy.types.Operator):
    bl_idname = "mhw.read_vnums_from_file"
    bl_label = "Read Vnums from file"
    bl_options = {'UNDO'}

    def execute(self, context):
        scn = context.scene
        ob = context.object
        path = os.path.expanduser(scn.MhxVertexGroupFile)
        fp = open(path, "rU")
        for line in fp:
            try:
                vn = int(line)
            except:
                vn = -1
            if vn >= 0:
                ob.data.vertices[vn].select = True
        fp.close()
        return {'FINISHED'}

     
def printFirstVertNum(context):
    ob = context.object
    print("First vert in ", ob)
    for v in ob.data.vertices:
        if v.select:
            print("  ", v.index)
            return
    print("None found")

class VIEW3D_OT_PrintFirstVnumButton(bpy.types.Operator):
    bl_idname = "mhw.print_first_vnum"
    bl_label = "Print first vnum"

    def execute(self, context):
        printFirstVertNum(context)
        return{'FINISHED'}    
              

#
#    selectVertNum8m(context):
#    class VIEW3D_OT_SelectVnumButton(bpy.types.Operator):
#
 
def selectVertNum(context):
    n = context.scene.MhxVertNum
    ob = context.object
    bpy.ops.object.mode_set(mode='OBJECT')
    for v in ob.data.vertices:
        v.select = False
    v = ob.data.vertices[n]
    v.select = True
    bpy.ops.object.mode_set(mode='EDIT')

class VIEW3D_OT_SelectVnumButton(bpy.types.Operator):
    bl_idname = "mhw.select_vnum"
    bl_label = "Select vnum"
    bl_options = {'UNDO'}

    def execute(self, context):
        selectVertNum(context)
        return{'FINISHED'}    

#
#    printEdgeNums(context):
#    class VIEW3D_OT_PrintEnumsButton(bpy.types.Operator):
#
 
def printEdgeNums(context):
    ob = context.object
    print("Edges in ", ob)
    for e in ob.data.edges:
        if e.select:
            print(e.index)
    print("End")

class VIEW3D_OT_PrintEnumsButton(bpy.types.Operator):
    bl_idname = "mhw.print_enums"
    bl_label = "Print enums"

    def execute(self, context):
        printEdgeNums(context)
        return{'FINISHED'}    
#
#    printFaceNums(context):
#    class VIEW3D_OT_PrintFnumsButton(bpy.types.Operator):
#
 
def printFaceNums(context):
    ob = context.object
    print("Faces in ", ob)
    for f in ob.data.faces:
        if f.select:
            print(f.index)
    print("End")

class VIEW3D_OT_PrintFnumsButton(bpy.types.Operator):
    bl_idname = "mhw.print_fnums"
    bl_label = "Print fnums"

    def execute(self, context):
        printFaceNums(context)
        return{'FINISHED'}    

#
#    selectQuads():
#    class VIEW3D_OT_SelectQuadsButton(bpy.types.Operator):
#

def selectQuads(context):
    ob = context.object
    for f in ob.data.faces:
        if len(f.vertices) == 4:
            f.select = True
        else:
            f.select = False
    return

class VIEW3D_OT_SelectQuadsButton(bpy.types.Operator):
    bl_idname = "mhw.select_quads"
    bl_label = "Select quads"
    bl_options = {'UNDO'}

    def execute(self, context):
        import bpy
        selectQuads(context)
        print("Quads selected")
        return{'FINISHED'}    

#
#    removeVertexGroups(context):
#    class VIEW3D_OT_RemoveVertexGroupsButton(bpy.types.Operator):
#

def removeVertexGroups(context):
    ob = context.object
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.vertex_group_remove(all=True)
    return

class VIEW3D_OT_RemoveVertexGroupsButton(bpy.types.Operator):
    bl_idname = "mhw.remove_vertex_groups"
    bl_label = "Unvertex all"
    bl_options = {'UNDO'}

    def execute(self, context):
        removeVertexGroups(context)
        print("All vertex groups removed")
        return{'FINISHED'}    

#
#
#

class VIEW3D_OT_IntegerVertexGroupsButton(bpy.types.Operator):
    bl_idname = "mhw.integer_vertex_groups"
    bl_label = "Integer vertex groups"
    bl_options = {'UNDO'}

    def execute(self, context):
        ob = context.object
        for v in ob.data.vertices:
            wmax = -1
            best = None
            for g in v.groups:
                if g.weight > wmax:
                    wmax = g.weight
                    best = g.group
            if not best:
                continue
            for g in v.groups:
                if g.group == best:
                    g.weight = 1
                else:
                    g.weight = 0
        print("Integer vertex groups done")
        return{'FINISHED'}    

#
#
#

def copyVertexGroups(scn, src, trg):
    print("Copy vertex groups %s => %s" % (src.name, trg.name))
    scn.objects.active = trg
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.vertex_group_remove(all=True)
    groups = {}
    for sgrp in src.vertex_groups:
        tgrp = trg.vertex_groups.new(name=sgrp.name)
        groups[sgrp.index] = tgrp
    for vs in src.data.vertices:
        for g in vs.groups:            
            tgrp = groups[g.group]
            tgrp.add([vs.index], g.weight, 'REPLACE')
    return

class VIEW3D_OT_CopyVertexGroupsButton(bpy.types.Operator):
    bl_idname = "mhw.copy_vertex_groups"
    bl_label = "Copy vgroups active => selected"
    bl_options = {'UNDO'}

    def execute(self, context):
        src = context.object
        scn = context.scene
        for ob in scn.objects:
            if ob.type == 'MESH' and ob != src:
                trg = ob
                break
        copyVertexGroups(scn, src, trg)
        print("Vertex groups copied")
        return{'FINISHED'}    
        
#
#
#

def mergeVertexGroups(scn, ob):
    vgroups = []
    for n in range(5):
        vg = scn["MhxVG%d" % n]
        if vg:
            vgroups.append(vg)
        else:
            break
    if not vgroups:
        return
    print("Merging", vgroups)
    tgrp = ob.vertex_groups[vgroups[0]]
    groups = []
    for vg in vgroups:
        groups.append( ob.vertex_groups[vg].index )
    for v in ob.data.vertices:
        w = 0
        for g in v.groups:
            if g.group in groups:
                w += g.weight
        if w > 1e-4:
            tgrp.add([v.index], w, 'REPLACE')
    for vgname in vgroups[1:]:
        vg = ob.vertex_groups[vgname]
        print("Remove", vg)
        ob.vertex_groups.remove(vg)
    return        
   
class VIEW3D_OT_MergeVertexGroupsButton(bpy.types.Operator):
    bl_idname = "mhw.merge_vertex_groups"
    bl_label = "Merge vertex groups"
    bl_options = {'UNDO'}

    def execute(self, context):
        mergeVertexGroups(context.scene, context.object)
        print("Vertex groups merged")
        return{'FINISHED'}    
   

#
#    unVertexDiamonds(context):
#    class VIEW3D_OT_UnvertexDiamondsButton(bpy.types.Operator):
#

def unVertexDiamonds(context):
    ob = context.object
    print("Unvertex diamonds in %s" % ob)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    me = ob.data
    faces = getFaces(me)
    for f in faces:        
        if len(f.vertices) < 4:
            for vn in f.vertices:
                me.vertices[vn].select = True
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.object.vertex_group_remove_from(all=True)
    bpy.ops.object.mode_set(mode='OBJECT')
    return

class VIEW3D_OT_UnvertexDiamondsButton(bpy.types.Operator):
    bl_idname = "mhw.unvertex_diamonds"
    bl_label = "Unvertex diamonds"
    bl_options = {'UNDO'}

    def execute(self, context):
        unVertexDiamonds(context)
        print("Diamonds unvertexed")
        return{'FINISHED'}    

class VIEW3D_OT_UnvertexSelectedButton(bpy.types.Operator):
    bl_idname = "mhw.unvertex_selected"
    bl_label = "Unvertex selected"
    bl_options = {'UNDO'}

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.object.vertex_group_remove_from(all=True)
        bpy.ops.object.mode_set(mode='OBJECT')
        print("Selected unvertexed")
        return{'FINISHED'}    

#
#
#

class VIEW3D_OT_MultiplyWeightsButton(bpy.types.Operator):
    bl_idname = "mhw.multiply_weights"
    bl_label = "Multiply weights"
    bl_options = {'UNDO'}

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT')    
        bpy.ops.wm.context_set_value(data_path="tool_settings.mesh_select_mode", value="(True,False,False)")
        bpy.ops.object.mode_set(mode='OBJECT')
        ob = context.object
        factor = context.scene.MhxWeight
        index = ob.vertex_groups.active_index
        for v in ob.data.vertices:
            if v.select:
                print(v, index)
                for g in v.groups:
                    if g.group == index:
                        g.weight *= factor                   
        bpy.ops.object.mode_set(mode='EDIT')    
        bpy.ops.wm.context_set_value(data_path="tool_settings.mesh_select_mode", value="(False,True,False)")
        print("Weights multiplied")
        return{'FINISHED'}    

#
#    deleteDiamonds(context)
#    Delete joint diamonds in main mesh
#    class VIEW3D_OT_DeleteDiamondsButton(bpy.types.Operator):
#

def deleteDiamonds(context):
    ob = context.object
    print("Delete diamonds in %s" % bpy.context.object)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    me = ob.data
    for f in me.faces:        
        if len(f.vertices) < 4:
            for vn in f.vertices:
                me.vertices[vn].select = True
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.object.mode_set(mode='OBJECT')
    return
    
class VIEW3D_OT_DeleteDiamondsButton(bpy.types.Operator):
    bl_idname = "mhw.delete_diamonds"
    bl_label = "Delete diamonds"
    bl_options = {'UNDO'}

    def execute(self, context):
        deleteDiamonds(context)
        print("Diamonds deleted")
        return{'FINISHED'}    
    

#
#    pairWeight(context):
#

def findGroupPairs(context):
    ob = context.object
    scn = context.scene
    name1 = scn['MhxBone1']
    name2 = scn['MhxBone2']
    weight = scn['MhxWeight']
    group1 = None
    group2 = None
    for vgrp in ob.vertex_groups:
        if vgrp.name == name1:
            group1 = vgrp
        if vgrp.name == name2:
            group2 = vgrp
    if not (group1 and group2):            
        raise NameError("Did not find vertex groups %s or %s" % (name1, name2))
    return (group1, group2)
    
    
def pairWeight(context):
    ob = context.object
    (group1, group2) = findGroupPairs(context)
    index1 = group1.index
    index2 = group2.index
    for v in ob.data.vertices:
        if v.select:
            for grp in v.groups:
                if grp.index == index1:
                    grp.weight = weight
                elif grp.index == index2:
                    grp.weight = 1-weight
                else:
                    ob.remove_from_group(grp, v.index)
    return


class VIEW3D_OT_PairWeightButton(bpy.types.Operator):
    bl_idname = "mhw.pair_weight"
    bl_label = "Weight pair"
    bl_options = {'UNDO'}

    def execute(self, context):
        pairWeight(context)
        return{'FINISHED'}    


def rampWeight(context):
    ob = context.object
    (group1, group2) = findGroupPairs(context)
    xmin = 1e6
    xmax = -1e6
    for v in ob.data.vertices:
        if v.select:
            x = v.co[0]
            if x < xmin: xmin = x
            if x > xmax: xmax = x
    factor = 1/(xmax-xmin)            
    for v in ob.data.vertices:
        if v.select:
            x = v.co[0]
            w = factor*(x-xmin)
            group1.add([v.index], 1-w, 'REPLACE')
            group2.add([v.index], w, 'REPLACE')
    return


class VIEW3D_OT_RampWeightButton(bpy.types.Operator):
    bl_idname = "mhw.ramp_weight"
    bl_label = "Weight ramp"
    bl_options = {'UNDO'}

    def execute(self, context):
        rampWeight(context)
        return{'FINISHED'}    


def createLeftRightGroups(context):
    ob = context.object
    left = ob.vertex_groups.new(name="Left")
    right = ob.vertex_groups.new(name="Right")
    xmax = 0.1
    factor = 1/(2*xmax)
    for v in ob.data.vertices:
        w = factor*(v.co[0]+xmax)
        if w > 1:
            left.add([v.index], 1, 'REPLACE')
        elif w < 0:
            right.add([v.index], 1, 'REPLACE')
        else:
            left.add([v.index], w, 'REPLACE')
            right.add([v.index], 1-w, 'REPLACE')
    return


class VIEW3D_OT_CreateLeftRightButton(bpy.types.Operator):
    bl_idname = "mhw.create_left_right"
    bl_label = "Create Left Right"
    bl_options = {'UNDO'}

    def execute(self, context):
        createLeftRightGroups(context)
        return{'FINISHED'}    


#----------------------------------------------------------
#   setupVertexPairs(ob):
#----------------------------------------------------------

def setupVertexPairs(context):
    ob = context.object
    scn = context.scene
    verts = []
    for v in ob.data.vertices:
        x = v.co[0]
        y = v.co[1]
        z = v.co[2]
        verts.append((z,y,x,v.index))
    verts.sort()        
    lverts = {}
    rverts = {}
    mverts = {}
    nmax = len(verts)
    notfound = []
    for n,data in enumerate(verts):
        (z,y,x,vn) = data
        n1 = n - 20
        n2 = n + 20
        if n1 < 0: n1 = 0
        if n2 >= nmax: n2 = nmax
        vmir = findVert(verts[n1:n2], vn, -x, y, z, notfound, scn)
        if vmir < 0:
            mverts[vn] = vn
        elif x > scn.MhxEpsilon:
            rverts[vn] = vmir
        elif x < -scn.MhxEpsilon:
            lverts[vn] = vmir
        else:
            mverts[vn] = vmir
    if notfound:            
        print("Did not find mirror image for vertices:")        
        for data in notfound:
            print("  %d at (%.4f %.4f %.4f) mindist %.4f" % tuple(data))
    print("Left-right-mid", len(lverts.keys()), len(rverts.keys()), len(mverts.keys()))
    return (lverts, rverts, mverts)
    
def findVert(verts, v, x, y, z, notfound, scn):
    mindist = 1e6
    for (z1,y1,x1,v1) in verts:
        dx = x-x1
        dy = y-y1
        dz = z-z1
        dist = math.sqrt(dx*dx + dy*dy + dz*dz)
        if dist < scn.MhxEpsilon:
            return v1
        if dist < mindist:
            mindist = dist
    if abs(x) > scn.MhxEpsilon:            
        notfound.append((v, x, y, z, mindist))
    return -1                    

#
#    symmetrizeWeights(context):
#    class VIEW3D_OT_SymmetrizeWeightsButton(bpy.types.Operator):
#

def symmetrizeWeights(context, left2right):
    ob = context.object
    bpy.ops.object.mode_set(mode='OBJECT')
    scn = context.scene

    left = {}
    left01 = {}
    left02 = {}
    leftIndex = {}
    left01Index = {}
    left02Index = {}
    right = {}
    right01 = {}
    right02 = {}
    rightIndex = {}
    right01Index = {}
    right02Index = {}
    symm = {}
    symmIndex = {}
    for vgrp in ob.vertex_groups:
        if vgrp.name[-2:] in ['_L', '.L', '_l', '.l']:
            nameStripped = vgrp.name[:-2]
            left[nameStripped] = vgrp
            leftIndex[vgrp.index] = nameStripped
        elif vgrp.name[-2:] in ['_R', '.R', '_r', '.r']:
            nameStripped = vgrp.name[:-2]
            right[nameStripped] = vgrp
            rightIndex[vgrp.index] = nameStripped
        elif vgrp.name[-4:].lower() == 'left':
            nameStripped = vgrp.name[:-4]
            left[nameStripped] = vgrp
            leftIndex[vgrp.index] = nameStripped
        elif vgrp.name[-5:].lower() == 'right':
            nameStripped = vgrp.name[:-5]
            right[nameStripped] = vgrp
            rightIndex[vgrp.index] = nameStripped
        elif vgrp.name[-5:] in ['.L.01', '.l.01']:
            nameStripped = vgrp.name[:-5]
            left01[nameStripped] = vgrp
            left01Index[vgrp.index] = nameStripped
        elif vgrp.name[-5:] in ['.R.01', '.r.01']:
            nameStripped = vgrp.name[:-5]
            right01[nameStripped] = vgrp
            right01Index[vgrp.index] = nameStripped
        elif vgrp.name[-5:] in ['.L.02', '.l.02']:
            nameStripped = vgrp.name[:-5]
            left02[nameStripped] = vgrp
            left02Index[vgrp.index] = nameStripped
        elif vgrp.name[-5:] in ['.R.02', '.r.02']:
            nameStripped = vgrp.name[:-5]
            right02[nameStripped] = vgrp
            right02Index[vgrp.index] = nameStripped
        else:
            symm[vgrp.name] = vgrp
            symmIndex[vgrp.index] = vgrp.name

    printGroups('Left', left, leftIndex, ob.vertex_groups)
    printGroups('Right', right, rightIndex, ob.vertex_groups)
    printGroups('Left01', left01, left01Index, ob.vertex_groups)
    printGroups('Right01', right01, right01Index, ob.vertex_groups)
    printGroups('Left02', left02, left02Index, ob.vertex_groups)
    printGroups('Right02', right02, right02Index, ob.vertex_groups)
    printGroups('Symm', symm, symmIndex, ob.vertex_groups)

    (lverts, rverts, mverts) = setupVertexPairs(context)
    if left2right:
        factor = 1
        fleft = left
        fright = right
        groups = list(right.values()) + list(right01.values()) + list(right02.values())
        cleanGroups(ob.data, groups)
    else:
        factor = -1
        fleft = right
        fright = left
        rverts = lverts
        groups = list(left.values()) + list(left01.values()) + list(left02.values())
        cleanGroups(ob.data, groups)

    for (vn, rvn) in rverts.items():
        v = ob.data.vertices[vn]
        rv = ob.data.vertices[rvn]
        #print(v.index, rv.index)
        for rgrp in rv.groups:
            rgrp.weight = 0
        for grp in v.groups:
            rgrp = None
            for (indices, groups) in [
                (leftIndex, right), (rightIndex, left),
                (left01Index, right01), (right01Index, left01),
                (left02Index, right02), (right02Index, left02),
                (symmIndex, symm)
                ]:
                try:
                    name = indices[grp.group]
                    rgrp = groups[name]
                except:
                    pass
            if rgrp:
                #print("  ", name, grp.group, rgrp.name, rgrp.index, v.index, rv.index, grp.weight)
                rgrp.add([rv.index], grp.weight, 'REPLACE')
            else:                
                gn = grp.group
                print("*** No rgrp for %s %s %s" % (grp, gn, ob.vertex_groups[gn]))
    return len(rverts)

def printGroups(name, groups, indices, vgroups):
    print(name)
    for (nameStripped, grp) in groups.items():
        print("  ", nameStripped, grp.name, indices[grp.index])
    return

def cleanGroups(me, groups):
    for grp in groups:
        print(grp)
        for v in me.vertices:
            grp.remove([v.index])
    return
    
class VIEW3D_OT_SymmetrizeWeightsButton(bpy.types.Operator):
    bl_idname = "mhw.symmetrize_weights"
    bl_label = "Symmetrize weights"
    bl_options = {'UNDO'}
    left2right = BoolProperty()

    def execute(self, context):
        import bpy
        n = symmetrizeWeights(context, self.left2right)
        print("Weights symmetrized, %d vertices" % n)
        return{'FINISHED'}    
        
#
#    cleanRight(context, doRight):
#    class VIEW3D_OT_CleanRightButton(bpy.types.Operator):
#

def cleanRight(context, doRight):
    ob = context.object
    bpy.ops.object.mode_set(mode='OBJECT')
    (lverts, rverts, mverts) = setupVertexPairs(context)
    for vgrp in ob.vertex_groups:
        if doRight:
            if vgrp.name[-2:] in ['_L', '.L', '_l', '.l']:
                for (vn, rvn) in rverts.items():
                    vgrp.remove([rvn])
        else:                    
            if vgrp.name[-2:] in ['_R', '.R', '_r', '.r']:
                for (vn, rvn) in rverts.items():
                    vgrp.remove([vn])
    return

class VIEW3D_OT_CleanRightButton(bpy.types.Operator):
    bl_idname = "mhw.clean_right"
    bl_label = "Clean right"
    bl_options = {'UNDO'}
    doRight = BoolProperty()

    def execute(self, context):
        cleanRight(context, self.doRight)
        return{'FINISHED'}    

#
#    symmetrizeShapes(context, left2right):
#    class VIEW3D_OT_SymmetrizeShapesButton(bpy.types.Operator):
#

def symmetrizeShapes(context, left2right):
    ob = context.object
    bpy.ops.object.mode_set(mode='OBJECT')
    scn = context.scene
    (lverts, rverts, mverts) = setupVertexPairs(context)
    if not left2right:
        rverts = lverts

    for key in ob.data.shape_keys.key_blocks:
        print(key.name)
        for rvn in rverts.values():
            rv = ob.data.vertices[rvn]
            key.data[rv.index].co = rv.co

        for v in ob.data.vertices:
            try:
                rvn = rverts[v.index]
            except:
                rvn = None
            if rvn:
                lco = key.data[v.index].co
                rco = lco.copy()
                rco[0] = -rco[0]
                key.data[rvn].co = rco

    return len(rverts)

class VIEW3D_OT_SymmetrizeShapesButton(bpy.types.Operator):
    bl_idname = "mhw.symmetrize_shapes"
    bl_label = "Symmetrize shapes"
    bl_options = {'UNDO'}
    left2right = BoolProperty()

    def execute(self, context):
        n = symmetrizeShapes(context, self.left2right)
        print("Shapes symmetrized, %d vertices" % n)
        return{'FINISHED'}    


def symmetrizeVerts(context, left2right):
    ob = context.object
    bpy.ops.object.mode_set(mode='OBJECT')
    scn = context.scene
    (lverts, rverts, mverts) = setupVertexPairs(context)
    if not left2right:
        rverts = lverts
                
    for v in ob.data.vertices:
        try:
            rvn = rverts[v.index]
        except KeyError:
            rvn = None
        if rvn:
            rco = v.co.copy()
            rco[0] = -rco[0]
            print(rvn, ob.data.vertices[rvn].co, rco)
            ob.data.vertices[rvn].co = rco
            print("   ", ob.data.vertices[rvn].co)

    return len(rverts)


class VIEW3D_OT_SymmetrizeVertsButton(bpy.types.Operator):
    bl_idname = "mhw.symmetrize_verts"
    bl_label = "Symmetrize verts"
    bl_options = {'UNDO'}
    left2right = BoolProperty()

    def execute(self, context):
        n = symmetrizeVerts(context, self.left2right)
        print("Verts symmetrized, %d vertices" % n)
        return{'FINISHED'}    

#
#    shapekeyFromObject(ob, targ):
#    class VIEW3D_OT_ShapeKeysFromObjectsButton(bpy.types.Operator):
#

def shapekeyFromObject(ob, targ):
    verts = ob.data.vertices
    tverts = targ.data.vertices
    print("Create shapekey %s" % targ.name)
    print(len(verts), len(tverts))
    if len(verts) != len(tverts):
        print("%s and %s do not have the same number of vertices" % (ob, targ))
        return
    if not ob.data.shape_keys:
        ob.shape_key_add(name='Basis', from_mix=False)
    skey = ob.shape_key_add(name=targ.name, from_mix=False)
    for n,v in enumerate(verts):
        vt = tverts[n].co
        pt = skey.data[n].co
        pt[0] = vt[0]
        pt[1] = vt[1]
        pt[2] = vt[2]
    print("Shape %s created" % skey)
    return    

class VIEW3D_OT_ShapeKeysFromObjectsButton(bpy.types.Operator):
    bl_idname = "mhw.shapekeys_from_objects"
    bl_label = "Shapes from objects"
    bl_options = {'UNDO'}

    def execute(self, context):
        import bpy
        ob = context.object
        for targ in context.scene.objects:
            if targ.type == 'MESH' and targ.select and targ != ob:
                shapekeyFromObject(ob, targ)
        print("Shapekeys created for %s" % ob)
        return{'FINISHED'}    

#
#
#


def symmetrizeSelection(context, left2right):
    ob = context.object
    bpy.ops.object.mode_set(mode='OBJECT')
    scn = context.scene
    (lverts, rverts, mverts) = setupVertexPairs(context)
    if not left2right:
        rverts = lverts
    for (vn, rvn) in rverts.items():
        v = ob.data.vertices[vn]
        rv = ob.data.vertices[rvn]
        rv.select = v.select
    return            


class VIEW3D_OT_SymmetrizeSelectionButton(bpy.types.Operator):
    bl_idname = "mhw.symmetrize_selection"
    bl_label = "Symmetrize Selection"
    bl_options = {'UNDO'}
    left2right = BoolProperty()

    def execute(self, context):
        symmetrizeSelection(context, self.left2right)
        print("Selection symmetrized")
        return{'FINISHED'}    

#
#    recoverDiamonds(context):
#    class VIEW3D_OT_RecoverDiamondsButton(bpy.types.Operator):
#

def recoverDiamonds(context):
    ob = context.object
    for dob in context.scene.objects:
        if dob.select and dob.type == 'MESH' and dob != ob:
            break
    if not dob:
        raise NameError("Need two selected meshes")

    if len(dob.data.vertices) < len(ob.data.vertices):
        tmp = dob
        dob = ob
        ob = tmp

    vdiamond = {}
    for v in dob.data.vertices:
        vdiamond[v.index] = False
    dfaces = getFaces(dob.data)
    for f in dfaces:
        if len(f.vertices) < 4:
            for vn in f.vertices:
                vdiamond[vn] = True

    vassoc = {}
    vedges = {}
    vfaces = {}
    vn = 0  
    for dv in dob.data.vertices:
        vedges[dv.index] = []
        vfaces[dv.index] = []
        if not vdiamond[dv.index]:
            vassoc[vn] = dv.index
            vn += 1

    for de in dob.data.edges:
        de.use_seam = False
        de.select = False
        dvn0 = de.vertices[0]
        vedges[dvn0].append(de)
        dvn1 = de.vertices[1]
        vedges[dvn1].append(de)
        
    for df in dfaces:
        for dvn in df.vertices:
            vfaces[dvn].append(df)

    for e in ob.data.edges:
        dvn0 = vassoc[e.vertices[0]]
        dvn1 = vassoc[e.vertices[1]]
        for de in vedges[dvn0]:
            if dvn1 in de.vertices:
                de.select = e.use_seam
                de.use_seam = e.use_seam
                #if e.use_seam:
                #    print(e.index, de.index)
                break
     
    faces = getFaces(ob.data)
    for f in faces:        
        dverts = []
        for vn in f.vertices:
            dverts.append(vassoc[vn])            
        for df in vfaces[dverts[0]]:
            for dvn in dverts:
                if dvn not in df.vertices:
                    continue            
            df.material_index = f.material_index   
            print(f.index, df.index, df.material_index)
            break
        
    context.scene.objects.active = dob

    bpy.ops.object.vertex_group_remove(all=True)

    for grp in ob.vertex_groups:
        group = dob.vertex_groups.new(grp.name)
        index = group.index
        for v in ob.data.vertices:    
            for vgrp in v.groups:
                if vgrp.group == index:
                    dn = vassoc[v.index]
                    #dob.vertex_groups.assign( [dn], group, vgrp.weight, 'REPLACE' )
                    group.add( [dn], vgrp.weight, 'REPLACE' )
                    continue

    print("Diamonds recovered")
    return
    

class VIEW3D_OT_RecoverDiamondsButton(bpy.types.Operator):
    bl_idname = "mhw.recover_diamonds"
    bl_label = "Recover diamonds"
    bl_options = {'UNDO'}

    def execute(self, context):
        recoverDiamonds(context)
        return{'FINISHED'}    

#
#    exportVertexGroups(filePath)
#    class VIEW3D_OT_ExportVertexGroupsButton(bpy.types.Operator):
#

def sortVertexGroups(ob):
    rig = ob.parent
    if True or not rig:
        return ob.vertex_groups

    roots = []
    for bone in rig.data.bones:
        if not bone.parent:
            roots.append(bone)
    
    vgroups = []
    for root in roots:
        vgroups += sortBoneVGroups(root, ob)
    return vgroups
    
    
def sortBoneVGroups(bone, ob):  
    try:
        vgroups = [ob.vertex_groups[bone.name]]
    except KeyError:
        vgroups = []
    for child in bone.children:
        vgroups += sortBoneVGroups(child, ob)
    return vgroups
    
        
def exportVertexGroups(context):
    scn = context.scene
    filePath = scn.MhxVertexGroupFile
    exportAllVerts = not scn.MhxExportSelectedOnly
    fileName = os.path.expanduser(filePath)
    fp = open(fileName, "w")
    ob = context.object
    me = ob.data
    vgroups = sortVertexGroups(ob)
    for vg in vgroups:
        index = vg.index
        weights = []
        for v in me.vertices:
            if exportAllVerts or v.select:
                for grp in v.groups:
                    if grp.group == index and grp.weight > 0.005:
                        weights.append((v.index, grp.weight))    
        exportList(context, weights, vg.name, fp)
    fp.close()
    print("Vertex groups exported to %s" % fileName)
    return

class VIEW3D_OT_ExportVertexGroupsButton(bpy.types.Operator):
    bl_idname = "mhw.export_vertex_groups"
    bl_label = "Export vertex groups"
    bl_options = {'UNDO'}

    def execute(self, context):
        exportVertexGroups(context)
        return{'FINISHED'}    


def exportLeftRight(context):
    scn = context.scene
    filePath = scn.MhxVertexGroupFile
    fileName = os.path.expanduser(filePath)
    fp = open(fileName, "w")
    ob = context.object
    eps = 0.07
    left = []
    right = []
    for v in ob.data.vertices:
        if v.co[0] > eps:
            left.append((v.index, 1.0))
        elif v.co[0] < -eps:
            right.append((v.index, 1.0))
        else:
            w = (v.co[0] + eps)/(2*eps)
            left.append((v.index, w))
            right.append((v.index, 1-w))
    exportList(context, left, "Left", fp)
    exportList(context, right, "Right", fp)
    fp.close()
    print("Left-right vertex groups exported to %s" % fileName)
    return

            
class VIEW3D_OT_ExportLeftRightButton(bpy.types.Operator):
    bl_idname = "mhw.export_left_right"
    bl_label = "Export Left/Right Vertex Groups"
    bl_options = {'UNDO'}

    def execute(self, context):
        exportLeftRight(context)
        return{'FINISHED'}    

#
#    exportSumGroups(context):
#    exportListAsVertexGroup(weights, name, fp):
#    class VIEW3D_OT_ExportSumGroupsButton(bpy.types.Operator):
#

def exportSumGroups(context):
    filePath = context.scene.MhxVertexGroupFile
    fileName = os.path.expanduser(filePath)
    fp = open(fileName, "w")
    ob = context.object
    me = ob.data
    for name in ['UpArm', 'LoArm', 'UpLeg']:
        for suffix in ['_L', '_R']:
            weights = {}
            for n in range(1,4):
                vg = ob.vertex_groups["%s%d%s" % (name, n, suffix)]
                index = vg.index
                for v in me.vertices:
                    for grp in v.groups:
                        if grp.group == index:
                            try:
                                w = weights[v.index]
                            except:
                                w = 0
                            weights[v.index] = grp.weight + w
                # ob.vertex_groups.remove(vg)
            exportList(context, weights.items(), name+'3'+suffix, fp)
    fp.close()
    return

def exportList(context, weights, name, fp):
    print("EL", name)
    if len(weights) == 0:
        return
    scn = context.scene
    offset = scn.MhxVertexOffset        
    if scn.MhxExportAsWeightFile:
        if len(weights) > 0:
            fp.write("\n# weights %s\n" % name)
            for (vn,w) in weights:
                if w > 0.005:
                    fp.write("  %d %.3g\n" % (vn+offset, w))
    else:
        fp.write("\n  VertexGroup %s\n" % name)
        for (vn,w) in weights:
            if w > 0.005:
                fp.write("    wv %d %.3g ;\n" % (vn+offset, w))
        fp.write("  end VertexGroup %s\n" % name)
    return

class VIEW3D_OT_ExportSumGroupsButton(bpy.types.Operator):
    bl_idname = "mhw.export_sum_groups"
    bl_label = "Export sum groups"
    bl_options = {'UNDO'}

    def execute(self, context):
        exportSumGroups(context)
        return{'FINISHED'}    

#
#    exportShapeKeys(filePath)
#    class VIEW3D_OT_ExportShapeKeysButton(bpy.types.Operator):
#

def exportShapeKeys(context):
    scn = context.scene
    filePath = context.scene.MhxVertexGroupFile
    fileName = os.path.expanduser(filePath)
    fp = open(fileName, "w")
    ob = context.object
    me = ob.data
    lr = "Sym"
    for skey in me.shape_keys.key_blocks:
        name = skey.name.replace(' ','_')    
        if name == "Basis":
            continue
        print(name)
        fp.write("  ShapeKey %s %s True\n" % (name, lr))
        fp.write("    slider_min %.2f ;\n" % skey.slider_min)
        fp.write("    slider_max %.2f ;\n" % skey.slider_max)
        for (n,pt) in enumerate(skey.data):
           vert = me.vertices[n]
           dv = pt.co - vert.co
           if dv.length > scn.MhxEpsilon:
               fp.write("    sv %d %.4f %.4f %.4f ;\n" %(n, dv[0], dv[1], dv[2]))
        fp.write("  end ShapeKey\n")
        print(skey)
    fp.close()
    print("Shape keys exported to %s" % fileName)
    return

class VIEW3D_OT_ExportShapeKeysButton(bpy.types.Operator):
    bl_idname = "mhw.export_shapekeys"
    bl_label = "Export shapekeys"
    bl_options = {'UNDO'}

    def execute(self, context):
        exportShapeKeys(context)
        return{'FINISHED'}    

#
#   listVertPairs(context):
#   class VIEW3D_OT_ListVertPairsButton(bpy.types.Operator):
#

def listVertPairs(context):
    scn = context.scene
    filePath = scn.MhxVertexGroupFile
    fileName = os.path.expanduser(filePath)
    print("Open %s" % fileName)
    fp = open(fileName, "w")
    ob = context.object
    verts = []
    for v in ob.data.vertices:
        if v.select:
            verts.append((v.co[2], v.index))
    verts.sort()
    nmax = int(len(verts)/2)
    fp.write("Pairs = (\n")
    for n in range(nmax):
        (z1, vn1) = verts[2*n]
        (z2, vn2) = verts[2*n+1]
        v1 = ob.data.vertices[vn1]
        v2 = ob.data.vertices[vn2]
        x1 = v1.co[0]
        y1 = v1.co[1]
        x2 = v2.co[0]
        y2 = v2.co[1]
        print("%d (%.4f %.4f %.4f)" % (v1.index, x1,y1,z1))
        print("%d (%.4f %.4f %.4f)\n" % (v2.index, x2,y2,z2))
        if ((abs(z1-z2) > scn.MhxEpsilon) or
            (abs(x1+x2) > scn.MhxEpsilon) or
            (abs(y1-y2) > scn.MhxEpsilon)):
            raise NameError("Verts %d and %d not a pair:\n  %s\n  %s\n" % (v1.index, v2.index, v1.co, v2.co))
        if x1 > x2:
            fp.write("    (%d, %d),\n" % (v1.index, v2.index))            
        else:
            fp.write("    (%d, %d),\n" % (v2.index, v1.index))            
    fp.write(")\n")
    fp.close()
    print("Wrote %s" % fileName)
    return

class VIEW3D_OT_ListVertPairsButton(bpy.types.Operator):
    bl_idname = "mhw.list_vert_pairs"
    bl_label = "List vert pairs"
    bl_options = {'UNDO'}

    def execute(self, context):
        listVertPairs(context)
        return{'FINISHED'}    
                   
#
#
#


def joinMeshes(context):
    scn = context.scene
    base = context.object
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    clothes = []
    for ob in context.selected_objects:
        if ob != base and ob.type == 'MESH':
            clothes.append(ob)
            scn.objects.active = ob            
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    print("Joining %s to %s" % (clothes, base))            

    verts = []
    faces = []    
    texfaces = []
    v0 = appendStuff(base, 0, verts, faces, texfaces)
    for clo in clothes:
        v0 = appendStuff(clo, v0, verts, faces, texfaces)
    me = bpy.data.meshes.new("NewBase")
    me.from_pydata(verts, [], faces)

    uvtex = me.uv_textures.new(name = "UVTex")
    for n,tf in enumerate(texfaces):
        print(n, tf)
        uvtex.data[n].uv = tf        
    ob = bpy.data.objects.new("NewBase", me)
    scn.objects.link(ob)
    scn.objects.active = ob
    print("Meshes joined")
    
    
    return
             
def appendStuff(ob, v0, verts, faces, texfaces):                
    for v in ob.data.vertices:
        verts.append(v.co)
    for f in ob.data.faces:
        face = []
        for vn in f.vertices:
            face.append(vn + v0)
        faces.append(face)
    v0 += len(ob.data.vertices)    
    
    if ob.data.uv_textures:
        uvtex = ob.data.uv_textures[0]
        for f in ob.data.faces:
            tf = uvtex.data[f.index].uv
            texfaces.append(tf)
    else:
        x0 = 0.99
        y0 = 0.99
        x1 = 1.0
        y1 = 1.0
        for f in ob.data.faces:
            tf = ((x0,y0),(x0,y1),(x1,y0),(x1,y1))
            texfaces.append(tf)                
    print("Done %s %d verts" % (ob.name, v0))
    return v0

class VIEW3D_OT_JoinMeshesButton(bpy.types.Operator):
    bl_idname = "mhw.join_meshes"
    bl_label = "Join meshes"
    bl_options = {'UNDO'}

    def execute(self, context):
        joinMeshes(context)
        return{'FINISHED'}    
                 
#                 
#   fixBaseFile():
#

the3dobjFolder = "C:/home/svn/data/3dobjs"

def baseFileGroups():    
    fp = open(os.path.join(the3dobjFolder, "base0.obj"), "rU")
    grp = None
    grps = {}
    fn = 0
    for line in fp:
        words = line.split()
        if words[0] == "f":
            grps[fn] = grp
            fn += 1
        elif words[0] == "g":
            grp = words[1]
    fp.close()
    return grps
    
def fixBaseFile():
    grps = baseFileGroups()
    infp = open(os.path.join(the3dobjFolder, "base1.obj"), "rU")
    outfp = open(os.path.join(the3dobjFolder, "base2.obj"), "w")
    fn = 0
    grp = None
    for line in infp:
        words = line.split()
        if words[0] == "f":
            try:
                fgrp = grps[fn]
            except:
                fgrp = None
            if fgrp != grp:
                grp = fgrp
                outfp.write("g %s\n" % grp)
            fn += 1
        outfp.write(line)
    infp.close()
    outfp.close()
    print("Base file fixed")
    return

class VIEW3D_OT_FixBaseFileButton(bpy.types.Operator):
    bl_idname = "mhw.fix_base_file"
    bl_label = "Fix base file"

    def execute(self, context):
        fixBaseFile()
        return{'FINISHED'}    
        
        
#
#    class CProxy
#

class CProxy:
    def __init__(self):
        self.refVerts = []
        self.firstVert = 0
        return
        
    def setWeights(self, verts, grp):
        rlen = len(self.refVerts)
        mlen = len(verts)
        first = self.firstVert
        if (first+rlen) != mlen:
            raise NameError( "Bug: %d refVerts != %d meshVerts" % (first+rlen, mlen) )
        gn = grp.index
        for n in range(rlen):
            vert = verts[n+first]
            refVert = self.refVerts[n]
            if type(refVert) == tuple:
                (rv0, rv1, rv2, w0, w1, w2, d0, d1, d2) = refVert
                vw0 = CProxy.getWeight(verts[rv0], gn)
                vw1 = CProxy.getWeight(verts[rv1], gn)
                vw2 = CProxy.getWeight(verts[rv2], gn)
                vw = w0*vw0 + w1*vw1 + w2*vw2
            else:
                vw = getWeight(verts[refVert], gn)
            grp.add([vert.index], vw, 'REPLACE')
        return

    def cornerWeights(self, vn):
        n = vn - self.firstVert
        refVert = self.refVerts[n]
        if type(refVert) == tuple:
            (rv0, rv1, rv2, w0, w1, w2, d0, d1, d2) = refVert
            return [(w0,rv0), (w1,rv1), (w2,rv2)]
        else:
            return [(1,refVert)]
        
    def getWeight(vert, gn):
        for grp in vert.groups:
            if grp.group == gn:
                return grp.weight
        return 0             
        
    def read(self, filepath):
        realpath = os.path.realpath(os.path.expanduser(filepath))
        folder = os.path.dirname(realpath)
        try:
            tmpl = open(filepath, "rU")
        except:
            tmpl = None
        if tmpl == None:
            print("*** Cannot open %s" % realpath)
            return None

        status = 0
        doVerts = 1
        vn = 0
        for line in tmpl:
            words= line.split()
            if len(words) == 0:
                pass
            elif words[0] == '#':
                status = 0
                if len(words) == 1:
                    pass
                elif words[1] == 'verts':
                    if len(words) > 2:
                        self.firstVert = int(words[2])                    
                    status = doVerts
                else:
                    pass
            elif status == doVerts:
                if len(words) == 1:
                    v = int(words[0])
                    self.refVerts.append(v)
                else:                
                    v0 = int(words[0])
                    v1 = int(words[1])
                    v2 = int(words[2])
                    w0 = float(words[3])
                    w1 = float(words[4])
                    w2 = float(words[5])            
                    d0 = float(words[6])
                    d1 = float(words[7])
                    d2 = float(words[8])
                    self.refVerts.append( (v0,v1,v2,w0,w1,w2,d0,d1,d2) )
        return
        
#
#   class VIEW3D_OT_ProjectMaterialsButton(bpy.types.Operator):
#

from random import random

class VIEW3D_OT_ProjectMaterialsButton(bpy.types.Operator):
    bl_idname = "mhw.project_materials"
    bl_label = "Project materials from proxy"

    def execute(self, context):
        ob = context.object
        proxy = CProxy()
        proxy.read(os.path.join(the3dobjFolder, "base.mhclo"))
        grps = baseFileGroups()
        grpList = set(grps.values())
        grpIndices = {}
        grpNames = {}
        n = 0
        for grp in grpList:
            mat = bpy.data.materials.new(grp)
            ob.data.materials.append(mat)
            mat.diffuse_color = (random(), random(), random())
            grpIndices[grp] = n
            grpNames[n] = grp
            n += 1
        
        vertFaces = {}
        for v in ob.data.vertices:
            vertFaces[v.index] = []
        
        for f in ob.data.faces:
            for vn in f.vertices:
                vertFaces[vn].append(f)
                if vn >= proxy.firstVert:
                    grp = None
                    continue
                grp = grps[f.index]
            if grp:
                f.material_index = grpIndices[grp]
        
        for f in ob.data.faces:
            if f.vertices[0] >= proxy.firstVert:
                cwts = []
                for vn in f.vertices:
                    cwts += proxy.cornerWeights(vn)
                cwts.sort()
                cwts.reverse()
                (w,vn) = cwts[0]
                for f1 in vertFaces[vn]:
                    mn = f1.material_index
                    f.material_index = f1.material_index                
                    continue

        print("Material projected from proxy")
        return{'FINISHED'}    

#
#   class VIEW3D_OT_ProjectWeightsButton(bpy.types.Operator):
#

class VIEW3D_OT_ProjectWeightsButton(bpy.types.Operator):
    bl_idname = "mhw.project_weights"
    bl_label = "Project weights from proxy"

    def execute(self, context):
        ob = context.object
        proxy = CProxy()
        proxy.read(os.path.join(the3dobjFolder, "base.mhclo"))
        for grp in ob.vertex_groups:
            print(grp.name)
            proxy.setWeights(ob.data.vertices, grp)
        print("Weights projected from proxy")
        return{'FINISHED'}    

#
#   exportObjFile(context):
#   setupTexVerts(ob, scn):
#

def exportObjFile(context):
    fp = open(os.path.join(the3dobjFolder, "base3.obj"), "w")
    scn = context.scene
    me = context.object.data
    for v in me.vertices:
        fp.write("v %.4f %.4f %.4f\n" % (v.co[0], v.co[2], -v.co[1]))
        
    for v in me.vertices:
        fp.write("vn %.4f %.4f %.4f\n" % (v.normal[0], v.normal[2], -v.normal[1]))
        
    if me.uv_textures:
        (uvFaceVerts, texVerts, nTexVerts) = setupTexVerts(me, scn)
        for vtn in range(nTexVerts):
            vt = texVerts[vtn]
            fp.write("vt %.4f %.4f\n" % (vt[0], vt[1]))
        n = 1
        mn = -1
        for f in me.faces:
            if f.material_index != mn:
                mn = f.material_index
                fp.write("g %s\n" % me.materials[mn].name)
            uvVerts = uvFaceVerts[f.index]
            fp.write("f ")
            for n,v in enumerate(f.vertices):
                (vt, uv) = uvVerts[n]
                fp.write("%d/%d " % (v+1, vt+1))
            fp.write("\n")
    else:
        for f in me.faces:
            fp.write("f ")
            for vn in f.vertices:
                fp.write("%d " % (vn+1))
            fp.write("\n")

    fp.close()
    print("base3.obj written")
    return
    
def setupTexVerts(me, scn):
    vertEdges = {}
    vertFaces = {}
    for v in me.vertices:
        vertEdges[v.index] = []
        vertFaces[v.index] = []
    for e in me.edges:
        for vn in e.vertices:
            vertEdges[vn].append(e)
    for f in me.faces:
        for vn in f.vertices:
            vertFaces[vn].append(f)
    
    edgeFaces = {}
    for e in me.edges:
        edgeFaces[e.index] = []
    faceEdges = {}
    for f in me.faces:
        faceEdges[f.index] = []
    for f in me.faces:
        for vn in f.vertices:
            for e in vertEdges[vn]:
                v0 = e.vertices[0]
                v1 = e.vertices[1]
                if (v0 in f.vertices) and (v1 in f.vertices):
                    if f not in edgeFaces[e.index]:
                        edgeFaces[e.index].append(f)
                    if e not in faceEdges[f.index]:
                        faceEdges[f.index].append(e)
        
    faceNeighbors = {}
    uvFaceVerts = {}
    for f in me.faces:
        faceNeighbors[f.index] = []
        uvFaceVerts[f.index] = []
    for f in me.faces:
        for e in faceEdges[f.index]:
            for f1 in edgeFaces[e.index]:
                if f1 != f:
                    faceNeighbors[f.index].append((e,f1))

    uvtex = me.uv_textures[0]
    vtn = 0
    texVerts = {}    
    for f in me.faces:
        uvf = uvtex.data[f.index]
        vtn = findTexVert(uvf.uv1, vtn, f, faceNeighbors, uvFaceVerts, texVerts, scn)
        vtn = findTexVert(uvf.uv2, vtn, f, faceNeighbors, uvFaceVerts, texVerts, scn)
        vtn = findTexVert(uvf.uv3, vtn, f, faceNeighbors, uvFaceVerts, texVerts, scn)
        if len(f.vertices) > 3:
            vtn = findTexVert(uvf.uv4, vtn, f, faceNeighbors, uvFaceVerts, texVerts, scn)
    return (uvFaceVerts, texVerts, vtn)     

def findTexVert(uv, vtn, f, faceNeighbors, uvFaceVerts, texVerts, scn):
    for (e,f1) in faceNeighbors[f.index]:
        for (vtn1,uv1) in uvFaceVerts[f1.index]:
            vec = uv - uv1
            if vec.length < scn.MhxEpsilon:
                uvFaceVerts[f.index].append((vtn1,uv))                
                return vtn
    uvFaceVerts[f.index].append((vtn,uv))
    texVerts[vtn] = uv
    return vtn+1
    
class VIEW3D_OT_ExportBaseObjButton(bpy.types.Operator):
    bl_idname = "mhw.export_base_obj"
    bl_label = "Export base3.obj"

    def execute(self, context):
        exportObjFile(context)
        return{'FINISHED'}    
    
                 
#
#    initInterface(context):
#    class VIEW3D_OT_InitInterfaceButton(bpy.types.Operator):
#

def initInterface(context):
    bpy.types.Scene.MhxEpsilon = FloatProperty(
        name="Epsilon", 
        description="Maximal distance for identification", 
        default=1.0e-3,
        min=0, max=1)

    bpy.types.Scene.MhxVertNum = IntProperty(
        name="Vert number", 
        description="Vertex number to select")

    bpy.types.Scene.MhxWeight = FloatProperty(
        name="Weight", 
        description="Weight of bone1, 1-weight of bone2", 
        default=1.0,
        min=0, max=1)

    bpy.types.Scene.MhxBone1 = StringProperty(
        name="Bone 1", 
        maxlen=40,
        default='Bone1')

    bpy.types.Scene.MhxBone2 = StringProperty(
        name="Bone 2", 
        maxlen=40,
        default='Bone2')

    bpy.types.Scene.MhxExportAsWeightFile = BoolProperty(
        name="Export as weight file", 
        default=False)

    bpy.types.Scene.MhxExportSelectedOnly = BoolProperty(
        name="Export selected verts only", 
        default=False)

    bpy.types.Scene.MhxVertexOffset = IntProperty(
        name="Offset", 
        default=0,
        description="Export vertex numbers with offset")

    bpy.types.Scene.MhxVertexGroupFile = StringProperty(
        name="Vertex group file", 
        maxlen=100,
        default="/home/vgroups.txt")


    bpy.types.Scene.MhxVG0 = StringProperty(name="MhxVG0", maxlen=40, default='')
    bpy.types.Scene.MhxVG1 = StringProperty(name="MhxVG1", maxlen=40, default='')
    bpy.types.Scene.MhxVG2 = StringProperty(name="MhxVG2", maxlen=40, default='')
    bpy.types.Scene.MhxVG3 = StringProperty(name="MhxVG3", maxlen=40, default='')
    bpy.types.Scene.MhxVG4 = StringProperty(name="MhxVG4", maxlen=40, default='')

    return

#
#   class VIEW3D_OT_LocalizeFilesButton(bpy.types.Operator):
#

def localizeFile(context, path):
    print("Localizing", path)
    ob = context.object
    lines = []

    fp = open(path, "r")
    for line in fp:
        words = line.split()
        vn = int(words[0])
        v = ob.data.vertices[vn]
        if v.select:
            lines.append(line)
        else:
            print(line)
    fp.close()
    
    fp = open(path, "w")
    for line in lines:
        fp.write(line)
    fp.close()
    
    return
    
    
def localizeFiles(context, path):
    print("Local files in ", path)
    folder = os.path.dirname(path)
    for file in os.listdir(folder):
        (fname, ext) = os.path.splitext(file)
        if ext == ".target":
            localizeFile(context, os.path.join(folder, file))


class VIEW3D_OT_LocalizeFilesButton(bpy.types.Operator):
    bl_idname = "mhw.localize_files"
    bl_label = "Localize Files"
    bl_options = {'UNDO'}

    filename_ext = ".target"
    filter_glob = StringProperty(default="*.target", options={'HIDDEN'})
    filepath = bpy.props.StringProperty(
        name="File Path", 
        maxlen= 1024, default= "")

    def execute(self, context):
        print("Exec localize files")
        localizeFiles(context, self.properties.filepath)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

#
#
#

class VIEW3D_OT_StatisticsButton(bpy.types.Operator):
    bl_idname = "mhw.statistics"
    bl_label = "Statistics"

    def execute(self, context):
        ob = context.object
        rig = ob.parent
        if ob.type == 'MESH':
            uvs = ob.data.uv_layers[0]
            print(
                "# Verts: %d\n" % len(ob.data.vertices) +
                "# Faces: %d\n" % len(ob.data.polygons) +
                "# UVs: %d %g\n" % (len(uvs.data), len(uvs.data)/2.0)
                )
        if rig and rig.type == 'ARMATURE':
            print(
                "# Bones: %d\n" % len(rig.data.bones)
                )
        return{'FINISHED'}    

#
#
#

VertexNumbers = {}

VertexNumbers["alpha8a"] = {
    "Tongue"    : (0,226),
    "Body"      : (226, 13606),
    "Hair"      : (13606, 14034),
    "Skirt"     : (14034, 14754),
    "Tights"    : (14754, 17428),
    "Penis"     : (17428, 17628),
    "EyeLashes" : (17628, 17878),
    "Eyes"      : (17878, 18022),
    "LoTeeth"   : (18022, 18090),
    "UpTeeth"   : (18090, 18158),
    "Joints"     : (18158, 19166)
}        

VertexNumbers["alpha8b"] = {
    "Body"      : (0, 13380),
    "Tongue"    : (13380, 13606),
    "Joints"    : (13606, 14614),
    "Eyes"      : (14614, 14758),
    "EyeLashes" : (14758, 15008),
    "LoTeeth"   : (15008, 15076),
    "UpTeeth"   : (15076, 15144),
    "Penis"     : (15144, 15344),
    "Tights"    : (15344, 18018),
    "Skirt"     : (18018, 18738),
    "Hair"      : (18738, 19166),
}


def transferVgroups(ob1, ob2):
    if len(ob1.vertex_groups) == 0:
        tmp = ob1
        ob1 = ob2
        ob2 = tmp
    print(ob1, ob1.vertex_groups)        
    print(ob2, ob2.vertex_groups)        
    if len(ob1.vertex_groups) == 0:
        raise NameError("%s has no vertex groups" % ob1)
    if len(ob2.vertex_groups) > 0:
        raise NameError("%s has vertex groups" % ob2)
    
    vgroups = {}
    for vg1 in ob1.vertex_groups:
        vg2 = ob2.vertex_groups.new(vg1.name)
        vgroups[vg1.index] = vg2
        if vg2.index != vg1.index:
            raise NameError("Oops %s %d %d" % (vg1.name, vg1.index, vg2.index))
    
    for v1 in ob1.data.vertices:
        vn2 = getVertex(v1.index)
        for g1 in v1.groups:
            vg2 = vgroups[g1.group]
            vg2.add([vn2], g1.weight, 'REPLACE')


def getVertex(vn1):
    vstruct1 = VertexNumbers["alpha8a"]
    for key in vstruct1:
        first1,last1 = vstruct1[key]
        if vn1 >= first1 and vn1 < last1:
            break

    vstruct2 = VertexNumbers["alpha8b"]
    first2,last2 = vstruct2[key]
    vn2 = vn1 - first1 + first2
    return vn2
    

def checkVgroupSanity():
    vstruct1 = VertexNumbers["alpha8a"]
    vstruct2 = VertexNumbers["alpha8b"]
    for key in vstruct1:
        first1,last1 = vstruct1[key]
        first2,last2 = vstruct2[key]
        nverts1 = last1-first1
        nverts2 = last2-first2
        if nverts1 == nverts2:
            print("    ", key)
        else:
            print("*** %s %d %d" % (key, nverts1, nverts2))
            
   
    
class VIEW3D_OT_TransferVgroupsButton(bpy.types.Operator):
    bl_idname = "mhw.transfer_vgroups"
    bl_label = "Transfer Vertex Groups"

    def execute(self, context):
        checkVgroupSanity()
        ob1 = context.object
        scn = context.scene
        for ob in scn.objects:
            if ob.type == 'MESH' and ob != ob1 and ob.select:
                ob2 = ob
                break
        transferVgroups(ob1, ob2)
        return{'FINISHED'}    


class VIEW3D_OT_CheckVgroupsSanityButton(bpy.types.Operator):
    bl_idname = "mhw.check_vgroups_sanity"
    bl_label = "Check Vertex Group Sanity"

    def execute(self, context):
        checkVgroupSanity()
        return{'FINISHED'}    
    
#
#    class MhxWeightToolsPanel(bpy.types.Panel):
#

class MhxWeightToolsPanel(bpy.types.Panel):
    bl_label = "Weight tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == 'MESH'

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        
        layout.label("Mesh Stats")
        layout.operator("mhw.print_vnums")
        layout.operator("mhw.print_first_vnum")
        layout.operator("mhw.print_enums")
        layout.operator("mhw.print_fnums")
        layout.operator("mhw.select_quads")
        layout.prop(scn, 'MhxVertNum')
        layout.operator("mhw.select_vnum")
        
        layout.separator()
        layout.label("Vertex Groups And Diamonds")
        layout.operator("mhw.unvertex_selected")
        layout.operator("mhw.unvertex_diamonds")
        layout.operator("mhw.delete_diamonds")
        layout.operator("mhw.recover_diamonds")
        layout.operator("mhw.integer_vertex_groups")
        layout.operator("mhw.copy_vertex_groups")
        layout.operator("mhw.remove_vertex_groups")

        layout.separator()
        layout.label("Symmetrization")
        layout.prop(scn, "MhxEpsilon")
        row = layout.row()
        row.label("Weights")
        row.operator("mhw.symmetrize_weights", text="L=>R").left2right = True
        row.operator("mhw.symmetrize_weights", text="R=>L").left2right = False

        row = layout.row()
        row.label("Clean")
        row.operator("mhw.clean_right", text="Right side of left vgroups").doRight = True
        row.operator("mhw.clean_right", text="Left side of right vgroups").doRight = False

        row = layout.row()
        row.label("Shapes")
        row.operator("mhw.symmetrize_shapes", text="L=>R").left2right = True    
        row.operator("mhw.symmetrize_shapes", text="R=>L").left2right = False

        #row = layout.row()
        #row.label("Verts")
        #row.operator("mhw.symmetrize_verts", text="L=>R").left2right = True    
        #row.operator("mhw.symmetrize_verts", text="R=>L").left2right = False    

        row = layout.row()
        row.label("Selection")
        row.operator("mhw.symmetrize_selection", text="L=>R").left2right = True    
        row.operator("mhw.symmetrize_selection", text="R=>L").left2right = False

        layout.separator()
        layout.label("Export")
        layout.prop(scn, 'MhxVertexGroupFile', text="File")
        row = layout.row()
        row.prop(scn, 'MhxExportAsWeightFile', text="As Weight File")
        row.prop(scn, 'MhxExportSelectedOnly', text="Selected Only")
        row.prop(scn, 'MhxVertexOffset', text="Offset")
        layout.operator("mhw.export_vertex_groups")    
        layout.operator("mhw.export_left_right")    
        layout.operator("mhw.export_sum_groups")    
        layout.operator("mhw.print_vnums_to_file")
        layout.operator("mhw.read_vnums_from_file")

        layout.separator()
        layout.operator("mhw.localize_files")
        layout.operator("mhw.transfer_vgroups")
        layout.operator("mhw.check_vgroups_sanity")
        
        
        

class MhxWeightExtraPanel(bpy.types.Panel):
    bl_label = "Weight tools extra"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == 'MESH'

       
    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.operator("mhw.statistics")    

        layout.prop(scn, "MhxVG0")
        layout.prop(scn, "MhxVG1")
        layout.prop(scn, "MhxVG2")
        layout.prop(scn, "MhxVG3")
        layout.prop(scn, "MhxVG4")
        layout.operator("mhw.merge_vertex_groups")

        layout.operator("mhw.list_vert_pairs")            

        layout.separator()
        layout.operator("mhw.shapekeys_from_objects")    
        layout.operator("mhw.export_shapekeys")    

        layout.label('Weight pair')
        layout.prop(context.scene, 'MhxWeight')
        layout.operator("mhw.multiply_weights")
        layout.prop(context.scene, 'MhxBone1')
        layout.prop(context.scene, 'MhxBone2')
        layout.operator("mhw.pair_weight")
        layout.operator("mhw.ramp_weight")
        layout.operator("mhw.create_left_right")        
        
        layout.label("Helper construction")
        layout.operator("mhw.join_meshes")
        layout.operator("mhw.fix_base_file")
        layout.operator("mhw.project_weights")
        layout.operator("mhw.project_materials")
        layout.operator("mhw.export_base_obj")

#
#    Init and register
#

initInterface(bpy.context)

def register():
    bpy.utils.register_module(__name__)
    pass

def unregister():
    bpy.utils.unregister_module(__name__)
    pass

if __name__ == "__main__":
    register()



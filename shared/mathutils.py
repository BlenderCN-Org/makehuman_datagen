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
Blender API mockup

"""

from math import *
import numpy as np
import numpy.linalg as la
import transformations as tm

#------------------------------------------------------------------
#   Data types
#------------------------------------------------------------------

def round(x):
    if abs(x) < 1e-4:
        return 0
    else:
        return x
        
#class Vector:
#   def __init__(self, vec):
#        self.vector = np.array(vec)

class Vector:
    def __init__(self, vec):
        if isinstance(vec, Vector):
            vec = vec.vector
        self.vector = np.array(vec)
        
    def __repr__(self):
        string = "<Vector"
        for elt in self.vector:
            string += (" %.4g" % round(elt))
        return string + ">"
        
    def __len__(self):
        return len(self.vector)
        
    def __getitem__(self, n):
        return self.vector[n]
        
    def __setitem__(self, n, value):
        self.vector[n] = value
        
    def __add__(self, vec):
        return Vector(self.vector + vec.vector)
        
    def __sub__(self, vec):
        return Vector(self.vector - vec.vector)
        
    def dot(self, vec):
        return np.dot(self.vector, vec.vector)
        
    def __rmul__(self, factor):
        return Vector(factor*self.vector)

    def __mul__(self, factor):
        return Vector(factor*self.vector)

    def __div__(self, denom):
        return Vector(self.vector/denom)
        
    def cross(self, vec):
        return Vector(np.cross(self.vector, vec.vector))
        
    def getLength(self):
        return sqrt(np.dot(self.vector, self.vector))
        
    def setLength(self):
        pass
  
    length = property(getLength, setLength)
    
        
        

class Matrix:        
    def __init__(self, data=None):
        if data is None:
            self.size = 4
            self.matrix = np.identity(4,float)
        else:
            self.size = len(data)
            self.matrix = np.array(data)    

    def __repr__(self):
        string = "<Matrix"
        for i in range(self.size):
            row = "\n      "
            for j in range(self.size):
                row += (" %.4g" % round(self.matrix[i,j]))
            string += row
        return string + ">"
        
    def __len__(self):
        return len(self.size)
        
    def __getitem__(self, n):
        return self.matrix[n,:]
        
    def __setitem__(self, n, value):
        self.matrix[n,:] = value
        
    def transposed(self):
        return Matrix(self.matrix.transpose())
   
    def inverted(self):
        return Matrix(la.inv(self.matrix))
        
    def mult(self, mat):
        return Matrix(np.dot(self.matrix, mat.matrix))
    
    def to_3x3(self):
        return Matrix(3, self.matrix[:3,:3])        
        
    def to_4x4(self):
        mat = Matrix(4)
        mat[:3,:3] = self.matrix[:3,:3]
        return mat        
        
    def decompose(self):
        loc = Vector(self.matrix[:3,3])
        rot = Matrix(self.matrix[:3,:3])
        scale = Vector(self.matrix[3,:3])
        return (loc,rot,scale)
                
    def compose(self, loc, rot, scale):
        mat = Matrix()
        if loc:
            mat.matrix[:3,3] = loc.vector
        if rot:
            mat.matrix[:3,:3] = rot.matrix[:3,:3]
        if scale:
            mat.matrix[3,:3] = scale.vector
        return mat

    def to_euler(self):
        return tm.euler_from_matrix(self.matrix)
    
    def to_quaternion(self):
        return tm.quaternion_from_matrix(self.matrix)
    
        
    Axis = {
        'X' : (1,0,0),
        'Y' : (0,1,0),
        'Z' : (0,0,1),
    }
    
    @classmethod
    def Rotation(self, angle, dim, axis):
        self.size = dim
        mat = tm.rotation_matrix(angle, Matrix.Axis[axis])
        if dim == 3:
            self.matrix = mat[:3,:3]
        else:
            self.matrix = mat

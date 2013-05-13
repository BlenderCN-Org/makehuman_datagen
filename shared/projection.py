#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers, Glynn Clements

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

Methods that help create texture maps by projection on the model.
Supported creators:
Light map creator
Image map creator
UV map creator

"""

import numpy as np
import gui3d
import mh
import log
import matrix
import scene
import image_operations

def v4to3(v): #unused.
    v = np.asarray(v)
    return v[:3,0] / v[3:,0]

def vnorm(v):
    return v / np.sqrt(np.sum(v ** 2, axis=-1))[...,None]

class Shader(object):
    pass

class UvAlphaShader(Shader):
    def __init__(self, dst, texture, uva):
        self.dst = dst
        self.texture = texture
        self.size = np.array([texture.width, texture.height])
        self.uva = uva

    def shade(self, i, xy, uvw):
        dst = self.dst.data[xy[...,1],xy[...,0]]
        uva = np.sum(self.uva[i][None,None,:,:] * uvw[...,[1,2,0]][:,:,:,None], axis=2)
        ix = np.floor(uva[:,:,:2] * self.size[None,None,:]).astype(int)
        ix = np.minimum(ix, self.size - 1)
        ix = np.maximum(ix, 0)
        src = self.texture.data[ix[...,1], ix[...,0]]
        a = uva[:,:,2]
        return a[:,:,None] * (src.astype(float) - dst) + dst

class ColorShader(Shader):
    def __init__(self, colors):
        self.colors = colors

    def shade(self, i, xy, uvw):
        return np.sum(self.colors[i][None,None,:,:] * uvw[...,[1,2,0]][:,:,:,None], axis=2)

def RasterizeTriangles(dst, coords, shader, progress = None):
    """
    Software rasterizer.
    """
    delta = coords - coords[:,[1,2,0],:]
    perp = np.concatenate((delta[:,:,1,None], -delta[:,:,0,None]), axis=-1)
    dist = np.sum(perp[:,0,:] * delta[:,2,:], axis=-1)
    perp /= dist[:,None,None]
    base = np.sum(perp * coords, axis=-1)

    cmin = np.floor(np.amin(coords, axis=1)).astype(int)
    cmax = np.ceil( np.amax(coords, axis=1)).astype(int)

    minx = cmin[:,0]
    maxx = cmax[:,0]
    miny = cmin[:,1]
    maxy = cmax[:,1]

    for i in xrange(len(coords)):
        if progress is not None and i % 100 == 0:
            progress(i, len(coords))

        ixy = np.mgrid[miny[i]:maxy[i],minx[i]:maxx[i]].transpose([1,2,0])[:,:,::-1]
        xy = ixy + 0.5
        uvw = np.sum(perp[i,None,None,:,:] * xy[:,:,None,:], axis=-1) - base[i,None,None,:]
        mask = np.all(uvw > 0, axis=-1)
        col = shader.shade(i, ixy, uvw)
        # log.debug('dst: %s', dst.data[miny[i]:maxy[i],minx[i]:maxx[i]].shape)
        # log.debug('src: %s', col.shape)
        dst.data[miny[i]:maxy[i],minx[i]:maxx[i],:][mask] = col[mask]

def getCamera(mesh):
    ex, ey, ez = gui3d.app.modelCamera.eye
    eye = np.matrix([ex,ey,ez,1]).T
    fx, fy, fz = gui3d.app.modelCamera.focus
    focus = np.matrix([fx,fy,fz,1]).T
    transform = mesh.transform.I
    eye = v4to3(transform * eye)
    focus = v4to3(transform * focus)
    camera = vnorm(eye - focus)
    # log.debug('%s %s %s', eye, focus, camera)
    return camera

def getFaces(mesh):
    group_mask = np.ones(len(mesh._faceGroups), dtype=bool)
    for g in mesh._faceGroups:
        if g.name.startswith('joint') or g.name.startswith('helper'):
            group_mask[g.idx] = False
    faces = np.argwhere(group_mask[mesh.group])[...,0]
    return faces

def mapImageSoft(srcImg, mesh, leftTop, rightBottom):
    dstImg = mh.Image(gui3d.app.selectedHuman.getTexture())

    dstW = dstImg.width
    dstH = dstImg.height

    srcImg = srcImg.convert(dstImg.components)

    camera = getCamera(mesh)
    faces = getFaces(mesh)

    # log.debug('matrix: %s', gui3d.app.modelCamera.getConvertToScreenMatrix())

    texco = np.asarray([0,dstH])[None,None,:] + mesh.texco[mesh.fuvs[faces]] * np.asarray([dstW,-dstH])[None,None,:]
    matrix = np.asarray(gui3d.app.modelCamera.getConvertToScreenMatrix(mesh))
    coord = np.concatenate((mesh.coord[mesh.fvert[faces]], np.ones((len(faces),4,1))), axis=-1)
    # log.debug('texco: %s, coord: %s', texco.shape, coord.shape)
    coord = np.sum(matrix[None,None,:,:] * coord[:,:,None,:], axis = -1)
    # log.debug('coord: %s', coord.shape)
    coord = coord[:,:,:2] / coord[:,:,3:]
    # log.debug('coord: %s', coord.shape)
    # log.debug('coords: %f-%f, %f-%f',
    #           np.amin(coord[...,0]), np.amax(coord[...,0]),
    #           np.amin(coord[...,1]), np.amax(coord[...,1]))
    # log.debug('rect: %s %s', leftTop, rightBottom)
    coord -= np.asarray([leftTop[0], leftTop[1]])[None,None,:]
    coord /= np.asarray([rightBottom[0] - leftTop[0], rightBottom[1] - leftTop[1]])[None,None,:]
    alpha = np.sum(mesh.vnorm[mesh.fvert[faces]] * camera[None,None,:], axis=-1)
    alpha = np.maximum(0, alpha)
    # alpha[...] = 1 # debug
    # log.debug('alpha: %s', alpha.shape)
    # log.debug('coords: %f-%f, %f-%f',
    #           np.amin(coord[...,0]), np.amax(coord[...,0]),
    #           np.amin(coord[...,1]), np.amax(coord[...,1]))
    uva = np.concatenate((coord, alpha[...,None]), axis=-1)
    # log.debug('uva: %s', uva.shape)
    valid = np.any(alpha >= 0, axis=1)
    # log.debug('valid: %s', valid.shape)
    texco = texco[valid,:,:]
    uva = uva[valid,:,:]

    # log.debug('%s %s', texco.shape, uva.shape)

    def progress(base, i, n):
        gui3d.app.progress(base + 0.5 * i / n)

    # log.debug('src: %s, dst: %s', srcImg.data.shape, dstImg.data.shape)

    log.debug("mapImage: begin render")

    RasterizeTriangles(dstImg, texco[:,[0,1,2],:], UvAlphaShader(dstImg, srcImg, uva[:,[0,1,2],:]), progress = lambda i,n: progress(0.0,i,n))
    RasterizeTriangles(dstImg, texco[:,[2,3,0],:], UvAlphaShader(dstImg, srcImg, uva[:,[2,3,0],:]), progress = lambda i,n: progress(0.5,i,n))
    gui3d.app.progress(1.0)

    log.debug("mapImage: end render")

    return dstImg

def mapImageGL(srcImg, mesh, leftTop, rightBottom):
    log.debug("mapImageGL: 1")

    dstImg = gui3d.app.selectedHuman.meshData.object3d.textureTex

    dstW = dstImg.width
    dstH = dstImg.height

    left, top = leftTop
    right, bottom = rightBottom

    camera = getCamera(mesh)

    coords = mesh.r_texco

    texmat = gui3d.app.modelCamera.getConvertToScreenMatrix(mesh)
    texmat = matrix.scale((1/(right - left), 1/(top - bottom), 1)) * matrix.translate((-left, -bottom, 0)) * texmat
    texmat = np.asarray(texmat)

    texco = mesh.r_coord

    alpha = np.sum(mesh.r_vnorm * camera[None,:], axis=-1)
    alpha = np.maximum(alpha, 0)
    color = (np.array([0, 0, 0, 0])[None,...] + alpha[...,None]) * 255

    color = np.ascontiguousarray(color, dtype=np.uint8)
    texco = np.ascontiguousarray(texco, dtype=np.float32)

    result = mh.renderSkin(dstImg, mesh.vertsPerPrimitive, coords, index = mesh.index,
                           texture = srcImg, UVs = texco, textureMatrix = texmat,
                           color = color, clearColor = None)

    return result

def mapImage(imgMesh, mesh, leftTop, rightBottom):
    if mh.hasRenderSkin():
        return mapImageGL(imgMesh.mesh.object3d.textureTex, mesh, leftTop, rightBottom)
    else:
        return mapImageSoft(mh.Image(imgMesh.getTexture()), mesh, leftTop, rightBottom)

def fixSeams(img):
    h,w,c = img.data.shape
    neighbors = np.empty((3,3,h,w,c), dtype=np.uint8)

    neighbors[1,1,:,:,:] = img.data

    neighbors[1,0,:,:,:] = np.roll(neighbors[1,1,:,:,:], -1, axis=-2)
    neighbors[1,2,:,:,:] = np.roll(neighbors[1,1,:,:,:],  1, axis=-2)

    neighbors[0,:,:,:,:] = np.roll(neighbors[1,:,:,:,:], -1, axis=-3)
    neighbors[2,:,:,:,:] = np.roll(neighbors[1,:,:,:,:],  1, axis=-3)

    chroma = neighbors[...,:-1]
    alpha = neighbors[...,-1]

    chroma_f = chroma.reshape(9,h,w,c-1)
    alpha_f = alpha.reshape(9,h,w)

    border = np.logical_and(alpha[1,1,:,:] == 0, np.any(alpha_f[:,:,:] != 0, axis=0))

    alpha_f = alpha_f.astype(np.float32)[...,None]
    fill = np.sum(chroma_f[:,:,:,:] * alpha_f[:,:,:,:], axis=0) / np.sum(alpha_f[:,:,:,:], axis=0)

    img.data[...,:-1][border] = fill.astype(np.uint8)[border]
    img.data[...,-1:][border] = 255

def mapLightingSoft(lightpos = (-10.99, 20.0, 20.0), progressCallback = None):
    """
    Create a lightmap for the selected human (software renderer).
    """

    mesh = gui3d.app.selectedHuman.mesh

    W = 1024
    H = 1024
    
    dstImg = mh.Image(width=W, height=H, components=4)
    dstImg.data[...] = 0

    delta = lightpos - mesh.coord
    ld = vnorm(delta)
    del delta
    s = np.sum(ld * mesh.vnorm, axis=-1)
    del ld
    s = np.maximum(0, np.minimum(255, (s * 256))).astype(np.uint8)
    mesh.color[...,:3] = s[...,None]
    mesh.color[...,3] = 255
    del s

    faces = getFaces(mesh)

    coords = np.asarray([0,H])[None,None,:] + mesh.texco[mesh.fuvs[faces]] * np.asarray([W,-H])[None,None,:]
    colors = mesh.color[mesh.fvert[faces]]
    # log.debug("mapLighting: %s %s %s", faces.shape, coords.shape, colors.shape)

    log.debug("mapLighting: begin render")

    def progress(base, i, n):
        if progressCallback == None:
            gui3d.app.progress(base + 0.5 * i / n, "Projecting lightmap")
        else:
            progressCallback(base + 0.5 * i / n)

    RasterizeTriangles(dstImg, coords[:,[0,1,2],:], ColorShader(colors[:,[0,1,2],:]), progress = lambda i,n: progress(0.0,i,n))
    RasterizeTriangles(dstImg, coords[:,[2,3,0],:], ColorShader(colors[:,[2,3,0],:]), progress = lambda i,n: progress(0.5,i,n))
    gui3d.app.progress(1.0)

    fixSeams(dstImg)

    log.debug("mapLighting: end render")

    mesh.setColor([255, 255, 255, 255])

    return dstImg

def mapLightingGL(lightpos = (-10.99, 20.0, 20.0)):
    """
    Create a lightmap for the selected human (hardware accelerated).
    """

    mesh = gui3d.app.selectedHuman.mesh

    W = 1024
    H = 1024

    delta = lightpos - mesh.coord
    ld = vnorm(delta)
    del delta
    s = np.sum(ld * mesh.vnorm, axis=-1)
    del ld
    s = np.maximum(0, np.minimum(255, (s * 256))).astype(np.uint8)
    mesh.color[...,:3] = s[...,None]
    mesh.color[...,3] = 255
    del s

    mesh.markCoords(colr = True)
    mesh.update()

    coords = mesh.r_texco
    colors = mesh.r_color

    dstImg = mh.renderSkin((W, H), mesh.vertsPerPrimitive, coords, index = mesh.index,
                           color = colors, clearColor = (0, 0, 0, 0))

    fixSeams(dstImg)

    mesh.setColor([255, 255, 255, 255])

    log.debug('mapLightingGL: %s', dstImg.data.shape)

    return dstImg

def mapLighting(lightpos = (-10.99, 20.0, 20.0), progressCallback = None):
    """
    Bake lightmap for human from one light.
    Uses OpenGL hardware acceleration if the necessary OGL features are
    available, otherwise uses a slower software rasterizer.
    """
    if mh.hasRenderSkin():
        return mapLightingGL(lightpos)
    else:
        return mapLightingSoft(lightpos, progressCallback)

def mapSceneLighting(scn, progressCallback = None):
    """
    Create a lightmap for a scene with one or multiple lights.
    """
    def progress(prog):
        if (progressCallback is not None):
            progressCallback(prog)
        else:
            pass

    lnum = float(len(scn.lights))
    if (lnum>0):    # Add up all the lightmaps.
        lmap = mapLighting(scn.lights[0].position, lambda p: progress(p/lnum))
        i = 1.0        
        for light in scn.lights[1:]:
            lmap = image_operations.mix(
                lmap, mapLighting(light.position, lambda p: progress((i+p)/lnum)),1,1)       
            i += 1.0
        return image_operations.clipped(lmap)
    else:   # If the scene has no lights, return an empty lightmap.
        return mh.Image(data = np.zeros((1024, 1024, 1), dtype=np.uint8))

def rasterizeHLines(dstImg, edges, delta, progress = None):
    flip = delta[:,0] < 0
    p = np.where(flip[:,None,None], edges[:,::-1,:], edges[:,:,:])
    del edges
    d = np.where(flip[:,None], -delta, delta)
    del delta, flip
    x0 = p[:,0,0]
    x1 = p[:,1,0]
    y0 = p[:,0,1]
    del p
    dx = d[:,0]
    dy = d[:,1]
    m = dy / dx
    del dx, dy, d
    c = y0 - m * x0
    x0 = np.floor(x0).astype(int)
    x1 = np.ceil(x1).astype(int)
    del y0

    data = dstImg.data[::-1]

    for i in xrange(len(x0)):
        if progress is not None and i % 100 == 0:
            progress(i, len(x0))
        x = np.arange(x0[i], x1[i])
        y = m[i] * (x + 0.5) + c[i]
        data[np.floor(y).astype(int),x,:] = 255

def rasterizeVLines(dstImg, edges, delta, progress = None):
    flip = delta[:,1] < 0
    p = np.where(flip[:,None,None], edges[:,::-1,:], edges[:,:,:])
    del edges
    d = np.where(flip[:,None], -delta, delta)
    del delta, flip
    x0 = p[:,0,0]
    y0 = p[:,0,1]
    y1 = p[:,1,1]
    del p
    dx = d[:,0]
    dy = d[:,1]
    m = dx / dy
    del dx, dy, d
    c = x0 - m * y0
    y0 = np.floor(y0).astype(int)
    y1 = np.ceil(y1).astype(int)
    del x0

    data = dstImg.data[::-1]

    for i in xrange(len(y0)):
        if progress is not None and i % 100 == 0:
            progress(i, len(y0))
        y = np.arange(y0[i], y1[i]) + 0.5
        x = m[i] * y + c[i]
        data[y.astype(int),np.floor(x).astype(int),:] = 255

def mapUVSoft():
    """
    Project the UV map topology of the selected human mesh onto a texture 
    (software rasterizer).
    """

    mesh = gui3d.app.selectedHuman.mesh

    W = 2048
    H = 2048
    
    dstImg = mh.Image(width=W, height=H, components=3)
    dstImg.data[...] = 0

    faces = getFaces(mesh)

    log.debug("mapUV: begin setup")

    fuvs = mesh.fuvs[faces]
    del faces
    edges = np.array([fuvs, np.roll(fuvs, 1, axis=-1)]).transpose([1,2,0]).reshape((-1,2))
    del fuvs
    edges = np.where((edges[:,0] < edges[:,1])[:,None], edges, edges[:,::-1])
    ec = edges[:,0] + (edges[:,1] << 16)
    del edges
    ec = np.unique(ec)
    edges = np.array([ec & 0xFFFF, ec >> 16]).transpose()
    del ec
    edges = mesh.texco[edges] * (W, H)

    delta = edges[:,1,:] - edges[:,0,:]
    vertical = np.abs(delta[:,1]) > np.abs(delta[:,0])
    horizontal = -vertical

    hdelta = delta[horizontal]
    vdelta = delta[vertical]
    del delta
    hedges = edges[horizontal]
    vedges = edges[vertical]
    del edges, horizontal, vertical

    log.debug("mapUV: begin render")

    def progress(base, i, n):
        gui3d.app.progress(base + 0.5 * i / n, "Projecting UV map")

    rasterizeHLines(dstImg, hedges, hdelta, progress = lambda i,n: progress(0.0,i,n))
    rasterizeVLines(dstImg, vedges, vdelta, progress = lambda i,n: progress(0.5,i,n))
    gui3d.app.progress(1.0)

    log.debug("mapUV: end render")

    return dstImg.convert(3)

def mapUVGL():
    """
    Project the UV map topology of the selected human mesh onto a texture 
    (hardware accelerated).
    """

    mesh = gui3d.app.selectedHuman.mesh

    W = 2048
    H = 2048
    
    dstImg = mh.Texture(size=(W,H), components=3)

    log.debug("mapUVGL: begin setup")

    fuvs = mesh.index
    edges = np.array([fuvs, np.roll(fuvs, 1, axis=-1)]).transpose([1,2,0]).reshape((-1,2))
    del fuvs
    edges = np.where((edges[:,0] < edges[:,1])[:,None], edges, edges[:,::-1])
    ec = edges[:,0] + (edges[:,1] << 16)
    del edges
    ec = np.unique(ec)
    edges = np.array([ec & 0xFFFF, ec >> 16]).transpose()
    del ec

    log.debug("mapUVGL: begin render")

    coords = mesh.r_texco
    edges = np.ascontiguousarray(edges, dtype=np.uint32)

    dstImg = mh.renderSkin(dstImg, 2, coords, index = edges, clearColor = (0, 0, 0, 255))

    log.debug("mapUV: end render")

    return dstImg.convert(3)

def mapUV():
    """
    Project the UV map topology of the selected human mesh onto a texture.
    Uses OpenGL hardware acceleration if the necessary OGL features are
    available, otherwise uses a slower software rasterizer.
    """
    if mh.hasRenderSkin():
        return mapUVGL()
    else:
        return mapUVSoft()


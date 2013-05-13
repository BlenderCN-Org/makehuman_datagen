#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Glynn Clements

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

import os.path
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.ARB.texture_non_power_of_two import *
from core import G
from image import Image
import log

class Texture(object):
    _npot = None
    _powers = None

    def __new__(cls, *args, **kwargs):
        self = super(Texture, cls).__new__(cls)

        if cls._npot is None:
            cls._npot = glInitTextureNonPowerOfTwoARB()
        if cls._powers is None:
            cls._powers = [2**i for i in xrange(20)]

        self.textureId = glGenTextures(1)
        self.width = 0
        self.height = 0
        self.modified = None

        return self

    def __init__(self, image = None, size = None, components = 4):
        if image is not None:
            self.loadImage(image)
        elif size is not None:
            width, height = size
            self.initTexture(width, height, components)

    def __del__(self):
        try:
            glDeleteTextures(self.textureId)
        except StandardError:
            pass

    @staticmethod
    def getFormat(components):
        if components == 1:
            return (GL_ALPHA8, GL_ALPHA)
        elif components == 3:
            return (3, GL_RGB)
        elif components == 4:
            return (4, GL_RGBA)
        else:
            raise RuntimeError("Unsupported pixel format")

    def initTexture(self, width, height, components = 4, pixels = None):
        internalFormat, format = self.getFormat(components)

        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

        use_mipmaps = not (width in self._powers and height in self._powers) and not self._npot
        if use_mipmaps and pixels is None:
            raise RuntimeError("Non-power-of-two textures not supported")

        if height == 1:
            glBindTexture(GL_TEXTURE_1D, self.textureId)

            if not use_mipmaps:
                glTexImage1D(GL_PROXY_TEXTURE_1D, 0, internalFormat, width, 0, format, GL_UNSIGNED_BYTE, pixels)
                if not glGetTexLevelParameteriv(GL_PROXY_TEXTURE_1D, 0, GL_TEXTURE_WIDTH):
                    log.notice('texture size (%d) too large, building mipmaps', width)
                    use_mipmaps = True

            if use_mipmaps:
                gluBuild1DMipmaps(GL_TEXTURE_1D, internalFormat, width, format, GL_UNSIGNED_BYTE, pixels)
                # glGetTexLevelParameter is broken on X11
                # width  = glGetTexLevelParameteriv(GL_TEXTURE_1D, 0, GL_TEXTURE_WIDTH)
            else:
                glTexImage1D(GL_TEXTURE_1D, 0, internalFormat, width, 0, format, GL_UNSIGNED_BYTE, pixels)

            glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        else:
            glBindTexture(GL_TEXTURE_2D, self.textureId)

            if not use_mipmaps:
                glTexImage2D(GL_PROXY_TEXTURE_2D, 0, internalFormat, width, height, 0, format, GL_UNSIGNED_BYTE, pixels)
                if not glGetTexLevelParameteriv(GL_PROXY_TEXTURE_2D, 0, GL_TEXTURE_WIDTH):
                    log.notice('texture size (%d x %d) too large, building mipmaps', width, height)
                    use_mipmaps = True

            if use_mipmaps:
                gluBuild2DMipmaps(GL_TEXTURE_2D, internalFormat, width, height, format, GL_UNSIGNED_BYTE, pixels)
                # glGetTexLevelParameter is broken on X11
                # width  = glGetTexLevelParameteriv(GL_TEXTURE_2D, 0, GL_TEXTURE_WIDTH)
                # height = glGetTexLevelParameteriv(GL_TEXTURE_2D, 0, GL_TEXTURE_HEIGHT)
            else:
                glTexImage2D(GL_TEXTURE_2D, 0, internalFormat, width, height, 0, format, GL_UNSIGNED_BYTE, pixels)

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        self.width, self.height = width, height
        log.debug('initTexture: %s, %s, %s', width, height, use_mipmaps)

    def loadImage(self, image):
        if isinstance(image, (str, unicode)):
            image = Image(image)

        pixels = image.flip_vertical().data

        self.initTexture(image.width, image.height, image.components, pixels)

    def loadSubImage(self, image, x, y):
        if not self.textureId:
            raise RuntimeError("Texture is empty, cannot load a sub texture into it")

        if isinstance(image, (str, unicode)):
            image = Image(image)

        internalFormat, format = self.getFormat(image.components)

        pixels = image.flip_vertical().data

        if image.height == 1:
            glBindTexture(GL_TEXTURE_1D, self.textureId)
            glTexSubImage1D(GL_TEXTURE_1D, 0, x, image.width, format, GL_UNSIGNED_BYTE, pixels)
        else:
            glBindTexture(GL_TEXTURE_2D, self.textureId)
            glTexSubImage2D(GL_TEXTURE_2D, 0, x, y, image.width, image.height, format, GL_UNSIGNED_BYTE, pixels)

_textureCache = {}

def getTexture(path, cache=None):
    texture = None
    cache = cache or _textureCache
    
    if path in cache:
        texture = cache[path]
        if texture is False:
            return texture

        if os.path.getmtime(path) > texture.modified:
            log.message('reloading %s', path)   # TL: unicode problems unbracketed

            try:
                img = Image(path=path)
                texture.loadImage(img)
            except RuntimeError, text:
                log.error("%s", text, exc_info=True)
                return
            else:
                texture.modified = os.path.getmtime(path)
    else:
        try:
            img = Image(path=path)
            texture = Texture(img)
        except RuntimeError, text:
            log.error("Error loading texture %s", path, exc_info=True)
            texture = False
        else:
            texture.modified = os.path.getmtime(path)
        cache[path] = texture

    return texture
    
def reloadTextures():
    log.message('Reloading textures')
    for path in _textureCache:
        try:
            _textureCache[path].loadImage(path)
        except RuntimeError, text:
            log.error("Error loading texture %s", path, exc_info=True)

def reloadTexture(path):
    log.message('Reloading texture %s', path)
    if path not in _textureCache.keys():
        log.error('Cannot reload non-existing texture %s', path)
    try:
        _textureCache[path].loadImage(path)
    except RuntimeError, text:
        log.error("Error loading texture %s", path, exc_info=True)


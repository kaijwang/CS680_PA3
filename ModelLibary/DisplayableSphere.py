'''
A displayable object which defines a shpere,
texture mapping is implemented and control by Bool doTexture

:author: Kaijun Wang
:version: 2021.10.10
'''
import os
import numpy as np
import string

try:
    import wx
    from wx import glcanvas
except ImportError:
    raise ImportError("Required dependency wxPython not present")

try:
    import OpenGL

    try:
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
        import OpenGL.GLUT as glut  # this fails on OS X 11.x
    except ImportError:
        from ctypes import util

        orig_util_find_library = util.find_library


        def new_util_find_library(name):
            res = orig_util_find_library(name)
            if res:
                return res
            return '/System/Library/Frameworks/' + name + '.framework/' + name


        util.find_library = new_util_find_library
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
        import OpenGL.GLUT as glut
except ImportError:
    raise ImportError("Required dependency PyOpenGL not present")

try:
    # From pip package "Pillow"
    from PIL import Image
except:
    print("Need to install PIL package. Pip package name is Pillow")
    raise ImportError

from Displayable import Displayable


class DisplayableSphere(Displayable):
    """
    Create a enclosed cylinder whose one end is at z=0 and it grows along z coordinates
    """

    callListHandle = 0  # long int. override the one in Displayable
    qd = None  # Quadric
    scale = None
    _bufferData = None

    def __init__(self, parent, radius, height, scale=None, doTexture=False, transparent=False):
        super().__init__(parent)
        parent.context.SetCurrent(parent)
        self.radius = radius
        self.height = height
        self.doTexture = doTexture
        if scale is None:
            scale = [1, 1, 1]
        self.scale = scale
        self.transparent = transparent

    def draw(self):
        gl.glCallList(self.callListHandle)

    def initialize(self):
        self.callListHandle = gl.glGenLists(1)
        self.qd = glu.gluNewQuadric()

        if self.transparent:
            gl.glEnable(gl.GL_BLEND)
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        gl.glNewList(self.callListHandle, gl.GL_COMPILE)
        gl.glPushMatrix()
        gl.glScale(*self.scale)

        glu.gluSphere(self.qd, self.radius, 36, 18)

        gl.glPopMatrix()
        gl.glEndList()

        gl.glDepthMask(gl.GL_TRUE)

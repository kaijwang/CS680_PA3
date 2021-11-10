'''
A displayable object which defines a roundCylinder (a cylinder with sphere in both ends)

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


class DisplayableRoundCylinder(Displayable):
    """
    Create a enclosed cylinder whose one end is at z=0 and it grows along z coordinates
    """

    ##### TODO 1: Build Creature Parts
    # Build the class(es) of basic geometric objects/combination that could add up to be a part of your creature.
    # E.g., you could write a cylinder class to be the trunk of your creature's limb. Or, you could
    # write a two-sphere class to be the eye ball of your creature (one sphere for the eye ball and one sphere for the lens/iris).
    # The needed GLU functions for cylinder and sphere are mentioned in README.md



    callListHandle = 0  # long int. override the one in Displayable
    qd = None  # Quadric
    scale = None
    # edgeLength = 1
    _bufferData = None

    def __init__(self, parent, top_radius, bot_radius, height, sphere_scale, scale=None, setoff=False):
        super().__init__(parent)
        parent.context.SetCurrent(parent)
        self.top_radius = top_radius
        self.bot_radius = bot_radius
        self.height = height
        self.sphere_scale = sphere_scale
        if scale is None:
            scale = [1, 1, 1]
        self.scale = scale
        self.setoff = setoff

    ##### BONUS 1: Texture your creature
    # Requirement: 1. Build the texture mapping that binds texture image to your objects.

    def draw(self):
        gl.glCallList(self.callListHandle)

    def initialize(self):
        self.callListHandle = gl.glGenLists(1)
        self.qd = glu.gluNewQuadric()

        gl.glNewList(self.callListHandle, gl.GL_COMPILE)
        gl.glPushMatrix()

        gl.glScale(*self.scale)
        if self.setoff:
            gl.glTranslate(0, -self.top_radius / 2, 0)

        glu.gluCylinder(self.qd,
                        self.top_radius, self.bot_radius,
                        self.height, 36, 18)

        gl.glScale(1.0, 1.0, self.sphere_scale)
        glu.gluSphere(self.qd, self.top_radius, 36, 18)

        gl.glTranslate(0, 0, self.height*(1/self.sphere_scale))
        glu.gluSphere(self.qd, self.bot_radius, 36, 18)

        gl.glPopMatrix()
        gl.glEndList()

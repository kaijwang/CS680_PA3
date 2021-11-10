'''
A displayable object which defines a triangle surface,
the surface's shape can change according to the edge position

:author: Kaijun Wang
:version: 2021.10.10
'''
import os
import numpy as np
import string

from Point import Point

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


class DisplayableSurface(Displayable):
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
    _bufferData = None

    def __init__(self, parent, point1, point2, point3, edgeLength, scale=None):
        super().__init__(parent)
        parent.context.SetCurrent(parent)
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3
        self.edgeLength = edgeLength
        if scale is None:
            scale = [1, 1, 1]
        self.scale = scale

    ##### BONUS 1: Texture your creature
    # Requirement: 1. Build the texture mapping that binds texture image to your objects.

    def draw(self):
        gl.glCallList(self.callListHandle)

    def update_points(self, uAngle, vAngle, wAngle):
        self.point3 = Point((self.edgeLength * np.sin(np.deg2rad(vAngle)), 0,
                            -self.edgeLength * np.cos(np.deg2rad(vAngle))))

    def initialize(self):
        self.callListHandle = gl.glGenLists(1)
        self.qd = glu.gluNewQuadric()

        gl.glNewList(self.callListHandle, gl.GL_COMPILE)
        gl.glPushMatrix()

        gl.glScale(*self.scale)

        gl.glBegin(gl.GL_TRIANGLES)
        gl.glVertex3f(*self.point1.getCoords())
        gl.glVertex3f(*self.point2.getCoords())
        gl.glVertex3f(*self.point3.getCoords())

        gl.glVertex3f(*self.point3.getCoords())
        gl.glVertex3f(*self.point2.getCoords())
        gl.glVertex3f(*self.point1.getCoords())

        gl.glEnd()

        gl.glPopMatrix()
        gl.glEndList()

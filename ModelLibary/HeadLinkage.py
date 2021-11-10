"""
Model our creature and wrap it in one class
First version at 09/28/2021

:author: micou(Zezhou Sun)
:version: 2021.2.1
"""

from Component import Component
from ModelLibary.DisplayableEyeball import DisplayableEyeball
from Point import Point
import ColorType as Ct
from ModelLibary.DisplayableRoundCylinder import DisplayableRoundCylinder
from ModelLibary.DisplayableSphere import DisplayableSphere


class HeadLinkage(Component):
    """
    Define our linkage model
    """

    ##### TODO 2: Model the Creature
    # Build the class(es) of objects that could utilize your built geometric object/combination classes. E.g., you could define
    # three instances of the cyclinder trunk class and link them together to be the "limb" class of your creature.

    components = None
    contextParent = None

    def __init__(self, parent, position, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        head = Component(Point((0, 0, 0)), DisplayableSphere(self.contextParent, 0.8, 0.15, [0.6, 0.6, 0.5]))
        head.setDefaultColor(Ct.LIGHTCORAL)
        head.setRotateExtent(head.uAxis, -30, 5)
        head.setRotateExtent(head.vAxis, -20, 20)
        head.setRotateExtent(head.wAxis, -30, 30)

        ear_l = Component(Point((0.4, 0.55, 0.1)), DisplayableRoundCylinder(self.contextParent, 0.8, 0.8, 0.1, 0.1, [0.4, 0.6, 0.5]))
        ear_l.setDefaultColor(Ct.LIGHTCORAL)
        ear_l.setDefaultAngle(20, ear_l.uAxis)
        ear_l.lock_rotate()

        ear_r = Component(Point((-0.4, 0.55, 0.1)),
                        DisplayableRoundCylinder(self.contextParent, 0.8, 0.8, 0.1, 0.1, [0.4, 0.6, 0.5]))
        ear_r.setDefaultColor(Ct.LIGHTCORAL)
        ear_r.setDefaultAngle(20, ear_r.uAxis)
        ear_r.lock_rotate()

        nose = Component(Point((0, -0.25, -0.37)), DisplayableSphere(self.contextParent, 0.3, 0.15, [0.5, 0.5, 0.5]))
        nose.setDefaultColor(Ct.DARKCORAL)
        nose.lock_rotate()

        eyeball_l = Component(Point((0.2, 0, -0.3)), DisplayableEyeball(self.contextParent, 0.3, [0.5, 0.5, 0.5]))
        eyeball_l.setDefaultColor(Ct.LIGHTCORAL)
        eyeball_l.setDefaultAngle(30, eyeball_l.wAxis)

        eyeball_r = Component(Point((-0.2, 0, -0.3)), DisplayableEyeball(self.contextParent, 0.3, [0.5, 0.5, 0.5]))
        eyeball_r.setDefaultAngle(-30, eyeball_l.wAxis)
        eyeball_r.setDefaultColor(Ct.LIGHTCORAL)

        self.addChild(head)
        head.addChild(ear_l)
        head.addChild(ear_r)
        head.addChild(nose)
        head.addChild(eyeball_l)
        head.addChild(eyeball_r)

        self.components = [head, ear_l, ear_r, eyeball_l, eyeball_r]

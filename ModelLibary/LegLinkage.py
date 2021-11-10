"""
Model our creature and wrap it in one class
First version at 09/28/2021

:author: micou(Zezhou Sun)
:version: 2021.2.1
"""

from Component import Component
from Point import Point
import ColorType as Ct
from ModelLibary.DisplayableRoundCylinder import DisplayableRoundCylinder


class LegLinkage(Component):
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

        scale1 = [0.07, 0.07, 0.15]

        calf = Component(Point((0, -0.1, 0.2)), DisplayableRoundCylinder(self.contextParent, 0.3, 0.15, 1, 0.5, [0.5, 0.5, 0.5]))
        calf.setDefaultColor(Ct.MAROON)
        calf.setDefaultAngle(45, calf.uAxis)
        calf.setDefaultAngle(90, calf.wAxis)
        calf.setRotateExtent(calf.uAxis, 15, 75)
        calf.setRotateExtent(calf.vAxis, -20, 20)
        calf.setRotateExtent(calf.wAxis, 70, 110)

        link1 = Component(Point((0, 0, 0.55)), DisplayableRoundCylinder(self.contextParent, 1, 1, 0.6, 0.5, scale1))
        link1.setDefaultColor(Ct.MAROON)
        link1.setDefaultAngle(-90, calf.wAxis)
        link1.setDefaultAngle(75, calf.vAxis)
        link1.lock_rotate()

        link2 = Component(Point((0, 0, -0.1)), DisplayableRoundCylinder(self.contextParent, 1, 1, 0.6, 0.5, scale1))
        link2.setDefaultColor(Ct.MAROON)
        link2.setDefaultAngle(135, link1.uAxis)
        link2.setDefaultAngle(30, link1.vAxis)
        link2.lock_rotate()

        link3 = Component(Point((0, 0, -0.1)),
                          DisplayableRoundCylinder(self.contextParent, 1, 1, 0.6, 0.5, scale1))
        link3.setDefaultColor(Ct.MAROON)
        link3.setDefaultAngle(135, link1.uAxis)
        link3.setDefaultAngle(-30, link1.vAxis)
        link3.lock_rotate()

        self.addChild(calf)
        calf.addChild(link1)
        link1.addChild(link2)
        link1.addChild(link3)

        self.components = [calf]

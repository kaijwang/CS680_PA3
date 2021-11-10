"""
Model our creature and wrap it in one class
First version at 09/28/2021

:author: micou(Zezhou Sun)
:version: 2021.2.1
"""
import numpy as np

from Component import Component
from ModelLibary.DisplayableCone import DisplayableCone
from ModelLibary.DisplayableSurface import DisplayableSurface
from Point import Point
import ColorType as Ct
from ModelLibary.DisplayableSphere import DisplayableSphere
from ModelLibary.DisplayableRoundCylinder import DisplayableRoundCylinder


class WingLinkage(Component):
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

        arm = Component(Point((0, 0, 0)),
                        DisplayableRoundCylinder(self.contextParent, 0.5, 0.5, 2, 0.2, [0.25, 0.25, 1]))
        arm.setDefaultColor(Ct.LIGHTCORAL)
        arm.setDefaultAngle(-120, arm.uAxis)
        arm.setDefaultAngle(10, arm.vAxis)

        limb1 = Component(Point((0, 0, 1.8)),
                          DisplayableRoundCylinder(self.contextParent, 0.5, 0.5, 1.8, 0.2, [0.2, 0.2, 1]))
        limb1.setDefaultColor(Ct.LIGHTCORAL)
        limb1.setDefaultAngle(135, limb1.vAxis)
        limb1.setRotateExtent(limb1.vAxis, 105, 165)
        limb1.setRotateExtent(limb1.uAxis, 0, 0)
        limb1.setRotateExtent(limb1.wAxis, 0, 0)

        hand1 = Component(Point((0, 0, 1.8)), DisplayableSphere(self.contextParent, 0.5, 0.5, [0.3, 0.3, 0.4]))
        hand1.setDefaultColor(Ct.LIGHTCORAL)

        wing1 = Component(Point((0, 0, 0)), DisplayableSurface(self.contextParent, Point((0, 0, 0)), Point((0, 0, 1.8)),
                                                               Point((1.8 * np.sin(np.deg2rad(limb1.vAngle)), 0,
                                                                      -1.8 * np.cos(np.deg2rad(limb1.vAngle)))), 1.8))
        wing1.setDefaultColor(Ct.LIGHTCORAL)

        limb2 = Component(Point((0, 0, 0)),
                          DisplayableRoundCylinder(self.contextParent, 0.5, 0.5, 1.8, 0.2, [0.2, 0.2, 1]))
        limb2.setDefaultColor(Ct.LIGHTCORAL)
        limb2.setDefaultAngle(-45, limb2.vAxis)
        limb2.setRotateExtent(limb2.vAxis, -75, -15)
        limb2.setRotateExtent(limb1.uAxis, 0, 0)
        limb2.setRotateExtent(limb1.wAxis, 0, 0)
        hand2 = Component(Point((0, 0, 1.8)), DisplayableSphere(self.contextParent, 0.5, 0.5, [0.3, 0.3, 0.4]))
        hand2.setDefaultColor(Ct.LIGHTCORAL)
        wing2 = Component(Point((0, 0, 0)), DisplayableSurface(self.contextParent, Point((0, 0, 0)), Point((0, 0, 1.8)),
                                                               Point((-1.8 * np.sin(np.deg2rad(limb2.vAngle)), 0,
                                                                      1.8 * np.cos(np.deg2rad(limb2.vAngle)))), -1.8))
        wing2.setDefaultColor(Ct.LIGHTCORAL)
        horn = Component(Point((0, 0, 2.05)), DisplayableCone(self.contextParent, 0.5, 0.5, [0.2, 0.2, 0.4]))
        horn.setDefaultColor(Ct.MAROON)



        self.addChild(arm)
        arm.addChild(limb1)
        arm.addChild(horn)
        limb1.addChild(limb2)
        limb1.addChild(hand1)
        limb1.addChild(wing1)
        limb2.addChild(hand2)
        limb2.addChild(wing2)

        self.components = [arm, limb1, limb2]

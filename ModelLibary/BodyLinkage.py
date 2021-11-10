"""
Model our creature and wrap it in one class

:author: Kaijun Wang
:version: 2021.11.9
"""

from Component import Component
from Point import Point
import ColorType as Ct
from ModelLibary.DisplayableSphere import DisplayableSphere


class BodyLinkage(Component):
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

        linkageLength = [0.9, 0.3]

        link1 = Component(Point((0, 0, 0)), DisplayableSphere(self.contextParent, 3, 3, [0.4, 0.4, 0.35], True))
        link1.setDefaultColor(Ct.LIGHTCORAL)
        link1.setDefaultAngle(90, link1.vAxis)
        link2 = Component(Point((0, -0.5, linkageLength[0])), DisplayableSphere(self.contextParent, 1.5, 1.5, [0.4, 0.35, 0.4]))
        link2.setDefaultColor(Ct.LIGHTCORAL)
        link2.setDefaultAngle(45, link2.uAxis)
        link2.setRotateExtent(link2.uAxis, 15, 75)
        link2.setRotateExtent(link2.vAxis, -15, 15)
        link2.setRotateExtent(link2.wAxis, 0, 0)

        self.addChild(link1)
        link1.addChild(link2)

        self.components = [link1, link2]

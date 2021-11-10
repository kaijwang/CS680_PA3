"""

:author: Kaijun Wang
:version: 2021.2.1
"""

from Component import Component
from Point import Point
import ColorType as Ct
from ModelLibary.DisplayableRoundCylinder import DisplayableRoundCylinder


class TailLinkage(Component):
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

        linkageLength = [0.3, 0.3, 0.3, 0.3, 0.3, 0.3]

        link1 = Component(Point((0, 0, 0)), DisplayableRoundCylinder(self.contextParent, 0.5, 0.5, 1.5, 0.6, [0.4, 0.2, 0.2]))
        link1.setDefaultColor(Ct.MAROON)
        link2 = Component(Point((0, 0, linkageLength[0])),
                          DisplayableRoundCylinder(self.contextParent, 0.5, 0.6, 1.5, 0.6, [0.4, 0.2, 0.2]))
        link2.setDefaultColor(Ct.MAROON)
        link3 = Component(Point((0, 0, linkageLength[1])),
                          DisplayableRoundCylinder(self.contextParent, 0.6, 0.75, 1.5, 0.6, [0.4, 0.2, 0.2]))
        link3.setDefaultColor(Ct.MAROON)
        link4 = Component(Point((0, 0, linkageLength[2])),
                          DisplayableRoundCylinder(self.contextParent, 0.75, 0.9, 1.5, 0.6, [0.4, 0.2, 0.2]))
        link4.setDefaultColor(Ct.MAROON)
        link5 = Component(Point((0, 0, linkageLength[3])),
                          DisplayableRoundCylinder(self.contextParent, 0.9, 0.9, 1.5, 0.6, [0.4, 0.2, 0.2]))
        link5.setDefaultColor(Ct.MAROON)
        link6 = Component(Point((0, 0, linkageLength[4])),
                          DisplayableRoundCylinder(self.contextParent, 0.9, 0.75, 1.5, 0.6, [0.4, 0.2, 0.2]))
        link6.setDefaultColor(Ct.MAROON)

        self.addChild(link1)
        link1.addChild(link2)
        link2.addChild(link3)
        link3.addChild(link4)
        link4.addChild(link5)
        link5.addChild(link6)

        self.components = [link1, link2, link3, link4, link5, link6]

        for link in self.components:
            link.setDefaultAngle(20, link.uAxis)
            link.setRotateExtent(link.uAxis, -40, 20)
            link.setRotateExtent(link.vAxis, -20, 20)
            link.setRotateExtent(link.wAxis, 0, 0)

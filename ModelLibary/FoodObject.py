from Component import Component
from ModelLibary.DisplayableSphere import DisplayableSphere
from Point import Point
import ColorType as Ct
from Animation import Animation
from EnvironmentObject import EnvironmentObject
from Vivarium import Tank


class FoodObject(Component, Animation, EnvironmentObject):
    """
    A Linkage with animation enabled and is defined as an object in environment
    """
    components = None
    rotation_speed = None
    translation_speed = None

    def __init__(self, parent, position, species_id):
        super(FoodObject, self).__init__(position)
        self.contextParent = parent

        body = Component(Point((0, 0, 0)), DisplayableSphere(self.contextParent, 1, 1, [0.1, 0.1, 0.1]))
        body.setDefaultColor(Ct.MAROON)

        self.addChild(body)

        self.components = [body]

        self.translation_speed = Point([0, -1, 0]).normalize() * 0.01

        self.bound_center = Point((0, 0, 0))
        self.bound_radius = 0.1
        self.species_id = species_id

    def animationUpdate(self):
        for item in self.env_obj_list:
            if isinstance(item, Tank):
                # then this is our vivarium tank, do wall collision detection
                tank_d = item.tank_dimensions
                if not (self.current_position[1] + self.translation_speed[1]) > (-tank_d[1] / 2 + self.bound_radius):
                    self.translation_speed.coords[1] = 0

        self.current_position += self.translation_speed

        self.update()

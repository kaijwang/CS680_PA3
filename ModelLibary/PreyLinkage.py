"""
Create a single prey object, which include two moving wings and several fixed limbs.
Add periodic self-moving, collision detection with other preys and searching nearest foods.
Model always facing the marching direction.

:author: Kaijun Wang
:version: 2021.11.9
"""
import random

import numpy as np
from scipy.spatial.transform import Rotation as R
from scipy.spatial.transform import Slerp

from Component import Component
from MathUtils import calculateQuaternion, calculate_reflect_vector
from ModelLibary.DisplayableRoundCylinder import DisplayableRoundCylinder
from ModelLibary.DisplayableSphere import DisplayableSphere
from ModelLibary.FoodObject import FoodObject
from Point import Point
import ColorType as Ct
from Displayable import Displayable
from Animation import Animation
from EnvironmentObject import EnvironmentObject
from Quaternion import Quaternion
from Vivarium import Tank

class PreyLinkage(Component, Animation, EnvironmentObject):
    """
    A Linkage with animation enabled and is defined as an object in environment
    """
    components = None
    rotation_speed = None
    translation_speed = None

    def __init__(self, parent, position, species_id):
        super(PreyLinkage, self).__init__(position)
        self.contextParent = parent

        self.slerp_quaternions = []

        chest = Component(Point((0, 0, 0)), DisplayableSphere(self.contextParent, 1, 1, [0.35, 0.4, 0.4], True))
        chest.setDefaultColor(Ct.ORANGE)

        head = Component(Point((-0.5, 0, 0)),
                          DisplayableSphere(self.contextParent, 0.6, 0.6, [0.5, 0.4, 0.5]))
        head.setDefaultColor(Ct.BROWN)
        head.setDefaultAngle(30, head.wAxis)

        body = Component(Point((0.8, -0.2, 0)), DisplayableSphere(self.contextParent, 1, 1, [0.6, 0.4, 0.4], True))
        body.setDefaultColor(Ct.YELLOW)
        body.setDefaultAngle(-20, body.wAxis)

        wing_l = Component(Point((0.3, 0.35, 0.3)),
                  DisplayableRoundCylinder(self.contextParent, 0.8, 0.8, 0.05, 0.1, [0.4, 0.8, 0.5], True))
        wing_l.setDefaultColor(Ct.SILVER)
        wing_l.setDefaultAngle(110, wing_l.uAxis)
        wing_l.setDefaultAngle(60, wing_l.vAxis)
        wing_l.setDefaultAngle(90, wing_l.wAxis)

        wing_r = Component(Point((0.3, 0.35, -0.3)),
                           DisplayableRoundCylinder(self.contextParent, 0.8, 0.8, 0.05, 0.1, [0.4, 0.8, 0.5], True))
        wing_r.setDefaultColor(Ct.SILVER)
        wing_r.setDefaultAngle(70, wing_r.uAxis)
        wing_r.setDefaultAngle(60, wing_r.vAxis)
        wing_r.setDefaultAngle(90, wing_r.wAxis)

        self.addChild(chest)
        chest.addChild(head)
        chest.addChild(body)
        chest.addChild(wing_l)
        chest.addChild(wing_r)

        self.components = [chest, head, body]
        self.wing_l = wing_l
        self.wing_r = wing_r

        self.rotation_speed = []
        self.rotation_speed.append([0, 4, 2])
        # for comp in self.components:
        #     comp.setRotateExtent(comp.uAxis, 0, 35)
        #     comp.setRotateExtent(comp.vAxis, -45, 45)
        #     comp.setRotateExtent(comp.wAxis, -45, 45)
        #     self.rotation_speed.append([1, 0, 0])
        #
        self.translation_speed = Point([1, 0, 0]).normalize() * 0.01
        self.translation_speed = Point([random.random() - 0.5 for _ in range(3)]).normalize() * 0.01
        start_quaternion = calculateQuaternion([-1, 0, 0], self.translation_speed.coords)
        self.setPreRotation(start_quaternion.toMatrix())

        self.bound_center = Point((0, 0, 0))
        self.bound_radius = 0.1 * 2
        self.species_id = species_id

        # boundingSphere = Component(self.bound_center,
        #                            DisplayableSphere(parent, self.bound_radius / 0.2, self.bound_radius))
        # boundingSphere.setDefaultColor(Ct.YELLOW)
        # self.addChild(boundingSphere)

    def animationUpdate(self):
        ##### TODO 2: Animate your creature!
        # Requirements:
        #   1. Set reasonable joints limit for your creature
        #   2. The linkages should move back and forth in a periodic motion, as the creatures move about the vivarium.
        #   3. Your creatures should be able to move in 3 dimensions, not only on a plane.

        ##### TODO 3: Interact with the environment
        # Requirements:
        #   1. Your creatures should always stay within the fixed size 3D "tank". You should do collision detection
        #   between it and tank walls. When it hits with tank walls, it should turn and change direction to stay
        #   within the tank.
        #   2. Your creatures should have a prey/predator relationship. For example, you could have a bug being chased
        #   by a spider, or a fish eluding a shark. This means your creature should react to other creatures in the tank
        #       1. Use potential functions to change its direction based on other creatures’ location, their
        #       inter-creature distances, and their current configuration.
        #       2. You should detect collisions between creatures.
        #           1. Predator-prey collision: The prey should disappear (get eaten) from the tank.
        #           2. Collision between the same species: They should bounce apart from each other. You can use a
        #           reflection vector about a plane to decide the after-collision direction.
        #       3. You are welcome to use bounding spheres for collision detection.

        ##### TODO 4: Eyes on the road!
        # Requirements:
        #   1. CCreatures should face in the direction they are moving. For instance, a fish should be facing the
        #   direction in which it swims. Remember that we require your creatures to be movable in 3 dimensions,
        #   so they should be able to face any direction in 3D space.

        ##### BONUS 6: Group behaviors
        # Requirements:
        #   1. Add at least 5 creatures to the vivarium and make it possible for creatures to engage in group behaviors,
        #   for instance flocking together. This can be achieved by implementing the
        #   [Boids animation algorithms](http://www.red3d.com/cwr/boids/) of Craig Reynolds.


        # create period animation for creature joints

        ## Self Movement
        wing_vdirection = 1
        wing_wdirection = 1

        self.wing_l.rotate(-self.rotation_speed[0][1], self.wing_l.vAxis)
        self.wing_l.rotate(self.rotation_speed[0][2], self.wing_l.wAxis)

        self.wing_r.rotate(-self.rotation_speed[0][1], self.wing_r.vAxis)
        self.wing_r.rotate(-self.rotation_speed[0][2], self.wing_r.wAxis)

        if self.wing_l.vAngle in [20, 60]:  # rotation reached the limit
            wing_vdirection = -1

        if self.wing_l.wAngle in [90, 110]:  # rotation reached the limit
            wing_wdirection = -1

        self.rotation_speed[0][1] *= wing_vdirection
        self.rotation_speed[0][2] *= wing_wdirection

        ### Translation in Tank
        pre_speed = [*self.translation_speed.coords]

        food_pos = []
        for item in self.env_obj_list:
            # Find Food
            if isinstance(item, FoodObject):
                food_pos.append(item.current_position)
                if np.linalg.norm((item.current_position - self.current_position).coords) < item.bound_radius + self.bound_radius:
                    item.species_id = 0

        sortedFood = sorted(food_pos, key=lambda pos: np.linalg.norm((self.current_position - pos).coords))

        if len(sortedFood) > 0:
            self.translation_speed = Point((sortedFood[0] - self.current_position).coords).normalize() * 0.01

        for item in self.env_obj_list:
            # Avoid encounter predator
            if item.species_id == 1:
                if np.linalg.norm((item.current_position - self.current_position).coords) < 0.1 * 10:
                    # self.translation_speed = (self.current_position - item.current_position).normalize() * 0.01
                    self.translation_speed = Point(calculate_reflect_vector(pre_speed, (
                                item.current_position - self.current_position).coords)).normalize() * 0.01

            # Avoid prey collision
            elif isinstance(item, PreyLinkage) and not item.species_id == self.species_id:
                if np.linalg.norm((item.current_position - self.current_position).coords) < 2*self.bound_radius:
                    self.translation_speed = Point(calculate_reflect_vector(pre_speed, (
                            item.current_position - self.current_position).coords)).normalize() * 0.01

        for item in self.env_obj_list:
            if isinstance(item, Tank):
                # then this is our vivarium tank, do wall collision detection
                tank_d = item.tank_dimensions
                if not ((tank_d[0] / 2 - self.bound_radius) >
                        (self.current_position[0] + self.translation_speed[0]) >
                        (-tank_d[0] / 2 + self.bound_radius)):
                    self.translation_speed.coords[0] *= -1
                if not ((tank_d[1] / 2 - self.bound_radius) >
                        (self.current_position[1] + self.translation_speed[1]) >
                        (-tank_d[1] / 2 + self.bound_radius)):
                    self.translation_speed.coords[1] *= -1
                if not ((tank_d[2] / 2 - self.bound_radius) >
                        (self.current_position[2] + self.translation_speed[2]) >
                        (-tank_d[2] / 2 + self.bound_radius)):
                    self.translation_speed.coords[2] *= -1

        self.current_position += self.translation_speed

        if len(self.slerp_quaternions) > 3:
            self.setPreRotation(Quaternion(*self.slerp_quaternions[0]).toMatrix())
            self.slerp_quaternions = np.delete(self.slerp_quaternions, 0, axis=0)
            self.update()
            return

        ### Change Facing Direction
        if not np.array_equal(pre_speed, self.translation_speed.coords):
            pre_quaternion = calculateQuaternion([-1, 0, 0], pre_speed)
            rotation = calculateQuaternion([-1, 0, 0], self.translation_speed.coords)

            key_rots = R.from_quat([[pre_quaternion.s, *pre_quaternion.v], [rotation.s, *rotation.v]])
            key_times = [0, 5]
            slerp = Slerp(key_times, key_rots)

            times = range(0, 6)
            interp_rots = slerp(times)
            self.slerp_quaternions = interp_rots[1:].as_quat()

        if len(self.slerp_quaternions) > 0:
            self.setPreRotation(Quaternion(*self.slerp_quaternions[0]).toMatrix())
            self.slerp_quaternions = np.delete(self.slerp_quaternions, 0, axis=0)
            # self.current_position -= self.translation_speed

        self.update()

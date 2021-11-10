"""
Create a single predator object, which used the model in PA2.
Add periodic self-moving, collision detection with walls and searching nearest prey.
Model always facing the marching direction.

:author: Kaijun Wang
:version: 2021.11.9
"""

import random

import numpy as np
from scipy.spatial.transform import Rotation as R
from scipy.spatial.transform import Slerp

from Component import Component
from MathUtils import calculateQuaternion
from ModelLibary.BodyLinkage import BodyLinkage
from ModelLibary.HeadLinkage import HeadLinkage
from ModelLibary.LegLinkage import LegLinkage
from ModelLibary.TailLinkage import TailLinkage
from ModelLibary.WingLinkage import WingLinkage
from Point import Point
from Animation import Animation
from EnvironmentObject import EnvironmentObject
from Quaternion import Quaternion
from Vivarium import Tank
from ModelLibary.PreyLinkage import PreyLinkage


class PredatorLinkage(Component, Animation, EnvironmentObject):
    """
    A Linkage with animation enabled and is defined as an object in environment
    """
    components = None
    rotation_speed = None
    translation_speed = None

    body = None
    head = None
    wing_l = None
    wing_r = None
    leg_l = None
    leg_r = None
    tail = None

    def __init__(self, parent, position):
        super(PredatorLinkage, self).__init__(position)

        self.slerp_quaternions = []
        body = BodyLinkage(parent, Point((0, 0, 0)))
        tail = TailLinkage(parent, Point((0, 0.1, 0.5)))
        leg_l = LegLinkage(parent, Point((0.2, -0.1, 0)))
        leg_r = LegLinkage(parent, Point((-0.2, -0.1, 0)))

        wing_l = WingLinkage(parent, Point((0.3, 0, 0)))
        wing_l.components[0].setRotateExtent(wing_l.components[0].uAxis, -240, -120)
        wing_l.components[0].setRotateExtent(wing_l.components[0].vAxis, 0, 60)
        wing_l.components[0].setRotateExtent(wing_l.components[0].wAxis, -60, 30)

        wing_r = WingLinkage(parent, Point((-0.3, 0, 0)))
        wing_r.components[0].setDefaultAngle(60, wing_r.components[0].uAxis)
        wing_r.components[0].setRotateExtent(wing_r.components[0].uAxis, -60, 60)
        wing_r.components[0].setRotateExtent(wing_r.components[0].wAxis, -30, 60)
        wing_r.components[0].setDefaultAngle(-170, wing_r.components[0].vAxis)
        wing_r.components[0].setRotateExtent(wing_r.components[0].vAxis, -180, -120)

        head = HeadLinkage(parent, Point((0, 0, -1.1)))

        self.addChild(body)
        body.components[-1].addChild(tail)
        body.components[-1].addChild(leg_l)
        body.components[-1].addChild(leg_r)
        body.components[-1].addChild(wing_l)
        body.components[-1].addChild(wing_r)
        body.components[0].addChild(head)

        self.components = body.components + tail.components + leg_l.components + leg_r.components \
                          + wing_l.components + wing_r.components + head.components

        self.neck = body.components[0]
        self.body = body.components[-1]
        self.head = head.components[0]
        self.wing_l = wing_l.components[0]
        self.wing_r = wing_r.components[0]
        self.leg_l = leg_l.components[0]
        self.leg_r = leg_r.components[0]
        self.tail = tail

        self.rotation_speed = []
        self.rotation_speed.append([1, 0, 0])
        self.rotation_speed.append([0, 0.5, 1.5])
        # for comp in self.components:
        #     comp.setRotateExtent(comp.uAxis, 0, 35)
        #     comp.setRotateExtent(comp.vAxis, -45, 45)
        #     comp.setRotateExtent(comp.wAxis, -45, 45)
        #     self.rotation_speed.append([1, 0, 0])
        #
        # self.translation_speed = Point([1, 0, 0]).normalize() * 0.01
        self.translation_speed = Point([random.random() - 0.5 for _ in range(3)]).normalize() * 0.01
        start_quaternion = calculateQuaternion([-1, 0, 0], self.translation_speed.coords)
        self.setPreRotation(start_quaternion.toMatrix())

        self.bound_center = Point((0, 0, 0))
        self.bound_radius = 0.1 * 6
        self.species_id = 1

        # boundingSphere = Component(self.bound_center,
        #           DisplayableSphere(parent, self.bound_radius/0.3, self.bound_radius))
        # boundingSphere.setDefaultColor(Ct.LIGHTCORAL)
        # self.addChild(boundingSphere)

    def animationUpdate(self):
        ##### TODO 2: Animate your creature!
        # Requirements:
        #   1. Set reasonable joints limit for your creature
        #   2. The linkages should move back and forth in a periodic motion, as the creatures move about the vivarium.
        #   3. Your creatures should be able to move in 3 dimensions, not only on a plane.

        # create period animation for creature joints

        ### Self Movement
        tail_udirection = 1
        wing_vdirection = 1
        wing_wdirection = 1

        for i, tail_part in enumerate(self.tail.components):
            tail_part.rotate(self.rotation_speed[0][0], tail_part.uAxis)
            if tail_part.uAngle in [-20, 20]:  # rotation reached the limit
                tail_udirection = -1

        self.wing_l.rotate(self.rotation_speed[1][1], self.wing_l.vAxis)
        self.wing_l.rotate(-self.rotation_speed[1][2], self.wing_l.wAxis)

        self.wing_r.rotate(self.rotation_speed[1][1], self.wing_r.vAxis)
        self.wing_r.rotate(self.rotation_speed[1][2], self.wing_r.wAxis)

        if self.wing_l.vAngle in [10, 30]:  # rotation reached the limit
            wing_vdirection = -1

        if self.wing_l.wAngle in [-60, 0]:  # rotation reached the limit
            wing_wdirection = -1

        self.rotation_speed[0][0] *= tail_udirection
        self.rotation_speed[1][1] *= wing_vdirection
        self.rotation_speed[1][2] *= wing_wdirection

        ### Translation in Tank
        pre_speed = [*self.translation_speed.coords]

        food_pos = []
        for item in self.env_obj_list:
            # Find Food
            if isinstance(item, PreyLinkage):
                food_pos.append(item.current_position)

        sortedFood = sorted(food_pos, key=lambda pos: np.linalg.norm((self.current_position - pos).coords))

        if len(sortedFood) > 0:
            self.translation_speed = Point((sortedFood[0] - self.current_position).coords).normalize() * 0.01

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

            # If encounter a prey, eat it
            elif isinstance(item, PreyLinkage):
                if (self.bound_radius + item.bound_radius) > np.linalg.norm((self.current_position -
                                                                             item.current_position).coords):
                    item.species_id = 0

        self.current_position += self.translation_speed

        ### Change Facing Direction
        if not np.array_equal(pre_speed, self.translation_speed.coords):
            pre_quaternion = calculateQuaternion([-1, 0, 0], pre_speed)
            rotation = calculateQuaternion([-1, 0, 0], self.translation_speed.coords)

            key_rots = R.from_quat([[pre_quaternion.s, *pre_quaternion.v], [rotation.s, *rotation.v]])
            key_times = [0, 9]
            slerp = Slerp(key_times, key_rots)

            times = range(0, 10)
            interp_rots = slerp(times)
            self.slerp_quaternions = interp_rots[1:].as_quat()

        if len(self.slerp_quaternions) > 0:
            self.setPreRotation(Quaternion(*self.slerp_quaternions[0]).toMatrix())
            self.slerp_quaternions = np.delete(self.slerp_quaternions, 0, axis=0)
            self.current_position -= self.translation_speed

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

        self.update()

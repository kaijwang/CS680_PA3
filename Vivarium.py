"""
All creatures should be added to Vivarium. Some help functions to add/remove creature are defined here.
Added functions to generate a single prey or several feeds.

:author: micou(Zezhou Sun), Kaijun Wang
:version: 2021.11.9
"""
import random

from Point import Point
from Component import Component
from Animation import Animation
from ModelTank import Tank
from EnvironmentObject import EnvironmentObject
from ModelLibary.PredatorLinkage import PredatorLinkage
from ModelLibary.PreyLinkage import PreyLinkage
from ModelLibary.FoodObject import FoodObject

class Vivarium(Component, Animation):
    """
    The Vivarium for our animation
    """
    components = None  # List
    parent = None  # class that have current context
    tank = None
    tank_dimensions = None
    cur_id = None

    ##### BONUS 5(TODO 5 for CS680 Students): Feed your creature
    # Requirements:
    #   Add chunks of food to the vivarium which can be eaten by your creatures.
    #     * When ‘f’ is pressed, have a food particle be generated at random within the vivarium.
    #     * Be sure to draw the food on the screen with an additional model. It should drop slowly to the bottom of
    #     the vivarium and remain there within the tank until eaten.
    #     * The food should disappear once it has been eaten. Food is eaten by the first creature that touches it.

    def __init__(self, parent):
        self.parent = parent

        self.addPreyFlag = False
        self.tank_dimensions = [4, 4, 4]
        tank = Tank(parent, self.tank_dimensions)
        super(Vivarium, self).__init__(Point((0, 0, 0)))

        # Build relationship
        self.addChild(tank)
        self.tank = tank

        # Store all components in one list, for us to access them later
        self.components = [tank]

        # self.addNewObjInTank(Linkage(parent, Point((0, 0, 0))))
        predator = PredatorLinkage(parent, Point((0, 0, 0)))
        predator.setDefaultScale([0.3, 0.3, 0.3])
        self.addNewObjInTank(predator)

        self.cur_id = 2
        for i in range(0, 5):
            self.generatePrey()

    def animationUpdate(self):
        """
        Update all creatures in vivarium
        """
        for c in self.components[::-1]:
            if c.species_id == 0:
                self.delObjInTank(c)
                # self.tank.update()
            if isinstance(c, Animation):
                c.animationUpdate()

    def generatePrey(self):
        """
        Generate a new prey obj
        """
        prey = PreyLinkage(self.parent,
                           Point((random.uniform(-1.8, 1.8), random.uniform(-1.8, 1.8), random.uniform(-1.8, 1.8))),
                           self.cur_id)
        prey.setDefaultScale([0.2, 0.2, 0.2])
        self.cur_id += 1
        self.addNewObjInTank(prey)
        prey.initialize()

    def generateFood(self):
        """
        Randomly generate food
        """
        for i in range(0, 10):
            food = FoodObject(self.parent,
                              Point((random.uniform(-1.8, 1.8), random.uniform(1.6, 1.8), random.uniform(-1.8, 1.8))),
                              self.cur_id)
            self.cur_id += 1
            self.addNewObjInTank(food)
            food.initialize()

    def delObjInTank(self, obj):
        if isinstance(obj, Component):
            self.tank.children.remove(obj)
            self.components.remove(obj)
            del obj

    def addNewObjInTank(self, newComponent):
        if isinstance(newComponent, Component):
            self.tank.addChild(newComponent)
            self.components.append(newComponent)
        if isinstance(newComponent, EnvironmentObject):
            # add environment components list reference to this new object's
            newComponent.env_obj_list = self.components


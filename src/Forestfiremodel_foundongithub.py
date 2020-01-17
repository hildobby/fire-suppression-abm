import random

import numpy as np

import math

import matplotlib.pyplot as plt

from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
# from mesa.datacollection import DataCollector
from Datacollector_v2 import DataCollector
from mesa.batchrunner import BatchRunner
from random import randint
from agent import *

# defines the model


class ForestFire(Model):
    '''
    Simple Forest Fire model.
    '''

    def __init__(
            self,
            height,
            width,
            density,
            temperature,
            truck_strategy,
            river_number,
            river_width,
            random_fires,
            num_firetruck,
            wind,
            vision,
            max_speed):
        super().__init__()
        '''
        Create a new forest fire model.

        Args:
            height, width: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        '''
        # Initialize model parameters
        self.height = height
        self.width = width
        self.density = density

        self.river_length = width
        # Will suck when set to higher than 2
        self.river_width = river_width

        self.temperature = temperature

        self.n_agents = 0
        self.agents = []
        self.initial_tree = height * width * density - self.river_length * self.river_width

        self.river_size = width

        # Set up model objects
        self.schedule_TreeCell = RandomActivation(self)
        self.schedule_FireTruck = RandomActivation(self)
        self.schedule = RandomActivation(self)

        # Set the wind
        self.wind = (randint(-1, 1), randint(-1, 1))
        self.grid = MultiGrid(height, width, torus=False)

        self.init_river(self.river_size)

        # agent_reporters={TreeCell: {"Life bar": "life_bar"}})

        self.init_vegetation(TreeCell, self.initial_tree)

        for i in range(len(self.agents)):
            self.schedule_TreeCell.add(self.agents[i])
            self.schedule.add(self.agents[i])

        self.init_firefighters(Firetruck, num_firetruck, truck_strategy, vision, max_speed)

        self.random_fires = random_fires
        self.temperature = temperature
        self.num_firetruck = num_firetruck
        self.truck_strategy = truck_strategy
        self.agents[10].condition = "On Fire"

        # initiate the datacollector
        self.dc = DataCollector(self,
                                model_reporters={
                                    "Fine": lambda m: self.count_type(m, "Fine"),
                                    "On Fire": lambda m: self.count_type(m, "On Fire"),
                                    "Burned Out": lambda m: self.count_type(m, "Burned Out"),
                                    "Extinguished": lambda m: self.count_extinguished_fires(m)
                                },

                                # tables={"Life bar": "life_bar", "Burning rate": "burning_rate"},

                                agent_reporters={TreeCell: {"Life bar": "life_bar", "Burning rate": "burning_rate"},
                                                 Firetruck: {"Condition": "condition"}})

        self.running = True
        self.dc.collect(self, [TreeCell, Firetruck])
        self.wind_direction = wind[0]
        self.wind_speed = wind[1]

    def init_river(self, n):
        '''
        Creating a river
        '''
        if self.river_width == 0:
            pass
        else:
            x = -1
            y = random.randrange(self.height)
            for i in range(int(n)):
                x += 1
                y += random.randint(-1, 1)
                while y <= 0 or y >= self.height or not self.grid.is_cell_empty((x, y)):
                    y += random.randint(-1, 1)
                self.new_river(RiverCell, (x, y))
                for j in range(self.river_width - 1):
                    y += random.choice([-1, 1])
                    while y <= 0 or y >= self.height or not self.grid.is_cell_empty((x, y)):
                        y += random.choice([-1, 1])
                    self.new_river(RiverCell, (x, y))

    def init_vegetation(self, agent_type, n):
        '''
        Creating trees
        '''
        for i in range(int(n)):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            while not self.grid.is_cell_empty((x, y)):
                x = random.randrange(self.width)
                y = random.randrange(self.height)
            self.new_agent(agent_type, (x, y))

    def init_firefighters(self, agent_type, num_firetruck, truck_strategy, vision, max_speed):
        for i in range(num_firetruck):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            firetruck = self.new_firetruck(Firetruck, (x, y), truck_strategy, vision, max_speed)
            self.schedule_FireTruck.add(firetruck)
            self.schedule.add(firetruck)

    def step(self):
        '''
        Advance the model by one step.
        '''

        self.schedule_TreeCell.step()
        self.schedule_FireTruck.step()

        self.dc.collect(self, [TreeCell, Firetruck])

        if self.random_fires:
            num_fine_trees = self.count_type(self, "Fine")
            if self.agents[num_fine_trees].condition == "Fine":
                self.randomfire(self, self.temperature, num_fine_trees)

        # Halt if no more fire
        if self.count_type(self, "On Fire") == 0:
            print(self.count_type(self, "On Fire"))
            print(" \n \n Fire is gone ! \n \n")
            self.running = False

    @staticmethod
    def randomfire(self, temperature, num_fine_trees):
        for i in range(0, num_fine_trees):
            if (random.random() < (math.exp(temperature / 10) / 600.0)):
                if (self.agents[num_fine_trees].condition == "Fine"):
                    self.agents[num_fine_trees].condition = "On Fire"

    @staticmethod
    def count_type(model, tree_condition):
        '''
        Helper method to count trees in a given condition in a given model.
        '''
        count = 0
        for tree in model.schedule_TreeCell.agents:

            if tree.condition == tree_condition:
                count += 1
        return count

    @staticmethod
    def count_extinguished_fires(model):
        '''
        Helper method to count extinguished fires in a given condition in a given model.
        '''

        count = 0
        for firetruck in model.schedule_FireTruck.agents:
            count += firetruck.extinguished

        return count

    def new_agent(self, agent_type, pos):
        '''
        Method that enables us to add agents of a given type.
        '''
        self.n_agents += 1

        # Create a new agent of the given type
        new_agent = agent_type(self, self.n_agents, pos)

        # Place the agent on the grid
        self.grid.place_agent(new_agent, pos)

        # And add the agent to the model so we can track it
        self.agents.append(new_agent)

        return new_agent

    def new_firetruck(self, agent_type, pos, truck_strategy, vision, max_speed):
        '''
        Method that enables us to add agents of a given type.
        '''
        self.n_agents += 1

        # Create a new agent of the given type
        new_agent = agent_type(self, self.n_agents, pos, truck_strategy, vision, max_speed)

        # Place the agent on the grid
        self.grid.place_agent(new_agent, pos)

        # And add the agent to the model so we can track it
        self.agents.append(new_agent)

        return new_agent

    def new_river(self, agent_type, pos):

        # Create a new agent of the given type
        new_agent = agent_type(self, self.n_agents, pos)

        # Place the agent on the grid
        self.grid.place_agent(new_agent, pos)

        # And add the agent to the model so we can track it

        return new_agent

    def remove_agent(self, agent):
        '''
        Method that enables us to remove passed agents.
        '''
        self.n_agents -= 1

        # Remove agent from grid
        self.grid.remove_agent(agent)

        # Remove agent from model
        self.agents.remove(agent)


# To be used if you want to run the model without the visualiser:
temperature = 20
truck_strategy = 'Goes to the closest fire'
density = 0.6
width = 100
height = 100
num_firetruck = 30
vision = 100
max_speed = 2
river_number = 0
river_width = 0
random_fires = 1
# wind[0],wind[1]=[direction,speed]
wind = [1, 2]
fire = ForestFire(
    height,
    width,
    density,
    temperature,
    truck_strategy,
    river_number,
    river_width,
    random_fires,
    num_firetruck,
    wind,
    vision,
    max_speed)
fire.run_model()

results = fire.dc.get_model_vars_dataframe()
agent_variable = fire.dc.get_agent_vars_dataframe()
results_firetrucks = fire.dc.get_model_vars_dataframe()

print(agent_variable[0])
print(agent_variable[1])

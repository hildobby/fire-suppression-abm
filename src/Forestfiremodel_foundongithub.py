import random

import numpy as np

import matplotlib.pyplot as plt

from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner

from src.agent import *

# defines the model
class ForestFire(Model):
    '''
    Simple Forest Fire model.
    '''

    def __init__(self, height, width, density):
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

        self.n_agents = 0
        self.agents = []
        self.initial_tree = height * width * density

        # Set up model objects
        self.schedule_TreeCell = RandomActivation(self)

        self.grid = MultiGrid(height, width, torus=False)
        self.dc = DataCollector({"Fine": lambda m: self.count_type(m, "Fine"),
                                 "On Fire": lambda m: self.count_type(m, "On Fire"),
                                 "Burned Out": lambda m: self.count_type(m, "Burned Out")})

        self.init_population(TreeCell, self.initial_tree)
        for i in range(len(self.agents)):
            self.schedule_TreeCell.add(self.agents[i])
        self.agents[10].condition = "On Fire"
        self.running = True
        self.dc.collect(self)

    def init_population(self, agent_type, n):
        '''
        Method that provides an easy way of making a bunch of agents at once.
        '''
        for i in range(int(n)):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            self.new_agent(agent_type, (x, y))


    def step(self):
        '''
        Advance the model by one step.
        '''

        self.schedule_TreeCell.step()
        for agent in list(self.agents):
            agent.step()
        self.dc.collect(self)
        # Halt if no more fire

        if self.count_type(self, "On Fire") == 0:
            self.running = False

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

    def remove_agent(self, agent):
        '''
        Method that enables us to remove passed agents.
        '''
        self.n_agents -= 1

        # Remove agent from grid
        self.grid.remove_agent(agent)

        # Remove agent from model
        self.agents.remove(agent)






density = 0.6
width = 100
height = 100
fire = ForestFire(width, height, density)
fire.run_model()
results = fire.dc.get_model_vars_dataframe()
print(results)
results.plot()
plt.show()
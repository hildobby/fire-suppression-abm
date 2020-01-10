#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Created on Wed Jan  8 15:30:03 2020
This code was implemented by Louis Weyland & Robin van den Berg, Hildebert Mouilé & Wiebe Jelsma

"""
from mesa import Agent
# Defines the tree agents


class TreeCell(Agent):
    '''
    A tree cell.

    Attributes:
        x, y: Grid coordinates
        condition: Can be "Fine", "On Fire", or "Burned Out"
        unique_id: (x,y) tuple.

    unique_id isn't strictly necessary here, but it's good practice to give one to each
    agent anyway.
    '''

    def __init__(self, model, unique_id, pos):
        '''
        Create a new tree.
        Args:
            pos: The tree's coordinates on the grid. Used as the unique_id
        '''
        super().__init__(unique_id, model)
        self.pos = pos
        self.unique_id = unique_id
        self.condition = "Fine"

    def step(self):
        '''
        If the tree is on fire, spread it to fine trees nearby.
        '''
        if self.condition == "On Fire":
            neighbors = self.model.grid.get_neighbors(self.pos, moore=True)
            for neighbor in neighbors:
                if neighbor.condition == "Fine":
                    neighbor.condition = "On Fire"
            self.condition = "Burned Out"

    def get_pos(self):
        return self.pos

# defines a random walker class


class Walker(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)

        self.pos = pos

    def random_move(self):
        '''
        This method should get the neighbouring cells (Moore's neighbourhood), select one, and move the agent to this cell.
        '''
        cell_list = self.model.grid.get_neighborhood(self.pos, moore=True)
        self.model.grid.move_agent(
            self, cell_list[random.randint(0, len(cell_list) - 1)])

    def guided_move(self):
        cell_list = self.model.grid.get_neighborhood(
            self.pos, moore=True, radius=3)
        neighbors_list = self.model.grid.get_neighbors(
            self.pos, moore=True, radius=3)


class Firetruck(Walker):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)

    def step(self):
        '''
        This method should move the Sheep using the `random_move()` method implemented earlier, then conditionally reproduce.
        '''
        self.random_move()

    def extinguish(self):
        neighbors_list = self.model.grid.get_neighbors(
            self.pos, moore=True, radius=1)
        for tree in neighbors_list:
            if tree.condition == "On Fire":
                tree.condition = "Burned Out"

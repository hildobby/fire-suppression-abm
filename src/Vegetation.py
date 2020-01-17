#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 15:30:03 2020

This code was implemented by
Louis Weyland & Robin van den Berg, Philippe Nicolau, Hildebert Mouilé & Wiebe Jelsma

"""
import random
from mesa import Agent


class TreeCell(Agent):

    '''
    A tree cell.

    Attributes:
        x, y: Grid coordinates
        condition: Can be "Fine", "On Fire", or "Burned Out"
        unique_id: (x,y) tuple.
        life_bar : looks at the life bar of the tree

    unique_id isn't strictly necessary here,
    but it's good practice to give one to each
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
        self.life_bar = 100       # give the tree a life bar
        self.burning_rate = 20
        self.probability = 0.5

        self.speed = 0.47

    def step(self):
        '''
        If the tree is on fire, spread it to fine trees nearby.
        '''
        if self.condition == "On Fire":
            neighbors = self.model.grid.get_neighbors(self.pos, moore=True)
            for neighbor in neighbors:

               if isinstance(neighbor, TreeCell) and neighbor.condition == "Fine":


                           # Look at the position of the neighbor and the wind which to calculate the probability
                           if self.pos[0]<neighbor.pos[0] and self.pos[1]==neighbor.pos[1]:
                                if random.uniform(0,1)< self.probability + (self.model.wind_dir[0]*self.model.wind_strength):
                                    neighbor.condition="On Fire"
                                    break
                           elif self.pos[0]>neighbor.pos[0] and self.pos[1]==neighbor.pos[1]:
                                if random.uniform(0,1)< self.probability - (self.model.wind_dir[0]*self.model.wind_strength):
                                    neighbor.condition = "On Fire"
                                    break
                           elif self.pos[0] == neighbor.pos[0] and self.pos[1] < neighbor.pos[1]:
                                if random.uniform(0,1)< self.probability + (self.model.wind_dir[1]*self.model.wind_strength):
                                    neighbor.condition = "On Fire"
                                    break
                           elif self.pos[0] == neighbor.pos[0] and self.pos[1] < neighbor.pos[1]:
                                    if random.uniform(0, 1) < self.probability - (self.model.wind_dir[1] *self.model.wind_strength):
                                        neighbor.condition = "On Fire"
                                    break
                           elif self.pos[0] < neighbor.pos[0] and self.pos[1] < neighbor.pos[1]:
                               if random.uniform(0, 1) < self.probability + (self.model.wind_dir[0] * self.model.wind_strength*self.model.wind_dir[1]):
                                   neighbor.condition = "On Fire"
                                   break
                           elif self.pos[0] < neighbor.pos[0] and self.pos[1] > neighbor.pos[1]:
                               if random.uniform(0, 1) < self.probability - (self.model.wind_dir[1] * self.model.wind_strength *self.model.wind_dir[0]):
                                   neighbor.condition = "On Fire"
                                   break
                           elif self.pos[0] > neighbor.pos[0] and self.pos[1] < neighbor.pos[1]:
                               if random.uniform(0, 1) < self.probability - (self.model.wind_dir[0] * self.model.wind_strength* self.model.wind_dir[1]):
                                   neighbor.condition = "On Fire"
                                   break
                           elif self.pos[0] > neighbor.pos[0] and self.pos[1] > neighbor.pos[1]:
                               if random.uniform(0, 1) < self.probability - (self.model.wind_dir[0] * self.model.wind_strength *self.model.wind_dir[0]):
                                   neighbor.condition = "On Fire"
                                   break


            # if on fire reduce life_bar
            if self.life_bar != 0:
                self.life_bar -= self.burning_rate
            else:
                self.condition = "Burned Out"

    def get_pos(self):
        return self.pos

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 15:30:03 2020

This code was implemented by
Louis Weyland & Robin van den Berg, Philippe Nicolau, Hildebert Mouilé & Wiebe Jelsma

"""
import sys
sys.path.append('../')

from environment.vegetation import TreeCell
import random
from mesa import Agent


class Rain(Agent):
    def __init__(self, model, unique_id, pos):
        '''
        Create one cell of rain.
        Args:
        '''
        super().__init__(unique_id, model)
        self.pos = pos
        self.unique_id = unique_id
        self.condition = "Rain"

    def get_pos(self):
        return self.pos

    def step(self):
        '''
        If the tree is on fire, spread it to fine trees nearby.
        '''
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True)
        for neighbor in neighbors:

            if isinstance(neighbor, TreeCell) and neighbor.life_bar <= 80:
                neighbor.life_bar += 20
                if neighbor.condition == "Burned Out" or neighbor.condition == "On Fire":
                    neighbor.condition = "Fine"

        self.random_move()

    def random_move(self):
        '''
        This method should get the neighbouring cells (Moore's neighbourhood)
        select one, and move the agent to this cell.
        '''

        cell_list = self.model.grid.get_neighborhood(self.pos, moore=True)

        # for cell in cell_list:
        #     if self.model.grid.get_cell_list_contents(cell):
        #         if isinstance(self.model.grid.get_cell_list_contents(cell)[0], RiverCell):
        #             cell_list.remove(cell)

        new_pos = cell_list[random.randint(0, len(cell_list) - 1)]

        self.model.grid.move_agent(self, new_pos)

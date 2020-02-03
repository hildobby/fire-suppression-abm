#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 15:30:03 2020

This code was implemented by
Louis Weyland, Robin van den Berg, Philippe Nicolau, Hildebert Mouilé & Wiebe Jelsma

"""
from mesa import Agent


class RiverCell(Agent):
    def __init__(self, model, unique_id, pos):
        '''
        Create one cell of a river.
        Args:
            pos: The tree's coordinates on the grid. Used as the unique_id
        '''
        super().__init__(unique_id, model)
        self.pos = pos
        self.unique_id = unique_id
        self.condition = "Plenty"

    def get_pos(self):
        return self.pos

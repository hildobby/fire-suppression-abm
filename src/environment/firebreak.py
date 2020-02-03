#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 17:54:44 2020

This code was implemented by
Louis Weyland, Robin van den Berg, Philippe Nicolau, Hildebert Mouilé & Wiebe Jelsma

"""
from mesa import Agent


class BreakCell(Agent):
    def __init__(self, model, unique_id, pos):
        '''
        A firebreak cell.
        Args:
            position & spread probability
        '''
        super().__init__(unique_id, model)
        self.pos = pos
        self.unique_id = unique_id
        self.condition = "Firebreak"

    def get_pos(self):
        return self.pos

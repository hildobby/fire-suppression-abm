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
                    if self.pos[0] < neighbor.pos[0] and self.pos[1] == neighbor.pos[1]:
                        if random.uniform(0, 1) < self.probability + (self.model.wind[0] * self.speed):
                            neighbor.condition = "On Fire"
                            break
                    elif self.pos[0] > neighbor.pos[0] and self.pos[1] == neighbor.pos[1]:
                        if random.uniform(0, 1) < self.probability - (self.model.wind[0] * self.speed):
                            neighbor.condition = "On Fire"
                            break
                    elif self.pos[0] == neighbor.pos[0] and self.pos[1] < neighbor.pos[1]:
                        if random.uniform(0, 1) < self.probability + (self.model.wind[1] * self.speed):
                            neighbor.condition = "On Fire"
                            break
                    elif self.pos[0] == neighbor.pos[0] and self.pos[1] < neighbor.pos[1]:
                        if random.uniform(0, 1) < self.probability - (self.model.wind[1] * self.speed):
                            neighbor.condition = "On Fire"
                        break
                    elif self.pos[0] < neighbor.pos[0] and self.pos[1] < neighbor.pos[1]:
                        if random.uniform(0, 1) < self.probability + \
                                (self.model.wind[0] * self.speed * self.model.wind[0]):
                            neighbor.condition = "On Fire"
                            break
                    elif self.pos[0] < neighbor.pos[0] and self.pos[1] > neighbor.pos[1]:
                        if random.uniform(0, 1) < self.probability - \
                                (self.model.wind[1] * self.speed * self.model.wind[0]):
                            neighbor.condition = "On Fire"
                            break
                    elif self.pos[0] > neighbor.pos[0] and self.pos[1] < neighbor.pos[1]:
                        if random.uniform(0, 1) < self.probability - \
                                (self.model.wind[0] * self.speed * self.model.wind[1]):
                            neighbor.condition = "On Fire"
                            break
                    elif self.pos[0] > neighbor.pos[0] and self.pos[1] > neighbor.pos[1]:
                        if random.uniform(0, 1) < self.probability - \
                                (self.model.wind[0] * self.speed * self.model.wind[0]):
                            neighbor.condition = "On Fire"
                            break

            # if on fire reduce life_bar
            if self.life_bar != 0:
                self.life_bar -= self.burning_rate
            else:
                self.condition = "Burned Out"

    def get_pos(self):
        return self.pos

# defines a random walker class


class Walker(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)

        self.pos = pos
        self.unique_id = unique_id

    def random_move(self):
        '''
        This method should get the neighbouring cells (Moore's neighbourhood)
        select one, and move the agent to this cell.
        '''

        cell_list = self.model.grid.get_neighborhood(self.pos, moore=True)
        new_pos = cell_list[random.randint(0, len(cell_list) - 1)]
        self.model.grid.move_agent(self, new_pos)

    def biggestfire_move(self):
        '''
        This method should get the neighbouring cells (Moore's neighbourhood)
        select the fire with the biggest life bar and move the fire truck to this position.
        It also checks if the position is closeby, otherwise it does not go there
        '''
        # find hot trees in neighborhood
        fire_intheneighborhood = False
        for i in [25, 50, 100]:
            limited_vision = int(self.vision * i / 100.)
            # find hot trees in neighborhood
            neighbors_list = self.model.grid.get_neighbors(
                self.pos, moore=True, radius=limited_vision)

            neighbors_list = [x for x in neighbors_list if x.condition == "On Fire"]

            # find closest fire
            min_distance = limited_vision**2
            min_life_bar = 0
            for neighbor in neighbors_list:
                current_life_bar = neighbor.life_bar
                distance = abs(neighbor.pos[0]**2 - self.pos[0]**2) + abs(neighbor.pos[1]**2 - self.pos[1]**2)
                if current_life_bar >= min_life_bar and distance <= min_distance:
                    min_distance = distance
                    min_life_bar = current_life_bar
                    closest_neighbor = neighbor
                    fire_intheneighborhood = True
            if fire_intheneighborhood:
                break

        # move toward fire if it is actually in the neighborhood
        if fire_intheneighborhood:

            # find how many places to move to reach the closest fire
            places_to_move_y = closest_neighbor.pos[1] - self.pos[1]
            places_to_move_x = closest_neighbor.pos[0] - self.pos[0]

            if self.pos[0] == 1 or self.pos[0] == self.model.width - 2 or self.pos[1] == 1 or \
                    self.pos[1] == self.model.height - 2:
                speed = 1
            else:
                speed = self.max_speed

            # choose step
            if places_to_move_x > 0 and places_to_move_y > 0:
                self.model.grid.move_agent(self, (self.pos[0] + speed, self.pos[1] + speed))
            elif places_to_move_x < 0 and places_to_move_y < 0:
                self.model.grid.move_agent(self, (self.pos[0] - speed, self.pos[1] - speed))
            elif places_to_move_y > 0 and places_to_move_x < 0:
                self.model.grid.move_agent(self, (self.pos[0] - speed, self.pos[1] + speed))
            elif places_to_move_y < 0 and places_to_move_x > 0:
                self.model.grid.move_agent(self, (self.pos[0] + speed, self.pos[1] - speed))
            elif places_to_move_x == 0:
                if places_to_move_y > 0:
                    self.model.grid.move_agent(self, (self.pos[0], self.pos[1] + speed))
                elif places_to_move_y < 0:
                    self.model.grid.move_agent(self, (self.pos[0], self.pos[1] - speed))
            elif places_to_move_y == 0:
                if places_to_move_x > 0:
                    self.model.grid.move_agent(self, (self.pos[0] + speed, self.pos[1]))
                elif places_to_move_x < 0:
                    self.model.grid.move_agent(self, (self.pos[0] - speed, self.pos[1]))

        # if fire not in the neighboorhood, do random move
        else:
            self.random_move()

    # Makes the firetruck move towards the fire
    def closestfire_move(self):
        fire_intheneighborhood = False
        for i in [5, 15, 25, 50, 100]:
            limited_vision = int(self.vision * i / 100.)

            # find hot trees in neighborhood
            neighbors_list = self.model.grid.get_neighbors(
                self.pos, moore=True, radius=limited_vision)

            neighbors_list = [x for x in neighbors_list if x.condition == "On Fire"]

            # find closest fire
            min_distance = limited_vision**2
            for neighbor in neighbors_list:
                distance = abs(neighbor.pos[0]**2 - self.pos[0]**2) + abs(neighbor.pos[1]**2 - self.pos[1]**2)
                if distance < min_distance:
                    min_distance = distance
                    closest_neighbor = neighbor
                    fire_intheneighborhood = True
            if fire_intheneighborhood:
                break

        """
        if fire_intheneighborhood == False:
            # find hot trees in neighborhood
            neighbors_list = self.model.grid.get_neighbors(
                self.pos, moore=True, radius=self.vision)

            neighbors_list = [x for x in neighbors_list if x.condition == "On Fire"]

            # find closest fire
            min_distance = self.vision**2
            fire_intheneighborhood = False
            for neighbor in neighbors_list:
                distance = abs(neighbor.pos[0]**2 - self.pos[0]**2) + abs(neighbor.pos[1]**2 - self.pos[1]**2)
                if distance < min_distance:
                    min_distance = distance
                    closest_neighbor = neighbor
                    fire_intheneighborhood = True
        """

        # move toward fire if it is actually in the neighborhood
        if fire_intheneighborhood:

            # find how many places to move to reach the closest fire
            places_to_move_y = closest_neighbor.pos[1] - self.pos[1]
            places_to_move_x = closest_neighbor.pos[0] - self.pos[0]

            if self.pos[0] == 1 or self.pos[0] == self.model.width - 2 or self.pos[1] == 1 or \
                    self.pos[1] == self.model.height - 2:
                speed = 1
            else:
                speed = self.max_speed

            # choose step
            if places_to_move_x > 0 and places_to_move_y > 0:
                self.model.grid.move_agent(self, (self.pos[0] + speed, self.pos[1] + speed))
            elif places_to_move_x < 0 and places_to_move_y < 0:
                self.model.grid.move_agent(self, (self.pos[0] - speed, self.pos[1] - speed))
            elif places_to_move_y > 0 and places_to_move_x < 0:
                self.model.grid.move_agent(self, (self.pos[0] - speed, self.pos[1] + speed))
            elif places_to_move_y < 0 and places_to_move_x > 0:
                self.model.grid.move_agent(self, (self.pos[0] + speed, self.pos[1] - speed))
            elif places_to_move_x == 0:
                if places_to_move_y > 0:
                    self.model.grid.move_agent(self, (self.pos[0], self.pos[1] + speed))
                elif places_to_move_y < 0:
                    self.model.grid.move_agent(self, (self.pos[0], self.pos[1] - speed))
            elif places_to_move_y == 0:
                if places_to_move_x > 0:
                    self.model.grid.move_agent(self, (self.pos[0] + speed, self.pos[1]))
                elif places_to_move_x < 0:
                    self.model.grid.move_agent(self, (self.pos[0] - speed, self.pos[1]))

        # if fire not in the neighboorhood, do random move
        else:
            self.random_move()


class Firetruck(Walker):
    def __init__(self, model, unique_id, pos, truck_strategy, vision, max_speed):
        super().__init__(unique_id, model, pos)
        self.unique_id = unique_id
        self.condition = "Full"
        self.extinguished = 0
        self.truck_strategy = truck_strategy
        self.vision = vision
        self.max_speed = max_speed
        self.life_bar = -5

    def get_pos(self):
        return self.pos

    def step(self):
        '''
        This method should move the Sheep using the `random_move()`
        method implemented earlier, then conditionally reproduce.
        '''
        if(self.truck_strategy == 'Goes to the closest fire'):
            self.closestfire_move()
        elif(self.truck_strategy == 'Goes to the biggest fire'):
            self.biggestfire_move()
        else:
            self.random_move()
        self.extinguish()

    def extinguish(self):
        neighbors_list = self.model.grid.get_neighbors(
            self.pos, moore=True, radius=1, include_center=True)
        for tree in neighbors_list:
            if tree.condition == "On Fire":
                tree.condition = "Is Extinguished"
                self.extinguished += 1
                self.life_bar -= 5

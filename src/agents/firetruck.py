#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 15:30:03 2020

This code was implemented by
Louis Weyland & Robin van den Berg, Philippe Nicolau, Hildebert Mouilé & Wiebe Jelsma

"""
import random
from mesa import Agent
from environment.river import RiverCell


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

        for cell in cell_list:
            if self.model.grid.get_cell_list_contents(cell):
                if isinstance(self.model.grid.get_cell_list_contents(cell)[0], RiverCell):
                    cell_list.remove(cell)

        new_pos = cell_list[random.randint(0, len(cell_list) - 1)]

        self.model.grid.move_agent(self, new_pos)

    def take_step(self, closest_neighbor):
        # choose step
        places_to_move_y = closest_neighbor.pos[1] - self.pos[1]
        places_to_move_x = closest_neighbor.pos[0] - self.pos[0]

        speedX, speedY = self.truck_max_speed, self.truck_max_speed

        if self.pos[0] == 1 or self.pos[0] == self.model.width - 2 or self.pos[1] == 1 or \
                self.pos[1] == self.model.height - 2:
            speedX = 1
            speedY = 1
        if abs(places_to_move_y) == 1:
            speedY = 1
        if abs(places_to_move_x) == 1:
            speedX = 1

        new_x, new_y = self.pos[0], self.pos[1]

        if places_to_move_x > 0:
            new_x += speedX
        if places_to_move_x < 0:
            new_x -= speedX
        if places_to_move_y > 0:
            new_y += speedY
        if places_to_move_y < 0:
            new_y -= speedY

        if self.model.grid.get_cell_list_contents((new_x, new_y)):
            if not isinstance(self.model.grid.get_cell_list_contents((new_x, new_y))[0], RiverCell):
                self.model.grid.move_agent(self, (new_x, new_y))

        else:
            self.model.grid.move_agent(self, (new_x, new_y))

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
            min_distance = limited_vision ** 2
            min_life_bar = 0
            for neighbor in neighbors_list:
                current_life_bar = neighbor.life_bar
                distance = abs(neighbor.pos[0] ** 2 - self.pos[0] ** 2) + abs(neighbor.pos[1] ** 2 - self.pos[1] ** 2)
                if current_life_bar >= min_life_bar and distance <= min_distance:
                    min_distance = distance
                    min_life_bar = current_life_bar
                    closest_neighbor = neighbor
                    fire_intheneighborhood = True
            if fire_intheneighborhood:
                break

        # move toward fire if it is actually in the neighborhood
        if fire_intheneighborhood:
            self.take_step(closest_neighbor)

        # if fire not in the neighbourhood, do random move
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
            min_distance = limited_vision ** 2
            for neighbor in neighbors_list:
                distance = abs(neighbor.pos[0] ** 2 - self.pos[0] ** 2) + abs(neighbor.pos[1] ** 2 - self.pos[1] ** 2)
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
            self.take_step(closest_neighbor)

        # if fire not in the neighboorhood, do random move
        else:
            self.random_move()

    def parallel_attack(self):
        fire_intheneighborhood = False
        for i in [2, 5, 15, 25, 50, 100]:
            limited_vision = int(self.vision * i / 100.)

            # find hot trees in neighborhood
            neighbors_list = self.model.grid.get_neighbors(
                self.pos, moore=True, radius=limited_vision)

            neighbors_list = [x for x in neighbors_list if x.condition == "On Fire"]

            # find closest fire
            min_distance = 100000
            max_life_bar = 0
            for neighbor in neighbors_list:
                print("New neighbour")
                xposition = abs(neighbor.pos[0] - self.pos[0])
                yposition = abs(neighbor.pos[1] - self.pos[1])
                if xposition == 1 and yposition == 1:
                    distance = 1
                elif xposition == 2 and yposition == 2:
                    distance = 2
                else:
                    distance = xposition + yposition

                # distance = abs(neighbor.pos[0] - self.pos[0]) ** 2 + abs(
                #     neighbor.pos[1] - self.pos[1]) ** 2
                print("Distance:", distance)

                life_bar = neighbor.life_bar
                if distance <= min_distance and life_bar >= max_life_bar:
                    max_life_bar = life_bar
                    min_distance = distance
                    closest_neighbor = neighbor
                    fire_intheneighborhood = True
            if fire_intheneighborhood:
                break

        if i == 2:
            neighbors_list_fire = self.model.grid.get_neighbors(closest_neighbor.pos, moore=False,
                                                                radius=1)
            max_distance = 0
            for neighbor in neighbors_list_fire:
                positionx = abs(neighbor.pos[0] - self.pos[0])
                positiony = abs(neighbor.pos[1] - self.pos[1])
                newdistance = positionx + positiony

                # print(neighbor.pos[0])
                # print(neighbor.pos[1])
                if neighbor.condition != "On Fire" and positionx <= self.truck_max_speed and \
                        positiony <= self.truck_max_speed and newdistance > max_distance:
                    max_distance = newdistance
                    closest_neighbor = neighbor

        if fire_intheneighborhood:
            self.take_step(closest_neighbor)


class Firetruck(Walker):
    def __init__(self, model, unique_id, pos, truck_strategy, vision, truck_max_speed):
        super().__init__(unique_id, model, pos)
        self.unique_id = unique_id
        self.condition = "Full"
        self.extinguished = 0
        self.truck_strategy = truck_strategy
        self.vision = vision
        self.truck_max_speed = truck_max_speed
        self.life_bar = -5

    def get_pos(self):
        return self.pos

    def step(self):
        '''
        This method should move the Sheep using the `random_move()`
        method implemented earlier, then conditionally reproduce.
        '''
        if (self.truck_strategy == 'Goes to the closest fire'):
            self.closestfire_move()
        elif (self.truck_strategy == 'Goes to the biggest fire'):
            self.biggestfire_move()
        elif (self.truck_strategy == "Parallel attack"):
            self.parallel_attack()
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

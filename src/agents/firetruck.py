#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 15:30:03 2020

This code was implemented by
Louis Weyland & Robin van den Berg, Philippe Nicolau, Hildebert Mouilé & Wiebe Jelsma

"""
import random
import numpy as np
import math
from mesa import Agent
from environment.river import RiverCell
from environment.vegetation import TreeCell


class Walker(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)

        self.pos = pos
        self.unique_id = unique_id

    def firefighters_tree_ratio(self, number_of_firefighters, trees_on_fire):
        if trees_on_fire > 0:
            return int(math.ceil(number_of_firefighters / trees_on_fire))
        return 1

    def random_move(self):
        '''
        This method should get the neighbouring cells (Moore's neighbourhood)
        select one, and move the agent to this cell.
        '''

        cell_list = self.model.grid.get_neighborhood(self.pos, moore=True, radius=self.truck_max_speed)

        for cell in cell_list:
            if self.model.grid.get_cell_list_contents(cell):
                if isinstance(self.model.grid.get_cell_list_contents(cell)[0], RiverCell):
                    cell_list.remove(cell)

        new_pos = cell_list[random.randint(0, len(cell_list) - 1)]

        self.model.grid.move_agent(self, new_pos)

    def take_step(self, closest_neighbor):

        places_to_move_y = closest_neighbor.pos[1] - self.pos[1]
        places_to_move_x = closest_neighbor.pos[0] - self.pos[0]

        speed_x = min(self.truck_max_speed, abs(places_to_move_x))
        speed_y = min(self.truck_max_speed, abs(places_to_move_y))

        new_x, new_y = self.pos[0], self.pos[1]

        if places_to_move_x > 0:
            new_x += speed_x
        if places_to_move_x < 0:
            new_x -= speed_x
        if places_to_move_y > 0:
            new_y += speed_y
        if places_to_move_y < 0:
            new_y -= speed_y

        if self.model.grid.get_cell_list_contents((new_x, new_y)):
            if not isinstance(self.model.grid.get_cell_list_contents(
                    (new_x, new_y))[0], RiverCell):
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
        ratio = self.firefighters_tree_ratio(
            self.model.num_firetruck, self.model.count_type(
                self.model, "On Fire"))
        fire_intheneighborhood = False
        limited_vision_list = [i for i in range(2, 100, 2)]
        for i in range(len(limited_vision_list)):

            limited_vision = int(self.vision * limited_vision_list[i] / 100.)
            if i > 0:
                inner_radius = int(
                    self.vision * limited_vision_list[i - 1] / 100.)
            else:
                inner_radius = 0

            # find hot trees in neighborhood
            neighbors_list = self.model.grid.get_neighbors(
                self.pos, moore=True, radius=limited_vision, inner_radius=inner_radius)

            neighbors_list = [
                x for x in neighbors_list if x.condition == "On Fire"]

            # find closest fire
            min_distance = limited_vision ** 2
            min_life_bar = 0
            for neighbor in neighbors_list:
                if neighbor.trees_claimed < ratio:
                    current_life_bar = neighbor.life_bar
                    distance = abs(neighbor.pos[0] ** 2 - self.pos[0] ** 2) + \
                        abs(neighbor.pos[1] ** 2 - self.pos[1] ** 2)
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
            closest_neighbor.trees_claimed += 1

        # if fire not in the neighbourhood, do random move
        else:
            self.random_move()

    # Makes the firetruck move towards the fire
    def closestfire_move(self):
        ratio = self.firefighters_tree_ratio(
            self.model.num_firetruck, self.model.count_type(
                self.model, "On Fire"))
        fire_intheneighborhood = False
        limited_vision_list = [i for i in range(2, 100, 2)]

        for i in range(len(limited_vision_list)):
            limited_vision = int(self.vision * limited_vision_list[i] / 100.)

            if i > 0:
                inner_radius = int(
                    self.vision * limited_vision_list[i - 1] / 100.)
            else:
                inner_radius = 0

            # find hot trees in neighborhood
            neighbors_list = self.model.grid.get_neighbors(
                self.pos, moore=True, radius=limited_vision, inner_radius=inner_radius)

            neighbors_list = [
                x for x in neighbors_list if x.condition == "On Fire"]

            # find closest fire
            min_distance = limited_vision ** 2
            for neighbor in neighbors_list:
                if neighbor.trees_claimed < ratio:
                    distance = abs(neighbor.pos[0] ** 2 - self.pos[0] ** 2) + \
                        abs(neighbor.pos[1] ** 2 - self.pos[1] ** 2)
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
            closest_neighbor.trees_claimed += 1

        # if fire not in the neighboorhood, do random move
        else:
            self.random_move()

    def optimized_closest_fire(self):
        attr = np.array([o.unique_id for o in self.model.firefighters_lists])
        # print(attr)
        # print(self.unique_id)
        # print(np.where(attr == self.unique_id))
        closest_neighbor = self.model.assigned_list[np.where(attr == self.unique_id)[0][0]]

        self.take_step(closest_neighbor)
        closest_neighbor.trees_claimed += 1

    def optimized_parallel_fire(self):
        attr = np.array([o.unique_id for o in self.model.firefighters_lists])
        # print(attr)
        # print(self.unique_id)
        # print(np.where(attr == self.unique_id))
        closest_neighbor = self.model.assigned_list[np.where(attr == self.unique_id)[0][0]]

        neighbors_list_fire = self.model.grid.get_neighbors(closest_neighbor.pos, moore=False,
                                                            radius=1)
        max_distance = 0
        for neighbor in neighbors_list_fire:
            position_x = abs(neighbor.pos[0] - self.pos[0])
            position_y = abs(neighbor.pos[1] - self.pos[1])
            new_distance = position_x + position_y

            if neighbor.condition != "On Fire" and position_x <= self.truck_max_speed and \
                    position_y <= self.truck_max_speed and new_distance > max_distance and \
                    isinstance(neighbor, TreeCell):
                max_distance = new_distance
                closest_neighbor = neighbor

        self.take_step(closest_neighbor)
        closest_neighbor.trees_claimed += 1

    def parallel_attack(self):
        ratio = self.firefighters_tree_ratio(
            self.model.num_firetruck, self.model.count_type(
                self.model, "On Fire"))
        fire_intheneighborhood = False
        limited_vision_list = [i for i in range(2, 100, 2)]
        for i in range(len(limited_vision_list)):
            limited_vision = int(self.vision * limited_vision_list[i] / 100.)

            if i > 0:
                inner_radius = int(
                    self.vision * limited_vision_list[i - 1] / 100.)
            else:
                inner_radius = 0

            # find hot trees in neighborhood
            neighbors_list = self.model.grid.get_neighbors(
                self.pos, moore=True, radius=limited_vision, inner_radius=inner_radius)

            neighbors_list = [
                x for x in neighbors_list if x.condition == "On Fire"]

            # find closest fire
            min_distance = 100000
            max_life_bar = 0
            for neighbor in neighbors_list:
                if neighbor.trees_claimed < ratio:

                    x_position = abs(neighbor.pos[0] - self.pos[0])
                    y_position = abs(neighbor.pos[1] - self.pos[1])
                    if x_position == y_position:
                        distance = x_position
                    else:
                        distance = x_position + y_position

                    # distance = abs(neighbor.pos[0] - self.pos[0]) ** 2 + abs(
                    #     neighbor.pos[1] - self.pos[1]) ** 2

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
                position_x = abs(neighbor.pos[0] - self.pos[0])
                position_y = abs(neighbor.pos[1] - self.pos[1])
                new_distance = position_x + position_y

                if neighbor.condition != "On Fire" and position_x <= self.truck_max_speed and \
                        position_y <= self.truck_max_speed and new_distance > max_distance:
                    max_distance = new_distance
                    closest_neighbor = neighbor

        if fire_intheneighborhood:
            self.take_step(closest_neighbor)
            closest_neighbor.trees_claimed += 1
        else:
            self.random_move()

    def indirect_attack(self):

        fire_is_close = False

        neighbor_list = self.model.grid.get_neighbors(
            self.pos, moore=True, radius=40, include_center=True)

        for neighbor in neighbor_list:
            if neighbor.condition == 'On Fire':
                fire_is_close = True

        if fire_is_close:

            if self.model.grid.is_cell_empty:
                list_of_cell_content = self.model.grid.get_cell_list_contents(
                    self.pos)
                for content in list_of_cell_content:
                    if isinstance(content, TreeCell):
                        content.condition = "Burned Out"

                    else:
                        if self.pos[0] >= max(firetrucks.pos[0] for firetrucks in self.model.firefighters_lists) and \
                                self.pos[1] >= max(firetrucks.pos[1] for firetrucks in self.model.firefighters_lists):

                            self.model.grid.move_agent(
                                self, (self.pos[0], self.pos[1] - 1))

                        elif self.pos[0] <= min(firetrucks.pos[0] for firetrucks in self.model.firefighters_lists) and \
                                self.pos[1] <= min(firetrucks.pos[1] for firetrucks in self.model.firefighters_lists):
                            self.model.grid.move_agent(
                                self, (self.pos[0], self.pos[1] + 1))

                        elif self.pos[0] <= min(firetrucks.pos[0] for firetrucks in self.model.firefighters_lists) and \
                                self.pos[1] >= max(firetrucks.pos[1] for firetrucks in self.model.firefighters_lists):
                            self.model.grid.move_agent(
                                self, (self.pos[0] + 1, self.pos[1]))

                        elif self.pos[0] >= max(firetrucks.pos[0] for firetrucks in self.model.firefighters_lists) and \
                                self.pos[1] <= min(firetrucks.pos[1] for firetrucks in self.model.firefighters_lists):
                            self.model.grid.move_agent(
                                self, (self.pos[0] - 1, self.pos[1]))

                        elif self.pos[0] <= min(firetrucks.pos[0] for firetrucks in self.model.firefighters_lists) and \
                                self.pos[1] < max(firetrucks.pos[1] for firetrucks in self.model.firefighters_lists):
                            self.model.grid.move_agent(
                                self, (self.pos[0], self.pos[1] + 1))

                        elif self.pos[0] < max(firetrucks.pos[0] for firetrucks in self.model.firefighters_lists) and \
                                self.pos[1] >= max(firetrucks.pos[1] for firetrucks in self.model.firefighters_lists):
                            self.model.grid.move_agent(
                                self, (self.pos[0] + 1, self.pos[1]))

                        elif self.pos[0] >= max(firetrucks.pos[0] for firetrucks in self.model.firefighters_lists) and \
                                self.pos[1] < max(firetrucks.pos[1] for firetrucks in self.model.firefighters_lists):
                            self.model.grid.move_agent(
                                self, (self.pos[0], self.pos[1] - 1))

                        elif self.pos[0] < max(firetrucks.pos[0] for firetrucks in self.model.firefighters_lists) and \
                                self.pos[1] <= min(firetrucks.pos[1] for firetrucks in self.model.firefighters_lists):
                            self.model.grid.move_agent(
                                self, (self.pos[0] - 1, self.pos[1]))

                        # in case the agent is not in the square to put it back

        else:
            self.optimized_closest_fire()


class Firetruck(Walker):
    def __init__(self, model, unique_id, pos,
                 truck_strategy, vision, truck_max_speed):
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
        # set step according to strategy
        if (self.truck_strategy == 'Goes to the closest fire'):
            self.closestfire_move()
        elif (self.truck_strategy == 'Goes to the biggest fire'):
            self.biggestfire_move()
        elif (self.truck_strategy == "Parallel attack"):
            self.optimized_parallel_fire()
        elif (self.truck_strategy == "Optimized closest"):
            self.optimized_closest_fire()
        elif (self.truck_strategy == 'Indirect attack'):
            self.indirect_attack()
        else:
            self.random_move()

        if (self.truck_strategy != 'Indirect attack'):
            self.extinguish()

    def extinguish(self):
        neighbors_list = self.model.grid.get_neighbors(
            self.pos, moore=True, radius=1, include_center=True)
        for tree in neighbors_list:
            if tree.condition == "On Fire":
                tree.fire_bar -= 1
                if tree.fire_bar == 0:
                    tree.condition = "Is Extinguished"
                    self.extinguished += 1

"""
Created on Wed Jan  8 15:30:03 2020

This code was implemented by
Louis Weyland & Robin van den Berg, Philippe Nicolau, Hildebert Mouilé & Wiebe Jelsma

"""
import random
from environment.rain import Rain
from agents.firetruck import Firetruck
from environment.vegetation import TreeCell
from environment.river import RiverCell
from agents.firetruck import Walker
from datacollector_v2 import DataCollector
from space_v2 import MultiGrid
from environment.firebreak import BreakCell
from mesa.time import RandomActivation
from mesa import Model
import numpy as np
import math
import sys
sys.path.append('../')


# defines the model


class ForestFire(Model):
    '''
    Simple Forest Fire model.
    '''

    def __init__(
            self,
            height=100,
            width=100,
            density=0.99,
            temperature=0,
            truck_strategy=4,
            river_number=0,
            river_width=0,
            random_fires=0,
            num_firetruck=10,
            vision=100,
            truck_max_speed=2,
            wind_strength=10,
            wind_dir="\u2B06  North",
            break_width=0,
            sparse_ratio=0.5,
            steps_to_extinguishment=1):
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
        self.river_width = river_width

        self.break_length = width
        self.break_width = break_width
        self.break_size = width

        self.temperature = temperature
        self.steps_to_extinguishment = steps_to_extinguishment
        self.n_agents = 0

        self.agents = []
        self.firefighters_lists = []
        self.initial_tree = height * width * density - \
            self.river_length * self.river_width
        self.initial_tree = self.initial_tree - self.break_length * self.break_width

        self.sparse_ratio = sparse_ratio

        # Set up model objects
        self.schedule_TreeCell = RandomActivation(self)
        self.schedule_FireTruck = RandomActivation(self)
        self.schedule = RandomActivation(self)
        self.current_step = 0

        # Set the wind
        self.wind = wind_strength

        # Translate the wind_dir string into vector
        wind_vector = {"\u2B06  North": (0, 1), "\u2197 North/East": (1, 1), "\u27A1 East": (1, 0),
                       "\u2198 South/East": (1, -1), "\u2B07 South": (0, -1), "\u2199 South/West": (-1, -1),
                       "\u2B05 West": (-1, 0), "\u2196 North/West": (-1, 1)}
        self.wind_dir = wind_vector[wind_dir]

        self.grid = MultiGrid(height, width, torus=False)

        # random.seed(1)
        self.init_river()
        self.init_break(self.break_size)

        # agent_reporters={TreeCell: {"Life bar": "life_bar"}})

        # random.seed(1)
        self.init_vegetation(TreeCell, self.initial_tree)

        for i in range(len(self.agents)):
            self.schedule_TreeCell.add(self.agents[i])
            self.schedule.add(self.agents[i])

        # Put int back to string
        if truck_strategy == 1:
            truck_strategy = "Optimized closest"
        elif truck_strategy == 0:
            truck_strategy = 'Random'
        elif truck_strategy == 2:
            truck_strategy = 'Goes to the biggest fire'
        elif truck_strategy == 3:
            truck_strategy = 'Parallel attack'
        elif truck_strategy == 4:
            truck_strategy = 'Indirect attack'

        self.random_fires = random_fires
        self.temperature = temperature
        self.num_firetruck = num_firetruck
        self.truck_strategy = truck_strategy
        self.wind_strength = wind_strength

        # random.seed(1)
        self.init_firefighters(Firetruck, num_firetruck, truck_strategy, vision, truck_max_speed)
        # self.init_rain()

        # Initialise fire in the middle if possible otherwise random
        self.agents[0].condition = "On Fire"

        # get initial fire position and define the square
        self.init_fire_pos = self.agents[0].pos

        # count number of fire took fire
        self.count_total_fire = 0

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

        self.buffer_x_min = int((self.init_fire_pos[0]) - 30)
        self.buffer_x_max = int((self.init_fire_pos[0]) + 30)
        self.buffer_y_min = int((self.init_fire_pos[1]) - 30)
        self.buffer_y_max = int((self.init_fire_pos[1]) + 30)
        self.buffer_coordinates = [self.buffer_x_min, self.buffer_x_max, self.buffer_y_min, self.buffer_y_max]
        self.tree_list_on_buffer = self.list_tree_in_buffer(self, self.buffer_coordinates)

    def init_river(self):
        '''
        Creating a river
        '''
        if self.river_width == 0:
            pass
        else:
            # initiating the river offgrid
            x = -1
            y_init = random.randrange(self.height - 1)

            # increasing the length of the river
            for i in range(int(self.river_length)):
                x += 1
                y = y_init + random.randint(-1, 1)

                while y < 0 or y >= self.height:
                    y += random.randint(-1, 1)
                self.new_river(RiverCell, (x, y))

                y_init = y

                # increasing the width of the river
                for j in range(self.river_width - 1):
                    new_width = random.choice([-1, 1])
                    if y + new_width < 0 or y + new_width == self.height:
                        new_width = -new_width
                    y += new_width
                    while not self.grid.is_cell_empty((x, y)):
                        if y + new_width < 0 or y + new_width == self.height:
                            new_width = -new_width
                        y += new_width
                    self.new_river(RiverCell, (x, y))

    def init_break(self, n):
        '''
        Creating a Firebreak (no fuel to burn on the designated area)
        '''
        if self.break_width == 0:
            pass
        else:
            # initiating the break offgrid
            x = -1
            y_init = random.randrange(self.height - 1)

            # increasing the length of the break
            for i in range(int(n)):
                x += 1
                y = y_init + random.randint(-1, 1)

                while y < 0 or y >= self.height:
                    y += random.randint(-1, 1)
                self.new_break(BreakCell, (x, y))

                y_init = y

                # increasing the width of the break
                for j in range(self.break_width - 1):
                    new_w = random.choice([-1, 1])
                    if y + new_w < 0 or y + new_w == self.height:
                        new_w = -new_w
                    y += new_w
                    while not self.grid.is_cell_empty((x, y)):
                        if y + new_w < 0 or y + new_w == self.height:
                            new_w = -new_w
                        y += new_w
                    self.new_break(BreakCell, (x, y))

    def init_vegetation(self, agent_type, n):
        '''
        Creating trees
        '''
        x = random.randrange(self.width)
        y = random.randrange(self.height)

        if self.river_width == 0 and self.break_width == 0:
            self.new_agent(agent_type, (int(self.width / 2), int(self.height / 2)))
        else:
            self.new_agent(agent_type, (x, y))

        for i in range(int(n - 1)):
            while not self.grid.is_cell_empty((x, y)):
                x = random.randrange(self.width)
                y = random.randrange(self.height)
            self.new_agent(agent_type, (x, y))

        '''
        5x FASTER METHOD BUT CREATES SAME "RANDOM" SPREAD EVERY INITIALIZATION

        if self.river_width == 0 and self.break_width == 0:
            self.new_agent(agent_type, (int(self.width / 2), int(self.height / 2)))
        else:
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            while not self.grid.is_cell_empty((x, y)):
                x = random.randrange(self.width)
                y = random.randrange(self.height)
            self.new_agent(agent_type, (x, y))

        while len(self.grid.empties) > self.width * self.height - self.initial_tree:
            self.new_agent(agent_type, self.grid.empties.pop())
        '''

    def init_firefighters(self, agent_type, num_firetruck,
                          truck_strategy, vision, truck_max_speed):
        if num_firetruck == 0:
            pass
        else:
            init_positions = self.equal_spread()

            for i in range(num_firetruck):
                my_pos = init_positions.pop()
                firetruck = self.new_firetruck(
                    Firetruck, my_pos, truck_strategy, vision, truck_max_speed)
                self.schedule_FireTruck.add(firetruck)
                self.schedule.add(firetruck)
                self.firefighters_lists.append(firetruck)

        '''
        METHOD TO PLACE FIREFIGHTERS RANDOMLY OVER GRID

        for i in range(num_firetruck):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            while self.grid.get_cell_list_contents((x, y)):
                if isinstance(self.grid.get_cell_list_contents(
                        (x, y))[0], RiverCell):
                    x = random.randrange(self.width)
                    y = random.randrange(self.height)
                else:
                    break

            firetruck = self.new_firetruck(
                Firetruck, (x, y), truck_strategy, vision, truck_max_speed)
            self.schedule_FireTruck.add(firetruck)
            self.schedule.add(firetruck)
        '''

    def init_rain(self):
        '''
        Creating rain
        '''
        x = random.randrange(self.width)
        y = random.randrange(self.height)
        self.new_agent(Rain, (x, y))
        neighbors = self.grid.get_neighbors((x, y), moore=True)
        for neighbor in neighbors:
            self.new_agent(Rain, neighbor.pos)

    def step(self):
        '''
        Advance the model by one step.
        '''
        self.trees_on_fire = 0
        self.schedule_TreeCell.step()

        self.tree_list = self.list_tree_by_type(self, "On Fire")
        if len(self.tree_list) > 0:

            if (self.truck_strategy == "Optimized closest"):
                self.assigned_list = self.assign_closest(
                    self.compute_distances(self.tree_list,
                                           self.firefighters_lists), self.tree_list)

            elif (self.truck_strategy == "Optimized Parallel attack"):
                self.assigned_list = self.assign_parallel(
                    self.compute_distances(self.tree_list, self.firefighters_lists),
                    self.tree_list)

            elif (self.truck_strategy == "Indirect attack"):
                self.assigned_list = self.assign_parallel(
                    self.compute_distances(self.tree_list, self.firefighters_lists),
                    self.tree_list)

            self.schedule_FireTruck.step()

        self.dc.collect(self, [TreeCell, Firetruck])
        self.current_step += 1

        if self.random_fires:
            randtree = int(random.random() * len(self.agents))
            if self.agents[randtree].condition == "Fine":
                self.randomfire(self, randtree)

        # Halt if no more fire
        if self.count_type(self, "On Fire") == 0:
            self.running = False

    @staticmethod
    def randomfire(self, randtree):
        if (random.random() < (math.exp(self.temperature / 15) / 300.0)):
            self.agents[randtree].condition = "On Fire"

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

    def compute_distances(self, tree_list, truck_list):
        distances = [[0 for x in range(len(truck_list))] for y in range(len(tree_list))]
        for i in range(len(tree_list)):
            for j in range(len(truck_list)):
                distances[i][j] = (tree_list[i].pos[0] - truck_list[j].pos[0]) ** 2 + \
                    (tree_list[i].pos[1] - truck_list[j].pos[1]) ** 2
        return distances

    def assign_closest(self, matrix, tree_list):
        assigned_trucks = [0 for x in range(self.num_firetruck)]
        ratio = Walker.firefighters_tree_ratio(self, self.num_firetruck, len(tree_list))
        matrix = np.asarray(matrix, dtype=int)
        while 0 in assigned_trucks:
            curr_smallest_pos = np.unravel_index(np.argmin(matrix, axis=None), matrix.shape)
            if assigned_trucks[curr_smallest_pos[1]] == 0 and tree_list[curr_smallest_pos[0]].trees_claimed < ratio:
                assigned_trucks[curr_smallest_pos[1]] = tree_list[curr_smallest_pos[0]]
                tree_list[curr_smallest_pos[0]].trees_claimed += 1
            matrix[curr_smallest_pos] = 100000
        return assigned_trucks

    def assign_parallel(self, matrix, tree_list):
        assigned_trucks = [0 for x in range(self.num_firetruck)]
        ratio = Walker.firefighters_tree_ratio(self, self.num_firetruck, len(tree_list))
        matrix = np.asarray(matrix, dtype=int)
        for i in range(len(matrix[0])):
            curr_best = [matrix[0][i], tree_list[0].life_bar, 0]
            indices = [j for j, x in enumerate(matrix[:, i]) if x <= curr_best[0]]
            for m in indices:
                if tree_list[m].trees_claimed >= ratio:
                    indices.remove(m)
            if len(indices) > 1:
                for k in indices:
                    if matrix[k][i] <= curr_best[0] and tree_list[k].life_bar >= curr_best[1]:
                        curr_best = [matrix[k][i], tree_list[k].life_bar, k]
                tree_list[curr_best[2]].trees_claimed += 1
            assigned_trucks[i] = tree_list[curr_best[2]]
        return assigned_trucks

    @staticmethod
    def list_tree_by_type(model, tree_condition):
        '''
        Helper method to count trees in a given condition in a given model.
        '''
        tree_list = [tree for tree in model.schedule_TreeCell.agents if tree.condition == tree_condition]

        return tree_list

    @staticmethod
    def list_tree_in_buffer(model, coordinates):
        '''
        Helper method to count trees lying on the buffer
        coordinates = [self.buffer_x_min,self.buffer_x_max,self.buffer_y_min,self.buffer_y_max]
        '''

        tree_list_b = [tree for tree in model.schedule_TreeCell.agents
                       if((tree.pos[1] == coordinates[2])
                          and (coordinates[0] <= tree.pos[0])
                           and (tree.pos[0] <= coordinates[1]))]
        tree_list_u = [tree for tree in model.schedule_TreeCell.agents
                       if((tree.pos[1] == coordinates[3])
                          and (coordinates[0] <= tree.pos[0])
                           and (tree.pos[0] <= coordinates[1]))]
        tree_list_l = [tree for tree in model.schedule_TreeCell.agents
                       if ((tree.pos[0] == coordinates[0])
                           and (coordinates[2] < tree.pos[1])
                           and (tree.pos[1] < coordinates[3]))]
        tree_list_r = [tree for tree in model.schedule_TreeCell.agents
                       if ((tree.pos[0] == coordinates[1])
                           and (coordinates[2] < tree.pos[1])
                           and (tree.pos[1] < coordinates[3]))]

        tree_list = tree_list_r + tree_list_l + tree_list_b + tree_list_u

        return tree_list

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

    def new_firetruck(self, agent_type, pos, truck_strategy,
                      vision, truck_max_speed):
        '''
        Method that enables us to add agents of a given type.
        '''
        self.n_agents += 1

        # Create a new agent of the given type
        new_agent = agent_type(
            self,
            self.n_agents,
            pos,
            truck_strategy,
            vision,
            truck_max_speed)

        # Place the agent on the grid
        self.grid.place_agent(new_agent, (int(pos[0]), int(pos[1])))

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

    def new_break(self, agent_type, pos):

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

    def equal_spread(self):

        edge_len = self.height - 1
        total_edge = 4 * edge_len

        x = 0
        y = 0

        start_pos = [(x, y)]
        spacing = total_edge / self.num_firetruck
        total_edge -= spacing
        step = 0

        while total_edge > 0:

            fill_x = edge_len - x
            fill_y = edge_len - y

            if spacing > edge_len:
                if x == 0:
                    x += edge_len
                    y += spacing - edge_len

                else:
                    x, y = y, x

            else:

                # Increasing x
                if y == 0 and x + spacing <= edge_len and step < 2:
                    x += spacing
                    step = 1

                # x maxxed, increasing y
                elif x + spacing > edge_len and y + (spacing - fill_x) < edge_len and step < 3:
                    x += fill_x
                    y += spacing - fill_x
                    step = 2

                # x&y maxxed, decreasing x
                elif x - (spacing - fill_y) >= 0 and y + fill_y >= edge_len and step < 4:
                    x -= (spacing - fill_y)
                    y += fill_y
                    step = 3

                # x emptied, decreasing y
                elif x - spacing < 0 and step < 5:
                    y -= (spacing - x)
                    x = 0
                    step = 4

            start_pos += [(round(x), round(y))]
            total_edge -= spacing

        return start_pos


'''
# To be used if you want to run the model without the visualiser:
temperature = 20
truck_strategy = 'Goes to the closest fire'
density = 0.6
width = 100
height = 100
num_firetruck = 30
vision = 100
break_number = 0
river_number = 0
river_width = 0
random_fires = 1
wind_strength = 8
wind_dir = "N"
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
    break_number,
    random_fires,
    num_firetruck,
    vision,
    max_speed,
    wind_strength,
    wind_dir
)
fire.run_model()

results = fire.dc.get_model_vars_dataframe()
agent_variable = fire.dc.get_agent_vars_dataframe()
results_firetrucks = fire.dc.get_model_vars_dataframe()

print(agent_variable[0])
print(agent_variable[1])
'''

#!/usr/bin/env python3

from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from Forestfiremodel_foundongithub import ForestFire
from agent import *


def forest_fire_portrayal(agent):
    portrayal = {"w": 1,
                 "h": 1,
                 "Filled": "true",
                 "scale": 2.5,
                 "heading_x": 1,
                 "heading_y": 0,
                 "Shape": "rect",
                 "Layer": 0}
    (x, y) = agent.get_pos()
    portrayal["x"] = x
    portrayal["y"] = y

    # define colour of the components
    colors = {"Fine": "#00AA00",
              "On Fire": "#880000",
              "Burned Out": "#000000",
              "Is Extinguished": "#0000ff",
              "Full": "#ffa500"}
    if isinstance(agent, Firetruck):
        portrayal["Layer"] = "1"
        portrayal["Shape"] = "arrowHead"
    portrayal["Color"] = colors[agent.condition]

    # give a color to the fire depending on the life_bar
    if agent.condition == "On Fire" and agent.life_bar > 0:
        portrayal["Color"] = "rgba(%d,14,14)" % (agent.life_bar + 166)

    return portrayal


canvas_element = CanvasGrid(forest_fire_portrayal, 100, 100, 500, 500)
# create line graph
tree_chart = ChartModule([{"Label": "Fine", "Color": "green"},
                          {"Label": "On Fire", "Color": "red"},
                          {"Label": "Burned Out", "Color": "black"}],
                         data_collector_name='dc')
extinguished_chart = ChartModule([{"Label": "Extinguished", "Color": "blue"}],
                                 data_collector_name='dc')

model_parameters = {
    'height': 100,
    'width': 100,
    'wind': (3, 4),
    'vision': 100,
    'max_speed': 2,
    'density': UserSettableParameter('slider', 'Tree density', 0.65, 0.01, 1.0, 0.01),
    'temperature': UserSettableParameter('slider', 'Temperature (°C)', 20, 0, 60, 1),
    'num_firetruck': UserSettableParameter('slider', 'Number of Firetrucks', 30, 0, 300, 1),
    'truck_strategy': UserSettableParameter('choice', 'Firetrucks strategy', value='Goes to the biggest fire',
                                            choices=['Goes to the closest fire', 'Goes to the biggest fire',
                                                     'Random movements']),
    'river_number': UserSettableParameter('slider', 'Number of rivers', 2, 0, 10, 1),  # Unused for now
    'river_width': UserSettableParameter('slider', 'River width', 3, 1, 5, 1),  # Unused for now
}

server = ModularServer(ForestFire, [canvas_element, tree_chart, extinguished_chart], "Forest Fire", model_parameters)

server.port = 8521
server.launch()

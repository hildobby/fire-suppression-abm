#!/usr/bin/env python3

from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from main_model import ForestFire

from environment.river import RiverCell
from environment.vegetation import TreeCell
from agents.firetruck import Firetruck
from environment.rain import Rain
from environment.firebreak import BreakCell


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
    colors = {-0.4: "#77bd98",   # Sparse
              0: "#00bf00",    # Normal
              0.3: "#008000",  # Dense

              "On Fire": "#880000",
              "Burned Out": "#000000",
              "Is Extinguished": "#c994c7",
              "Full": "#ffa500",
              "Plenty": "#0000ff",

              "Rain": "#636363",
              "Firebreak": "#bdbdbd"}

    # if isinstance(agent, Rain):
    #     portrayal = {"w": 3,
    #                  "h": 3,
    #                  "Filled": "False",
    #                  "Shape": "circle",
    #                  "r": 2.5,
    #                  "Scale": 2.5,
    #                  "Layer": 1}
    # portrayal = {"Filled": "false", "h": 3, "w": 3, "Layer": 2}
    if isinstance(agent, Firetruck):
        portrayal["Layer"] = "1"
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"

    if isinstance(agent, TreeCell) and agent.condition == "Fine":
        portrayal["Color"] = colors[agent.veg_density]

    else:
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
    'vision': 100,
    'text_environment': UserSettableParameter('static_text', value='Environment Generation Settings'),
    'density': UserSettableParameter('slider', 'Tree density', 0.99, 0.01, 1.0, 0.01),
    'sparse_ratio': UserSettableParameter('slider', 'Ratio of sparse vegetations', 0.5, 0, 1.0, 0.1),
    'river_width': UserSettableParameter('slider', 'River width', 0, 0, 10, 1),
    'break_width': UserSettableParameter('slider', 'Firebreak width', 0, 0, 6, 1),
    'text_agents': UserSettableParameter('static_text', value='Agents Settings'),
    'num_firetruck': UserSettableParameter('slider', 'Number of Firetrucks', 15, 0, 50, 1),
    'truck_max_speed': UserSettableParameter('slider', 'Speed of Firetrucks', 2, 1, 30, 1),
    'truck_strategy': UserSettableParameter('choice', 'Firetrucks strategy', value='Parallel attack',
                                            choices=['Goes to the closest fire', 'Goes to the biggest fire',
                                                     'Random movements', 'Parallel attack']),
    'text_other_settings': UserSettableParameter('static_text', value='Other Settings'),
    'wind_strength': UserSettableParameter('slider', 'Wind strength', 10, 0, 80, 1),
    'wind_dir': UserSettableParameter('choice', 'Wind Direction', value=('\u2B07 South'),
                                      choices=["\u2B06  North", "\u2197 North/East", "\u27A1 East",
                                               "\u2198 South/East", "\u2B07 North", "\u2199 South/West",
                                               "\u2B05 West", "\u2196 North/West"]),
    'random_fires': UserSettableParameter('checkbox', 'Spontaneous Fires (Temperature based)', value=False),
    'temperature': UserSettableParameter('slider', 'Temperature (°C)', 20, 0, 60, 1)
}

server = ModularServer(ForestFire, [canvas_element, tree_chart, extinguished_chart], "Forest Fire", model_parameters)

server.port = 8521
server.launch()

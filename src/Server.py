#!/usr/bin/env python3

from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from main_model import ForestFire

from environment.river import RiverCell
from environment.vegetation import TreeCell
from agents.firetruck import Firetruck
from environment.rain import Rain


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
              "Is Extinguished": "#c994c7",
              "Full": "#ffa500",
              "Plenty": "#0000ff",
              "Rain": "#636363"}
    if isinstance(agent, Firetruck):
        portrayal["Layer"] = "1"
        portrayal["Shape"] = "arrowHead"
    portrayal["Color"] = colors[agent.condition]
    if isinstance(agent, Rain):
        portrayal["Layer"] = "1"
        portrayal["w"] = "3"
        portrayal["h"] = "3"

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
    # 'wind': (3, 4),
    'vision': 100,
    'max_speed': 2,
    'text_environment': UserSettableParameter('static_text', value='Environment Generation Settings'),
    'density': UserSettableParameter('slider', 'Tree density', 0.99, 0.01, 1.0, 0.01),
    'river_number': UserSettableParameter('slider', 'Number of rivers', 0, 0, 10, 1),  # Unused for now
    'river_width': UserSettableParameter('slider', 'River width', 1, 0, 10, 1),
    'text_agents': UserSettableParameter('static_text', value='Agents Settings'),
    'num_firetruck': UserSettableParameter('slider', 'Number of Firetrucks', 30, 0, 300, 1),
    'truck_speed': UserSettableParameter('slider', 'Speed of Firetrucks', 5, 1, 30, 1),  # Unused for now
    'truck_strategy': UserSettableParameter('choice', 'Firetrucks strategy', value='Parallel attack',
                                            choices=['Goes to the closest fire', 'Goes to the biggest fire',
                                                     'Random movements', 'Parallel attack']),
    'text_other_settings': UserSettableParameter('static_text', value='Other Settings'),
    'text_settings': UserSettableParameter('static_text', value='Wind Settings'),
    'wind_strength': UserSettableParameter('slider', 'Wind strength', 10, 0, 80, 1),
    'wind_dir': UserSettableParameter('choice', 'Wind Direction', value=('\u2B06 North'),
                                      choices=["\u2B07 South", "\u2198 South/West", "\u27A1 West",
                                               "\u2197 North/West", "\u2B06 North", "\u2196 North/East",
                                               "\u2B05 East", "\u2199 South/East"]),
    'random_fires': UserSettableParameter('checkbox', 'Spontaneous Fires (Temperature based)', value=True),
    'temperature': UserSettableParameter('slider', 'Temperature (°C)', 20, 0, 60, 1),
}

server = ModularServer(ForestFire, [canvas_element, tree_chart, extinguished_chart], "Forest Fire", model_parameters)

server.port = 8521
server.launch()

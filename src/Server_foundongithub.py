from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from Forestfiremodel_foundongithub import ForestFire
from agent import *


def forest_fire_portrayal(Agent):
    portrayal = {"w": 1, "h": 1, "Filled": "true", "scale": 2.5,
                 "heading_x": 1, "heading_y": 0, "Shape": "rect", "Layer": 0}
    (x, y) = agent.get_pos()
    portrayal["x"] = x
    portrayal["y"] = y

    colors = {"Fine": "#00AA00",
              "On Fire": "#880000",
              "Burned Out": "#000000",
              "Full": "#ffa500"}
    if isinstance(agent, Firetruck):
        portrayal["Layer"] = "1"
        portrayal["Shape"] = "arrowHead"
    portrayal["Color"] = colors[agent.condition]

    assert(agent.burning_rate == 20), "Burning rate needs to be 20  for the moment ! It is hardcoded"
    cmap = {100: "#f50202",
            80: "#8c0f0f",
            60: "#570a0a",
            40: "#3d0808",
            20: "#290d0d"}

    if agent.condition == "On Fire" and agent.life_bar > 0:
        portrayal["Color"] = cmap[agent.life_bar]

    return portrayal

# def firetruck_portrayal(firetruck):
#     if firetruck is None:
#         return
#     portrayal = {"Shape": "circle", "w": 1, "h": 1, "Filled": "true", "Layer": 1}
#     (x, y) = firetruck.get_pos()
#     portrayal["x"] = x
#     portrayal["y"] = y
#     colors = {"Full": "#00BB00",
#               "Empty": "#880000"}
#     portrayal["Color"] = colors[firetruck.haswater]
#     return portrayal


canvas_element = CanvasGrid(forest_fire_portrayal, 100, 100, 500, 500)
# create line graph
tree_chart = ChartModule([{"Label": "Fine", "Color": "green"},
                          {"Label": "On Fire", "Color": "red"},
                          {"Label": "Burned Out", "Color": "black"}],
                         data_collector_name='dc')
extinguished_chart = ChartModule([{"Label": "Extinguished", "Color": "blue"}],
                                 data_collector_name='dc')

model_sliders = {'density': UserSettableParameter('slider', 'Tree density', 0.65, 0.01, 1.0, 0.01),
                 'temperature_slider': UserSettableParameter('slider', 'Temperature (°C)', 20, 0, 100, 1)
                 }

model_parameters = {'height': 100,
                    'width': 100,
                    'density': UserSettableParameter('slider', 'Tree density', 0.65, 0.01, 1.0, 0.01),
                    'temperature': UserSettableParameter('slider', 'Temperature', 0.65, 0.01, 1.0, 0.01),
                    'num_firetruck': 30,
                    'vision': 100,
                    'max_speed': 2,
                    }

server = ModularServer(ForestFire, [canvas_element, tree_chart, extinguished_chart], "Forest Fire", model_parameters)

server.port = 8521
server.launch()

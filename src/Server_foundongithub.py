from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer

from Forestfiremodel_foundongithub import ForestFire
from agent import *


def forest_fire_portrayal(agent):
    if agent is None:
        return
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
    (x, y) = agent.get_pos()
    portrayal["x"] = x
    portrayal["y"] = y
    colors = {"Fine": "#00AA00",
              "On Fire": "#880000",
              "Burned Out": "#000000",
              "Full": "#ffa500"}
    portrayal["Color"] = colors[agent.condition]
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


server = ModularServer(ForestFire, [canvas_element, tree_chart, extinguished_chart],
                       "Forest Fire", {'height': 100, 'width': 100, 'density': 0.65,
                                       'num_firetruck': 30, 'vision': 100})
print("is it going wrong here?")

server.port = 8521
server.launch()

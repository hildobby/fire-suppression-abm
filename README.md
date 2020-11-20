Agent-based Modeling: Wildfire prevention simulation using agent-based modeling written in Python 3+
=========================================
[![Build Status](https://travis-ci.org/hildobby/Asian-paced_Yodeling.svg?branch=master)](https://travis-ci.org/hildobby/Asian-paced_Yodeling)

This project uses [Mesa](https://github.com/projectmesa/mesa), an Apache2 licensed agent-based modeling (or ABM) 
framework in Python.

This repository allows users to simulate a wildfire in a randomly generated forest environment. The random generation 
is based on user settable settings from the visualisation tool provided by mesa. This simulation is created in a 2D grid of size 100x100. The firefighting agents will attempt to extinguish said fire using a strategy chosen by the user, the firefighter's success depends on the settings used in the simulation. The program also allows for sensitivity analysis with a built-in script.

![A screenshot of the simulation's visualisation](https://github.com/hildobby/fire-suppression-abm/blob/master/src/visualisation.png)

*Above: A screenshot of the visualisation tool provided by Mesa.*

Features
------------

* User settable settings for environment generation such as wind direction, wind strength, rivers, rain, # of firefighting agents and other parameters.
* Multiple firefighting strategies ('Go to the closest fire', 'Go to the biggest fire', 'Random movements', 
'Parallel attack' and 'Indirect attack')
* Sensitivity analysis (One-factor-a-time OFAT) of the environmental settings

Running the server
------------

**Cloning the repository**

To clone the repository using `git`, run the following command in your command line tool:
```bash
git clone https://github.com/hildobby/fire-suppression-abm.git
```

**In order to download all the required packages**

To download all the packages using `pip`, navigate to the repository's local directory and run the following:
```bash
pip install -r "requirements.txt"
```
**In order to run the server with visualisation**

To run the simulation with the GUI in python, run the following fromt your cloned repository's local directory:
```bash
python src/server.py
```

Running the Sensitivity Analysis
------------
To run the Sensitivity analysis run the following command
```bash
python src/sensitivity_analysis/ofat_sa.py
```
where the built-in BatchRunner of mesa is used. More precisely, the child class BatchRunnerMP is used
which allows for parallel computing.
One needs to determine manually which parameters to feed to the 
mesa build in BatchRunner such as the wind strength, the bounds and the number of cores to use.




What remains to be worked on
------------

* Add tests and use codecov
* Adding new types of agents
* Implementing new fire fighting methods
* Make agents able to change their method depending on the circumstances


Litterature used for the project's formulas and settings
------------
* Alexandridis, A., Vakalis, D., Siettos, C. I., & Bafas, G. V. (2008). A  cellular  automata  model for forest fire spread prediction: The case of the wildfire that swept through spetses island in 1990. Applied Mathematics and Computation, 204 (1), 191–201
* Brooks, M. L., D’antonio, C.  M., Richardson, D.  M., Grace, J. B., Keeley, J. E., DiTomaso, J. M.,... Pyke, D. (2004). Effects  of  invasive alien plants on fire regimes. BioScience, 54 (7), 677–688
* Cheney, N. P., Gould, J. S., McCaw, W. L., & Anderson, W. R. (2012). Predicting  fire behaviour in dry eucalypt forest in southern australia. Forest Ecology and Management, 280, 120-131. Retrieved from http://www.sciencedirect.com/science/article/pii/S0378112712003325 doi:https://doi.org/10.1016/j.foreco.2012.06.012
* DeBano, L. F., Neary, D. G., & Ffolliott, P. F. (1998). Fire effects on ecosystems. John Wiley & Sons. Grimm, V., Berger, U., DeAngelis, D. L., Polhill, J. G., Giske, J., & Railsback,S. F. (2010).The odd protocol:A review and first update. Ecological Modelling, 221 (23), 2760-2768. Retrieved  from http://www.sciencedirect.com/science/article/pii/S030438001000414X doi: https://doi.org/10.1016/j.ecolmodel.2010.08.019
* Hansen, R. (2012, 05). Estimating the amount of water required to extinguish wildfires under different conditions and in various fuel types. International Journal of Wildland Fire, 21, 525-536. doi: 10.1071/WF11022 CO
* Hu, X., & Sun, Y. (2007). Agent-based modeling and simulation of wildland fire suppression. In 2007 winter simulation conference (pp. 1275-1283).
* Lee,  Y.-H.,  Fried,  J., Albers,  H., & Haight, R. (2012, 11). Deploying initial attack resources for wildfire suppression: Spatial coordination, budget constraints, and capacity constraints. Canadian  Journal of  Forest Research, 43, 56-65. doi:  10.1139/cjfr-2011-0433
* McKinney,  W.   (2012). Python  for  data  analysis: Data wrangling with pandas, numpy, and ipython.” O’Reilly Media, Inc.”.
* Millman, K. J., & Aivazis, M. (2011). Python for scientists and engineers. Computing in Science & Engineering, 13 (2), 9–12.
* Nolan, R. H., Boer, M.  M., Collins,  L., Resco  de Dios, V., Clarke, H., Jenkins, M.,... Bradstock, R. A. (2020). Causes and consequences of eastern australia’s 2019-20  season of mega-fires. Global change biology.
* Russoa, L., Vakalisb, D., & Siettos, C. (2013). Simulating the wildfire in rhodes in 2008 with a cellular automata model. CHEMICAL  ENGINEERING, 35.
* Shinneman, D. J.,  Germino, M. J., Pilliod, D. S., Aldridge, C. L., Vaillant, N. M., & Coates, P. S (2019). The  ecological uncertainty  of wildfire fuel breaks: examples from the sagebrush steppe. Frontiers in Ecology and the Environment, 17 (5), 279–288.
* Williams,  F. (1977). Mechanisms of fire spread. In Symposium (international) on combustion (Vol. 16, pp. 1281–1294)

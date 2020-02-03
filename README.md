Asian-paced Yodeling: Wildfire prevention simulation using agent-based modeling written in Python 3+
=========================================
[![Build Status](https://travis-ci.org/hildobby/Asian-paced_Yodeling.svg?branch=master)](https://travis-ci.org/hildobby/Asian-paced_Yodeling)

This project uses [Mesa](https://github.com/projectmesa/mesa), an Apache2 licensed agent-based modeling (or ABM) framework in Python.

This repository allows users to simulate a wildfire in a randomly generated forest environment. The random generation is based on user settable settings from the visualisation tool provided by mesa. This simulation is created in a 2D grid of size 100x100. The firefighting agents will attempt to extinguish said fire using a strategy chosen by the user, the firefighter's success depends on the settings used in the simulation. The program also allows for sensitivity analysis with a built-in script.

![A screenshot of the simulation's visualisation](https://github.com/hildobby/Asian-paced_Yodeling/blob/master/src/visualisation.png)

*Above: A screenshot of the visualisation tool provided by Mesa.*

Features
------------

* User settable settings for environment generation, firefighting agents and other parameters such as wind
* Mutliple firefighting strategies
* Sensitivity analysis built into the code

Running the server
------------

**Cloning the repository**

To clone the repository using `git`, run the following command in your command line tool:
```bash
git clone https://github.com/hildobby/Asian-paced_Yodeling.git
```

**In order to download all the required packages**

To download all the packages using `pip`, navigate to the repository's local directory and run the following:
```bash
pip install -r "requirements.txt"
```
**In order to run the server with visualisation**

To run the simulation with the gui in python, run the following fromt your cloned repository's local directory:
```bash
python src/server.py
```

Running the Sensitivity Analysis
------------


What remains to be worked on
------------

* Adding new types of agents
* Implementing new fire fighting methods
* Make agents able to change their method depending on the circumstances


Litterature used for the project's formulas and settings
------------

Asian-paced Yodeling: Wildfire prevention simulation using agent-based modeling written in Python 3+
=========================================

.. image:: https://api.travis-ci.org/hildobby/asian-paced_yodeling.svg?branch=master
        :target: https://travis-ci.org/hildobby/asian-paced_yodeling

This project uses Mesa
  `Mesa`_ is an Apache2 licensed agent-based modeling (or ABM) framework in Python.

It allows users to quickly create agent-based models using built-in core components (such as spatial grids and agent schedulers) or customized implementations; visualize them using a browser-based interface; and analyze their results using Python's data analysis tools. Its goal is to be the Python 3-based alternative to NetLogo, Repast, or MASON.


.. image:: https://github.com/hildobby/Asian-paced_Yodeling/blob/master/src/visualisation.png
   :width: 100%
   :scale: 100%
   :alt: A screenshot of the Schelling Model in Mesa

*Above: A screenshot of the visualisation tool using Mesa.*

.. _`Mesa` : https://github.com/projectmesa/mesa/


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

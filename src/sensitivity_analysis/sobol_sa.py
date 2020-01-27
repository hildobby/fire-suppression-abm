#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 15:30:03 2020

This code was implemented by
Louis Weyland & Robin van den Berg, Philippe Nicolau, Hildebert Mouilé & Wiebe Jelsma

"""

from IPython.display import clear_output
from itertools import combinations
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from SALib.analyze import sobol
from mesa.batchrunner import BatchRunnerMP
from forestfiremodel_SA import ForestFire
from SALib.sample import saltelli
import sys
sys.path.append('../')


# Set the repetitions, the amount of steps, and the amount of distinct values per variable
replicates = 10
distinct_samples = 10

##########################################################################
##########################################################################
##########################################################################
# OFAT with truck_strategy #1


problem = {
    'num_vars': 2,
    'names': ['wind_strength', 'num_firetruck'],
    'bounds': [[0, 30], [0, 60]]
}


model_reporters = {"On Fire": lambda m: m.count_total_fire,
                   "Extinguished": lambda m: m.count_extinguished_fires(m),
                   "Step": lambda m: m.current_step}


data = {}


# We get all our samples here
param_values = saltelli.sample(problem, distinct_samples)

# READ NOTE BELOW CODE
batch = BatchRunnerMP(ForestFire,
                      variable_parameters={name: [] for name in problem['names']},
                      model_reporters=model_reporters, nr_processes=2)


count = 0
for i in range(replicates):
    for vals in param_values:
        # Change parameters that should be integers
        vals = list(vals)
        vals[1] = int(vals[1])

        # Transform to dict with parameter names and their values
        variable_parameters = {}
        for name, val in zip(problem['names'], vals):
            variable_parameters[name] = val

        batch.run_iteration(variable_parameters, tuple(vals), count)
        count += 1

        clear_output()
        print(f'{count / (len(param_values) * (replicates)) * 100:.2f}% done')

data = batch.get_model_vars_dataframe()

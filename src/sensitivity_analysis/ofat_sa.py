#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 15:30:03 2020

This code was implemented by
Louis Weyland & Robin van den Berg, Philippe Nicolau, Hildebert Mouilé & Wiebe Jelsma

"""

import os
from mesa.batchrunner import BatchRunnerMP
import numpy as np
from forestfiremodel_SA import ForestFire
import sys
sys.path.append('../')


try:
    import pathos
except BaseException:
    print("Nanana that's what i though ! You need to install pathos")
    raise

# set the number of cores
n_cores = 3

# Set the repetitions, the amount of steps, and the amount of distinct
# values per variable
replicates = 5
distinct_samples = 5


##########################################################################
##########################################################################
##########################################################################
# OFAT with truck_strategy #1

truck_strategy = 1
problem = {
    'num_vars': 3,
    'names': ['wind_strength', 'num_firetruck', 'truck_strategy'],
    'bounds': [[0, 30], [0, 60], [truck_strategy]]
}

# Set the outputs

model_reporters = {"On Fire": lambda m: m.count_total_fire,
                   "Extinguished": lambda m: m.count_extinguished_fires(m),
                   "Step": lambda m: m.current_step}


data = {}

for i, var in enumerate(problem['names']):
    # Get the bounds for this variable and get <distinct_samples> samples
    # within this space (uniform)
    if var != 'truck_strategy':
        samples = np.linspace(*problem['bounds'][i], num=distinct_samples)

    # firetrucks need to be integers.
    if var == 'num_firetruck':
        samples = np.linspace(
            *problem['bounds'][i],
            num=distinct_samples,
            dtype=int)

    if var == 'truck_strategy':
        samples = np.linspace(1, 1, 1)

    batch = BatchRunnerMP(
        ForestFire,
        iterations=replicates,
        variable_parameters={var: samples},
        model_reporters=model_reporters,
        display_progress=True, nr_processes=n_cores)

    batch.run_all()

    data[var] = batch.get_model_vars_dataframe()

directory = os.chdir("data/")
for i, var in enumerate(problem['names']):
    name = "ofat_{}_{}___repli_{}__dist_samp_{}.csv".format(
        truck_strategy, var, replicates, distinct_samples)
    data[var].to_csv(name)


##########################################################################
##########################################################################
##########################################################################
# OFAT with truck_strategy #2
directory = os.chdir("../")
truck_strategy = 2
problem = {
    'num_vars': 3,
    'names': ['wind_strength', 'num_firetruck', 'truck_strategy'],
    'bounds': [[0, 30], [0, 60], [truck_strategy]]
}

# Set the repetitions, the amount of steps, and the amount of distinct
# values per variable

# Set the outputs

model_reporters = {"On Fire": lambda m: m.count_total_fire,
                   "Extinguished": lambda m: m.count_extinguished_fires(m),
                   "Step": lambda m: m.current_step}


data = {}

for i, var in enumerate(problem['names']):
    # Get the bounds for this variable and get <distinct_samples> samples
    # within this space (uniform)
    if var != 'truck_strategy':
        samples = np.linspace(*problem['bounds'][i], num=distinct_samples)

    # firetrucks need to be integers.
    if var == 'num_firetruck':
        samples = np.linspace(
            *problem['bounds'][i],
            num=distinct_samples,
            dtype=int)

    if var == 'truck_strategy':
        samples = np.linspace(1, 1, 1)

    batch = BatchRunnerMP(
        ForestFire,
        iterations=replicates,
        variable_parameters={var: samples},
        model_reporters=model_reporters,
        display_progress=True, nr_processes=n_cores)

    batch.run_all()

    data[var] = batch.get_model_vars_dataframe()

directory = os.chdir("data/")
for i, var in enumerate(problem['names']):
    name = "ofat_{}_{}___repli_{}__dist_samp_{}.csv".format(
        truck_strategy, var, replicates, distinct_samples)
    data[var].to_csv(name)


##########################################################################
##########################################################################
##########################################################################
# OFAT with truck_strategy #3
directory = os.chdir("../")
truck_strategy = 3
problem = {
    'num_vars': 3,
    'names': ['wind_strength', 'num_firetruck', 'truck_strategy'],
    'bounds': [[0, 30], [0, 60], [truck_strategy]]
}

# Set the repetitions, the amount of steps, and the amount of distinct
# values per variable

# Set the outputs

model_reporters = {"On Fire": lambda m: m.count_total_fire,
                   "Extinguished": lambda m: m.count_extinguished_fires(m),
                   "Step": lambda m: m.current_step}


data = {}

for i, var in enumerate(problem['names']):
    # Get the bounds for this variable and get <distinct_samples> samples
    # within this space (uniform)
    if var != 'truck_strategy':
        samples = np.linspace(*problem['bounds'][i], num=distinct_samples)

    # firetrucks need to be integers.
    if var == 'num_firetruck':
        samples = np.linspace(
            *problem['bounds'][i],
            num=distinct_samples,
            dtype=int)

    if var == 'truck_strategy':
        samples = np.linspace(1, 1, 1)

    batch = BatchRunnerMP(
        ForestFire,
        iterations=replicates,
        variable_parameters={var: samples},
        model_reporters=model_reporters,
        display_progress=True, nr_processes=n_cores)

    batch.run_all()

    data[var] = batch.get_model_vars_dataframe()

directory = os.chdir("data/")
for i, var in enumerate(problem['names']):
    name = "ofat_{}_{}___repli_{}__dist_samp_{}.csv".format(
        truck_strategy, var, replicates, distinct_samples)
    data[var].to_csv(name)

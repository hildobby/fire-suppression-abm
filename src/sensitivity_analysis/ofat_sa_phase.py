#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 15:30:03 2020

This code was implemented by
Louis Weyland & Robin van den Berg, Philippe Nicolau, Hildebert Mouilé & Wiebe Jelsma

"""
import sys
sys.path.append('../')

import os
from mesa.batchrunner import BatchRunnerMP
import numpy as np
from forestfiremodel_SA_phase import ForestFire
import matplotlib.pyplot as plt


try:
    import pathos
except BaseException:
    print("Nanana that's what i though ! You need to install pathos")
    raise

# set the number of cores
n_cores = 3

# Set the repetitions, the amount of steps, and the amount of distinct
# values per variable
replicates = 20
distinct_samples = 20


##########################################################################
##########################################################################
##########################################################################


problem = {
    'num_vars': 1,
    'names': ['density'],
    'bounds': [[0, 1]]
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


    batch = BatchRunnerMP(
        ForestFire,
        iterations=replicates,
        variable_parameters={var: samples},
        model_reporters=model_reporters,
        display_progress=True, nr_processes=n_cores)

    batch.run_all()

    data[var] = batch.get_model_vars_dataframe()



param=['On Fire', 'Step']

for i, var in enumerate(problem['names']):
    f, axs = plt.subplots(1, figsize=(7, 10))
    x = data[var].groupby(var).mean().reset_index()[var]
    y = data[var].groupby(var).mean()[param[0]]

    replicates = data[var].groupby(var)[param[0]].count()
    err = (1.96 * data[var].groupby(var)[param[0]].std()) / np.sqrt(replicates)

    axs.plot(x, y, c='k')
    axs.fill_between(x, y - err, y + err)

    axs.set_xlabel(var)
    axs.set_ylabel(param[0])


plt.show()



directory = os.chdir("data/")
for i, var in enumerate(problem['names']):
    name = "ofat_{}___repli_{}__dist_samp_{}.csv".format(
        var,replicates,distinct_samples)
    data[var].to_csv(name)


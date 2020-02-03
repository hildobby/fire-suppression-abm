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
import time

begin = time.time()


try:
    import pathos
except BaseException:
    print("Nanana that's what i though ! You need to install pathos")
    raise

# set the number of cores
n_cores = 22

# Set the repetitions, the amount of steps, and the amount of distinct
# values per variable
replicates = 50
distinct_samples = 30


##########################################################################
##########################################################################
##########################################################################


# problem = {
#     'num_vars': 1,
#     'names': ['density'],
#     'bounds': [[0, 1]]
# }

problem = {
    'num_vars': 1,
    'names': ['truck_max_speed'],
    'bounds': [[1, 30]]
}

truck_strategy = 3

print("this is a run with {} and {}".format(truck_strategy, problem['names'][0]))

# problem = {
#     'num_vars': 1,
#     'names': ['wind_strength'],
#     'bounds': [[0, 30]]
# }

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

    # steps need to be integers.
    if var == 'truck_max_speed':
        samples = np.linspace(
            *problem['bounds'][i],
            num=distinct_samples,
            dtype=int)

    if var == 'truck_strategy':
        samples = np.linspace(0, 0, 1)

    batch = BatchRunnerMP(
        ForestFire,
        iterations=replicates,
        variable_parameters={var: samples},
        model_reporters=model_reporters,
        display_progress=True, nr_processes=n_cores)

    batch.run_all()
    data[var] = batch.get_model_vars_dataframe()


param = ['On Fire']


for i, var in enumerate(problem['names']):
    f, axs = plt.subplots(1, figsize=(10, 7))
    x = data[var].groupby(var).mean().reset_index()[var]
    y = data[var].groupby(var).mean()[param[0]]

    err = (1.96 * data[var].groupby(var)[param[0]].std()) / np.sqrt(replicates)

    axs.plot(x, y, c='k')
    axs.fill_between(x, y - err, y + err, color='grey')

    axs.set_xlabel("Wind speed (m/s)", fontweight='bold', fontsize=20)
    axs.set_ylabel("Burnt fraction", fontweight='bold', fontsize=20)
    axs.set_xlim(1, 7)


directory = os.chdir("data/")
for i, var in enumerate(problem['names']):
    name = "truckstrategy_{}_ofat_{}___repli_{}__dist_samp_{}.csv".format(
        truck_strategy, var, replicates, distinct_samples)
    data[var].to_csv(name)

plt.savefig("truckstrategy_{}_ofat_{}___repli_{}__dist_samp_{}.png".format(
    truck_strategy, var, replicates, distinct_samples), dpi=300)

# print("Mean of the number of extinguished trees: ", data["truck_strategy"]["Extinguished"].mean())
# print("Variance of the number of extinguished trees: ", data["truck_strategy"]["Extinguished"].var())

# print("Mean of the number of extinguished trees: ", data["truck_strategy"]["Extinguished"].mean())
# print("Variance of the number of extinguished trees: ", data["truck_strategy"]["Extinguished"].var())
#
# print("Mean of the number of burned trees: ", data["truck_strategy"]["On Fire"].mean())
# print("Variance of the number of burned trees: ", data["truck_strategy"]["On Fire"].var())
#
# hist = data["truck_strategy"]["On Fire"].hist()
# hist.set_xlabel("Burned (%)", fontweight='bold', fontsize=20)
# hist.set_ylabel("Occurrence (#)", fontweight='bold', fontsize=20)
#
# plt.savefig("hist_truckstrategy_1_ofat_{}___repli_{}__dist_samp_{}.png".\
#               format(var, replicates, distinct_samples), dpi=300)
#
#
# print("Mean of the number of steps to end: ", data["truck_strategy"]["Step"].mean())
# print("Variance of the number of steps to end: ", data["truck_strategy"]["Step"].var())

end = time.time()

print("This took: ", (end - begin))

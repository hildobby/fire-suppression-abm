#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 15:30:03 2020

This code was implemented by
Louis Weyland & Robin van den Berg, Philippe Nicolau, Hildebert Mouilé & Wiebe Jelsma

"""

import sys
sys.path.append('../')
import pandas as pd
import os
from mesa.batchrunner import BatchRunnerMP
import numpy as np
from forestfiremodel_sa import ForestFire
import matplotlib.pyplot as plt
import time
'''
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
replicates = 1000
distinct_samples = 1

# set the variable to do the OFAT on
ofat_var='truck_strategy'
lower_bound=0
upper_bound=1

# set the strategy for which to do the sensitivity analysis
truck_strategy = 0

##########################################################################
##########################################################################
##########################################################################


problem = {
    'num_vars': 1,
    'names': [ofat_var],
    'bounds': [[lower_bound, upper_bound]]
}


print("this is a run with {} and {}".format(truck_strategy, problem['names'][0]))

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
        samples = np.linspace(truck_strategy, truck_strategy, 1)

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

    axs.set_xlabel(var, fontweight='bold', fontsize=20)
    axs.set_ylabel("Burnt fraction", fontweight='bold', fontsize=20)
    axs.set_xlim(lower_bound, upper_bound)


directory = os.chdir("data/")
for i, var in enumerate(problem['names']):
    name = "truckstrategy_{}_ofat_{}___repli_{}__dist_samp_{}.csv".format(
        truck_strategy, ofat_var, replicates, distinct_samples)
    data[var].to_csv(name)

plt.savefig("truckstrategy_{}_ofat_{}___repli_{}__dist_samp_{}.png".format(
    truck_strategy, ofat_var, replicates, distinct_samples), dpi=300)

print("Mean of the number of extinguished trees: ", data["truck_strategy"]["Extinguished"].mean())
print("Variance of the number of extinguished trees: ", data["truck_strategy"]["Extinguished"].var())

print("Mean of the number of extinguished trees: ", data["truck_strategy"]["Extinguished"].mean())
print("Variance of the number of extinguished trees: ", data["truck_strategy"]["Extinguished"].var())

print("Mean of the number of burned trees: ", data["truck_strategy"]["On Fire"].mean())
print("Variance of the number of burned trees: ", data["truck_strategy"]["On Fire"].var())
'''
# To plot histogram
directory = os.chdir("data/")
file_name = ["truckstrategy_0_ofat_truck_strategy___repli_1000__dist_samp_1.csv",
             "truckstrategy_1_ofat_truck_strategy___repli_1000__dist_samp_1.csv",
             "truckstrategy_2_ofat_truck_strategy___repli_1000__dist_samp_1.csv",
             "truckstrategy_3_ofat_truck_strategy___repli_1000__dist_samp_1.csv",
             "truckstrategy_4_ofat_truck_strategy___repli_1000__dist_samp_1.csv"]


for i in file_name:

    data=pd.read_csv(i)

    f, axs = plt.subplots(1, figsize=(10, 7))


    if i =='truckstrategy_0_ofat_truck_strategy___repli_1000__dist_samp_1.csv' or \
            i=='truckstrategy_4_ofat_truck_strategy___repli_1000__dist_samp_1.csv':

        hist = data["On Fire"].hist(range=(0.90,1))

    else:
        hist = data["On Fire"].hist()

    hist.set_xlabel("Burnt ", fontweight='bold', fontsize=20)
    hist.set_ylabel("Occurrence (#)", fontweight='bold', fontsize=20)
    axs.xaxis.set_tick_params(labelsize=20)
    axs.yaxis.set_tick_params(labelsize=20)
    plt.xlim(0, 1)
   
    #plt.savefig("hist_truckstrategy_{}_ofat_{}___repli_{}__dist_samp_{}.png".\
    #              format(truck_strategy, var, replicates, distinct_samples), dpi=300)
    name= i.split(".")
    plt.savefig("hist_"+name[0], dpi=300)

# print("Mean of the number of steps to end: ", data["truck_strategy"]["Step"].mean())
# print("Variance of the number of steps to end: ", data["truck_strategy"]["Step"].var())

# end = time.time()

# print("This took: ", (end - begin))

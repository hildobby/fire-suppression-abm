#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 15:30:03 2020

This code was implemented by
Louis Weyland & Robin van den Berg, Philippe Nicolau, Hildebert Mouilé & Wiebe Jelsma

"""

from SALib.sample import saltelli
from mesa.batchrunner import BatchRunner
from SALib.analyze import sobol
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from Forestfiremodel_SA import ForestFire
from IPython.display import clear_output



# Define which variable to change
problem = {
    'num_vars': 2,
    'names': ['wind_strength', 'num_firetruck'],
    'bounds': [[0, 30], [0, 60]]
}

# Set the repetitions, the amount of steps, and the amount of distinct values per variable
replicates = 4
distinct_samples = 4

# Set the outputs

model_reporters={"On Fire": lambda m: m.count_type(m, "On Fire"),
                 "Extinguished": lambda m: m.count_extinguished_fires(m)}

data = {}

for i, var in enumerate(problem['names']):
    # Get the bounds for this variable and get <distinct_samples> samples within this space (uniform)
    samples = np.linspace(*problem['bounds'][i], num=distinct_samples)


    # firetrucks need to be integers.
    if var == 'num_firetruck':
        samples = np.linspace(*problem['bounds'][i], num=distinct_samples, dtype=int)

    batch = BatchRunner(
            ForestFire,
            iterations=replicates,
            variable_parameters={var: samples},
            model_reporters=model_reporters,
            display_progress=True)

    batch.run_all()

    data[var] = batch.get_model_vars_dataframe()


def plot_param_var_conf(ax, df, var, param, i):
    """
    Helper function for plot_all_vars. Plots the individual parameter vs
    variables passed.

    Args:
        ax: the axis to plot to
        df: dataframe that holds the data to be plotted
        var: variables to be taken from the dataframe
        param: which output variable to plot
    """
    x = df.groupby(var).mean().reset_index()[var]
    y = df.groupby(var).mean()[param]

    replicates = df.groupby(var)[param].count()
    err = (1.96 * df.groupby(var)[param].std()) / np.sqrt(replicates)

    ax.plot(x, y, c='k')
    ax.fill_between(x, y - err, y + err)

    ax.set_xlabel(var)
    ax.set_ylabel(param)


def plot_all_vars(df, param):
    """
    Plots the parameters passed vs each of the output variables.

    Args:
        df: dataframe that holds all data
        param: the parameter to be plotted
    """

    f, axs = plt.subplots(3, figsize=(7, 10))

    for i, var in enumerate(problem['names']):
        plot_param_var_conf(axs[i], data[var], var, param, i)


for param in ("On Fire",  "Extinguished"):
    plot_all_vars(data, param)
    plt.show()

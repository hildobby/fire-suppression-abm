#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 15:30:03 2020

This code was implemented by
Louis Weyland & Robin van den Berg, Philippe Nicolau, Hildebert Mouilé & Wiebe Jelsma

"""
import matplotlib.pyplot as plt
import os
import pandas as pd

directory = os.chdir("data/")


# data_truck_strategy
data_1 = {}
data_2 = {}
data_3 = {}

# Load the files into dict
for filename in os.listdir('.'):
    if filename.startswith("ofat_1"):
        data_1[filename.split('.csv')[0]] = pd.read_csv(filename)

for filename in os.listdir('.'):
    if filename.startswith("ofat_2"):
        data_2[filename.split('.csv')[0]] = pd.read_csv(filename)


for filename in os.listdir('.'):
    if filename.startswith("ofat_3"):
        data_3[filename.split('.csv')[0]] = pd.read_csv(filename)


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

    f, axs = plt.subplots(3)

    for i, var in enumerate(problem['names']):
        plot_param_var_conf(axs[i], data[var], var, param, i)


for param in ("On Fire", "Extinguished", "Step"):
    plot_all_vars(data, param)
    plt.show()

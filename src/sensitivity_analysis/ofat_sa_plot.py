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
import numpy as np

directory = os.chdir("data/")


# data_truck_strategy
data_1 = {}
data_2 = {}
data_3 = {}

list_var = ['wind_strength', 'num_firetruck']
rep = 5
dist = 5

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


for var in list_var:

    # number of strategies
    for i in range(1,4):
        globals()['x_{}_%s'.format(var) % i]= eval("data_" + str(i))["ofat_{}_{}___repli_{}__dist_samp_{}"\
            .format(i,var,rep,dist)].groupby(var).mean().reset_index()[var]

        param = "On Fire"
        globals()['y_{}_on_fire_%s'.format(var) % i]=eval("data_" + str(i))["ofat_{}_{}___repli_{}__dist_samp_{}"\
            .format(i,var,rep,dist)].groupby(var).mean()[param]
        globals()['err_{}_fire_%s'.format(var) % i] = (1.96 * eval("data_" + str(i))\
            ["ofat_{}_{}___repli_{}__dist_samp_{}".format(i,var,rep,dist)].groupby(var)[param].std()) / np.sqrt(rep)

        param = "Step"
        globals()['y_{}_step_%s'.format(var) % i] =eval("data_" + str(i))["ofat_{}_{}___repli_{}__dist_samp_{}"\
            .format(i,var,rep,dist)].groupby(var).mean()[param]
        globals()['err_{}_step_%s'.format(var) % i] = (1.96 * eval("data_" + str(i))\
            ["ofat_{}_{}___repli_{}__dist_samp_{}".format(i,var,rep,dist)].groupby(var)[param].std()) / np.sqrt(rep)

        param = "Extinguished"
        globals()['y_{}_extinguish_%s'.format(var) % i] =eval("data_" + str(i))["ofat_{}_{}___repli_{}__dist_samp_{}"\
            .format(i,var,rep,dist)].groupby(var).mean()[param]
        globals()['err_{}_extinguish_%s'.format(var) % i] = (1.96 * eval("data_" + str(i))\
            ["ofat_{}_{}___repli_{}__dist_samp_{}".format(i,var,rep,dist)].groupby(var)[param].std()) / np.sqrt(rep)

    f, ax = plt.subplots(3, figsize=(7, 10))
    for i in range(1, 4):
        ax[0].plot(globals()['x_{}_%s'.format(var) % i], globals()[('y_{}_on_fire_%s'.format(var) % i)],label=i)
        ax[0].fill_between(globals()['x_{}_%s'.format(var) % i], \
                           globals()[('y_{}_on_fire_%s'.format(var) % i)] -\
                           globals()['err_{}_fire_%s'.format(var) % i], globals()[('y_{}_on_fire_%s'.format(var) % i)]\
                           +globals()['err_{}_fire_%s'.format(var) % i],alpha=0.7)
        ax[0].set_xlabel(var)
        ax[0].set_ylabel("On Fire")

        ax[0].legend()

        ax[1].plot(globals()['x_{}_%s'.format(var) % i], globals()[('y_{}_step_%s'.format(var) % i)],label=i)
        ax[1].fill_between(globals()['x_{}_%s'.format(var) % i], \
                           globals()[('y_{}_step_%s'.format(var) % i)] -\
                           globals()['err_{}_step_%s'.format(var) % i], globals()[('y_{}_step_%s'.format(var) % i)]\
                           +globals()['err_{}_step_%s'.format(var) % i],alpha=0.7)
        ax[1].set_xlabel(var)
        ax[1].set_ylabel("Step")
        ax[1].legend()


        ax[2].plot(globals()['x_{}_%s'.format(var) % i], globals()[('y_{}_extinguish_%s'.format(var) % i)],label=i)
        ax[2].fill_between(globals()['x_{}_%s'.format(var) % i], \
                          globals()[('y_{}_extinguish_%s'.format(var) % i)] -\
                           globals()['err_{}_extinguish_%s'.format(var) % i], globals()[('y_{}_extinguish_%s'.format(var) % i)]\
                           +globals()['err_{}_extinguish_%s'.format(var) % i],alpha=0.7)
        ax[2].set_xlabel(var)
        ax[2].set_ylabel("Extinguished")
        ax[2].legend()






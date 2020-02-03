#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 15:30:03 2020

This code was implemented by
Louis Weyland & Robin van den Berg, Philippe Nicolau, Hildebert Mouilé & Wiebe Jelsma

"""
import sys
sys.path.append('../')
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np

directory = os.chdir("data/")


# data_truck_strategy
data_1 = {}
data_2 = {}
data_3 = {}

plot_name = 'sensitivity_sparse_ratio_V1'
x_label = 'sparse ratio'
var = 'sparse_ratio'
param = 'On Fire'

file_name = ["truckstrategy_0_ofat_sparse_ratio___repli_50__dist_samp_25.csv",
             "truckstrategy_1_ofat_sparse_ratio___repli_50__dist_samp_25.csv",
             "truckstrategy_2_ofat_sparse_ratio___repli_50__dist_samp_25.csv",
             "truckstrategy_3_ofat_sparse_ratio___repli_50__dist_samp_25.csv"]

f, ax = plt.subplots(1, figsize=(10, 7))

for i in range(len(file_name)):
    # to plot the lines
    df = pd.read_csv(file_name[i])

    x = df.groupby(var).mean().reset_index()[var]
    y = df.groupby(var).mean()[param]

    replicates = df.groupby(var)[param].count()
    err = (1.96 * df.groupby(var)[param].std()) / np.sqrt(replicates)

    ax.plot(x, y, c='k')
    ax.fill_between(x, y - err, y + err)

ax.set_xlabel(x_label, fontweight='bold', fontsize=20)
ax.set_ylabel('burnt/fine vegetation', fontweight='bold', fontsize=20)
ax.legend(["Random", "Closest", "Newest", "Parallel"])
leg = ax.get_legend()
leg.legendHandles[0].set_color('blue')
leg.legendHandles[1].set_color('orange')
leg.legendHandles[2].set_color('green')
leg.legendHandles[3].set_color('red')

ax.xaxis.set_tick_params(labelsize=20)
ax.yaxis.set_tick_params(labelsize=20)

ax.set_xticks(np.arange(0, 1, 0.2))


plt.xlim([0, 1])
plt.ylim([0, 1.05])
plt.savefig(plot_name, dpi=300)
plt.show()

'''
# Load the files into dict
for filename in os.listdir('.'):
    if filename.startswith("ofat_sparse_ratio___repli_50__dist_samp_50"):
        data_1[filename.split('.csv')[0]] = pd.read_csv(filename)

for filename in os.listdir('.'):
    if filename.startswith("truckstrategy_2"):
        data_2[filename.split('.csv')[0]] = pd.read_csv(filename)


for filename in os.listdir('.'):
    if filename.startswith("truckstrategy_3"):
        data_3[filename.split('.csv')[0]] = pd.read_csv(filename)
'''

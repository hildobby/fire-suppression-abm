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

var = 'num_firetruck'
x_label = 'Number of firetrucks #'
param = 'On Fire'
replicates = 100
distinct_samples = 1
file_name = 'truckstrategy_0_ofat_truck_strategy___repli_100__dist_samp_1.csv'
plot_name = 'hist_truckstrategy_0_ofat_truck_strategy___repli_100__dist_samp_1'


# To plot Histo
data = pd.read_csv(file_name)
f, axs = plt.subplots(1, figsize=(10, 7))
hist = data["On Fire"].hist(range=(0.9,1))
hist.set_xlabel("Burnt ", fontweight='bold', fontsize=20)
hist.set_ylabel("Occurrence (#)", fontweight='bold', fontsize=20)
axs.xaxis.set_tick_params(labelsize=20)
axs.yaxis.set_tick_params(labelsize=20)
plt.xlim([0, 1.01])


plt.savefig("hist_truckstrategy_1_ofat_{}___repli_{}__dist_samp_{}.png".\
           format(var, replicates, distinct_samples), dpi=300)




''''

# to plot the lines
df = pd.read_csv(file_name)

x = df.groupby(var).mean().reset_index()[var]
y = df.groupby(var).mean()[param]

replicates = df.groupby(var)[param].count()
err = (1.96 * df.groupby(var)[param].std()) / np.sqrt(replicates)


f, ax = plt.subplots(1, figsize=(10, 7))

ax.plot(x, y, c='k')
ax.fill_between(x, y - err, y + err, color='gray')

ax.set_xlabel(x_label, fontweight='bold', fontsize=20)
ax.set_ylabel('Forest burnt', fontweight='bold', fontsize=20)

ax.xaxis.set_tick_params(labelsize=20)
ax.yaxis.set_tick_params(labelsize=20)

ax.set_xticks(range(1, 30, 6))


plt.xlim([1, 30])
plt.ylim([0, .5])
plt.show()
plt.savefig(plot_name, dpi=300)


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









for var in list_var:

    # number of strategies
    for i in range(1, 4):
        globals()['x_{}_%s'.format(var) % i] = eval("data_" + str(i))["ofat_{}_{}___repli_{}__dist_samp_{}"
                                                                      .format(i, var, rep, dist)].groupby(var)\
            .mean().reset_index()[var]

        param = "On Fire"
        globals()['y_{}_on_fire_%s'.format(var) % i] = eval("data_" + str(i))["ofat_{}_{}___repli_{}__dist_samp_{}"
                                                                              .format(i, var, rep, dist)]\
            .groupby(var).mean()[param]
        globals()['err_{}_fire_%s'.format(var) % i] = (1.96 * eval("data_" + str(i))
                                                       ["ofat_{}_{}___repli_{}__dist_samp_{}"
                                                        .format(i, var, rep, dist)]
                                                       .groupby(var)[param].std()) / np.sqrt(rep)

        param = "Step"
        globals()['y_{}_step_%s'.format(var) % i] = eval("data_" + str(i))["ofat_{}_{}___repli_{}__dist_samp_{}"
                                                                           .format(i, var, rep, dist)]\
            .groupby(var).mean()[param]
        globals()['err_{}_step_%s'.format(var) % i] = (1.96 * eval("data_" + str(i))
                                                       ["ofat_{}_{}___repli_{}__dist_samp_{}"
                                                        .format(i, var, rep, dist)]
                                                       .groupby(var)[param].std()) / np.sqrt(rep)

        param = "Extinguished"
        globals()['y_{}_extinguish_%s'.format(var) % i] = eval("data_" + str(i))["ofat_{}_{}___repli_{}__dist_samp_{}"
                                                                                 .format(i, var, rep, dist)]\
            .groupby(var).mean()[param]
        globals()['err_{}_extinguish_%s'.format(var) % i] = (1.96 * eval("data_" + str(i))
                                                             ["ofat_{}_{}___repli_{}__dist_samp_{}"
                                                              .format(i, var, rep, dist)]
                                                             .groupby(var)[param].std()) / np.sqrt(rep)

    f, ax = plt.subplots(3, figsize=(7, 10))
    for i in range(1, 4):
        ax[0].plot(
            globals()['x_{}_%s'.format(var) % i], globals()[('y_{}_on_fire_%s'.format(var) % i)], label=i)
        ax[0].fill_between(
            globals()['x_{}_%s'.format(var) % i],
            globals()[('y_{}_on_fire_%s'.format(var) % i)] - globals()['err_{}_fire_%s'.format(var) % i],
            globals()[('y_{}_on_fire_%s'.format(var) % i)] + globals()['err_{}_fire_%s'.format(var) % i], alpha=0.7)
        ax[0].set_xlabel(var)
        ax[0].set_ylabel("On Fire")
        ax[0].legend()

        ax[1].plot(
            globals()['x_{}_%s'.format(var) % i], globals()[('y_{}_step_%s'.format(var) % i)], label=i)
        ax[1].fill_between(
            globals()['x_{}_%s'.format(var) % i],
            globals()[('y_{}_step_%s'.format(var) % i)] - globals()['err_{}_step_%s'.format(var) % i],
            globals()[('y_{}_step_%s'.format(var) % i)] + globals()['err_{}_step_%s'.format(var) % i], alpha=0.7)
        ax[1].set_xlabel(var)
        ax[1].set_ylabel("Step")
        ax[1].legend()

        ax[2].plot(
            globals()['x_{}_%s'.format(var) % i], globals()[('y_{}_extinguish_%s'.format(var) % i)], label=i)
        ax[2].fill_between(
            globals()['x_{}_%s'.format(var) % i],
            globals()[('y_{}_extinguish_%s'.format(var) % i)] - globals()['err_{}_extinguish_%s'.format(var) % i],
            globals()[('y_{}_extinguish_%s'.format(var) % i)] + globals()['err_{}_extinguish_%s'.format(var) % i],
            alpha=0.7)
        ax[2].set_xlabel(var)
        ax[2].set_ylabel("Extinguished")
        ax[2].legend()


'''

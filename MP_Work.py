from __future__ import division
from pandas import Series, DataFrame
from scipy.stats import ttest_ind
import pandas as pd
import numpy as np
import os
import xlrd
import time
import matplotlib.pyplot as plt

df = pd.read_csv("C:\Users\Matt\Dropbox\MP\MP Final Report\Survey Graphs and Summary.csv")

govtlevel = DataFrame(df['Govt Level'])

govtlevel1 = df['Q3']
govtlevel.plot(govtlevel['Govt Level'], kind = 'bar')

govtlevel1.plot(kind = 'hist')

fig1 = plt.figure() ##initializing plot
ax1 = plot(govtlevel["Govt Level"], kind = 'bar')
ax1 = fig1.add_subplot(2, 1, 1) ##two rows, one column, one plot
ax1.plot(govtlevel.plot(kind = 'hist'))
ax1.axhline(2, color = 'r', linestyle = '--')
ax1.set_title('t-stats over-time')

ax2 = fig1.add_subplot(2, 1, 2) ##two rows, one column, one plot
ax2.plot(t_p['pval'])
ax2.axhline(0.05, color = 'r', linestyle = '--')
ax2.set_title('p-values over-time')

fig, axes = plt.subplots(2,1)
govtlevel1.plot(kind = 'bar', ax = axes[0], color = 'k')

fig, axes = plt.subplots(2,1)
data = Series(np.random.rand(16), index = list('abcdefghijklmnop'))
data.plot(kind = 'bar', ax = axes[0], color = 'k', alpha = 0.7)
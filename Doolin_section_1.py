######################################################################
#PUBPOL 590-Big Data Analysis
#Final Project
#Section 1
######################################################################

from __future__ import division
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import os
import statsmodels.api as sm
import matplotlib.pyplot as plt

main_dir = "C:\Users\Matt\Documents\Nicholas School-2nd Year\Spring 2015\Big Data Analysis"
root = main_dir + "\Python\Data\\"

##################################################################
#Part A
##################################################################

#Pathing and Stacking Gas Data
paths = [root + v for v in os.listdir(root) if v.startswith("gas_long_redux")]
df = pd.concat([pd.read_csv(v) for v in paths], ignore_index = True)

#Cleaning Data
##Missing values
df.kwh.isnull()
df = df.fillna(0)

#Negative Values
df[df < 0] = 0

#Dropping Duplicated ID and Dates
df.duplicated(['ID', 'date_cer'])
df = df.drop_duplicates(['ID', 'date_cer'])

print "\n\n\n"
print df.shape
print df.kwh.mean()

################################################
#Part B
################################################

#importing additional data
allocation = pd.read_csv(root + 'residential_allocations.csv', usecols = [0,1])
timeseries = pd.read_csv(root + 'time_correction.csv')

df = pd.merge(df, allocation, on = 'ID')
#creating hour_cer column to merge on
df['hour_cer'] = df['date_cer'] % 100
df['day_cer'] = df['date_cer'] // 100

df = df.reset_index()
#merging datasets
df = pd.merge(df, timeseries, on = ['day_cer', 'hour_cer'])
df = df.sort(['index']).reset_index()

del df['index']
del df['level_0']

print "\n\n\n"
print df[df.ID == 1021].head(20)

##################################################
#Part C
##################################################

#Aggregating by month
grp = df.groupby(['year', 'month', 'ID', 'allocation'])

df1 = grp['kwh'].sum().reset_index()
df1['mo_str'] = ['0' + str(v) if v < 10 else str(v) for v in df1['month']]
df1['kwh_ym'] = 'kwh_' + df1.year.apply(str) + "_" + df1.mo_str.apply(str)

#pivoting from long to wide
df_piv = df1.pivot('ID', 'kwh_ym', 'kwh')
df_piv.reset_index(inplace = True)
df_piv.columns.name = None

df_piv

print "\n\n\n"
print df_piv.shape
print df_piv.head()

###################################################
#Part D
###################################################

grps = df1.groupby(['kwh_ym','allocation'])
grps_mean = grps.mean().unstack('allocation')
grps_mean['kwh'].plot()
plt.show()

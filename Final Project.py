from __future__ import division
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import os
import statsmodels.api as sm

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

allocation = pd.read_csv(root + 'residential_allocations.csv', usecols = [0,1])
timeseries = pd.read_csv(root + 'time_correction.csv')

df['hour_cer'] = df['date_cer'] % 100

df1 = pd.merge(df, allocation, timeseries)







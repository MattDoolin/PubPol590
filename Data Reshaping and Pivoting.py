from __future__ import division
from pandas import Series, DataFrame
from scipy.stats import ttest_ind
from datetime import datetime, timedelta
from dateutil import parser
import pandas as pd
import numpy as np
import os
import xlrd
import pytz 
import time
import matplotlib.pyplot as plt

main_dir = "C:\Users\Matt\Documents\Nicholas School-2nd Year\Spring 2015\Big Data Analysis"
root = main_dir + "\Python\Data\\"

#Import Data
#header = 0 is saying that first row is header, no header would be header = null
df = pd.read_csv(root + "sample_30min.csv", header = 0, parse_dates = [1], date_parser = parser.parse)

df_assign = pd.read_csv(root + "sample_assignments.csv", usecols = [0,1])
df = pd.merge(df, df_assign)

##add/drop variables
df['year'] = df['date'].apply(lambda x: x.year)
df['month'] = df['date'].apply(lambda x: x.month)
df['day'] = df['date'].apply(lambda x: x.day)
df['ymd'] = df['date'].apply(lambda x: x.date())

# daily aggregate
grp = df.groupby(['year', 'month', 'day', 'panid', 'assignment'])
grp = df.groupby(['ymd', 'panid', 'assignment'])
df1 = grp['kwh'].sum().reset_index()

##Pivoting Data (Reshape)


# go from 'long' to 'wide'

## 1. create column names for wide date
# create strings names and denote consumption and date
# use ternery expression: [true-expr(x) if conditions else false-expr(x) for x in list]
#df1['day_str'] = ['0' + str(v) if v < 10 else str(v) for v in df1['date']] # Want to add a zero to days less than 10
#df1['kwh_ymd'] = 'kwh_' + df1.year.apply(str) + '_' + df1.month.apply(str) + '_' + df1.day_str.apply(str)

df1['kwh_ymd'] = 'kwh_' + df1['ymd'].apply(str)

# 2. pivot---long to wide data
#first thing in function is the individual identifier, in this case panid
#Second thing is the columns we want which is kwh_plus the ymd value
#Third thing is what you want at each row/column intersection, in this case kwh
df1_piv = df1.pivot('panid', 'kwh_ymd', 'kwh')
df1_piv

#clean up to make table pretty
df1_piv.reset_index(inplace = True) # this makes panid its own variable
df1_piv.columns.name = None

# Merge Time invariant Data
df2 = pd.merge(df_assign, df1_piv) #attaching order to put assignment value at the front
#export data for regression
df2.to_csv(root + "07_kwh_wide.csv", sep = ",", index = False)
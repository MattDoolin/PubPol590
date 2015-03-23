from __future__ import division
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os
import xlrd
import pytz 
from datetime import datetime, timedelta
import time
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt

main_dir = "C:\Users\Matt\Documents\Nicholas School-2nd Year\Spring 2015\Big Data Analysis"
root = main_dir + "\Python\Data\\"

#import and mergedata
df = pd.read_csv(root + "sample_30min.csv", header = 0, parse_dates = [1])
df_assign = pd.read_csv(root + 'sample_assignments.csv', usecols = [0,1])

df = pd.merge(df, df_assign)

##Timestamp Data
df['date'][0] #provides the time stamp for row 0
df['date'][0].day #provides the day for row 0
df['date'][0].month #provides month

#NEW Variables
#anonymous function--applies to every value in series
#provides year in new column extracted from time stamp
df['year'] = df['date'].apply(lambda x: x.year)
df['month'] = df['date'].apply(lambda x: x.month)
df['day'] = df['date'].apply(lambda x: x.day)
df['ymd'] = df['date'].apply(lambda x: x.date())


##df now has new year, month, and day columns--now can group over the month or day
    ##as opposed to the 30 minute interval data that we had
#df.head shows the first 100 rows
df.head(100)

# AGGREGATION (DAILY)
grp = df.groupby(['year', 'month', 'day', 'panid', 'assignment'])

#want to aggregate all row indices that have same year, day, and
#for each of these groups apply the sum function but only to kwh
agg = grp['kwh'].sum()
##Converts dataframe back to normal look
agg = agg.reset_index()
#makes two assignments for each day
grp1 = agg.groupby(['year', 'month', 'day', 'assignment'])
grp1.head()
grp1.groups #shows the dictionary

#splitting data up into trtment and ctrl
## 0,1,2, 3 are the indeces for the columns from grp1 key
trt = {(k[0], k[1], k[2]): agg.kwh[v].values for k, v in grp1.groups.iteritems() if k[3] == 'T'}
ctrl = {(k[0], k[1], k[2]): agg.kwh[v].values for k, v in grp1.groups.iteritems() if k[3] == 'C'}

keys = ctrl.keys()

# tstats and pvalues
tstats = DataFrame([(k, np.abs(float(ttest_ind(trt[k], ctrl[k], equal_var = False)[0]))) for k in keys], columns = ['ymd', 'tstat'])
pvals = DataFrame([(k, (ttest_ind(trt[k], ctrl[k], equal_var = False)[1])) for k in keys], columns = ['ymd', 'pval'])
t_p = pd.merge(tstats, pvals)

##sort and reset index
t_p.sort(['ymd'], inplace = True)
t_p.reset_index(inplace = True, drop = True)

##Plotting
fig1 = plt.figure()
p1 = fig1.add_subplot(2,1,1)
p1.plot(t_p['tstat']) 
p1.axhline(2, color = 'r', linestyle = '--')
p1.axvline(14, color = 'g', linestyle = '--')
p1.set_title("t stats over time")

p2 = fig1.add_subplot(2,1,2)
p2.plot(t_p['pval']) 
p2.axhline(0.05, color = 'r', linestyle = '--')
p2.axvline(14, color = 'g', linestyle = '--')
p2.set_title("p values over time")


#Aggregating by Month
grp2 = df.groupby(['year', 'month', 'panid', 'assignment'])

#want to aggregate all row indices that have same year, month, and
#for each of these groups apply the sum function but only to kwh
agg2 = grp2['kwh'].sum()
##Converts dataframe back to normal look
agg2 = agg2.reset_index()
#makes two assignments for each day
grp3 = agg2.groupby(['year', 'month', 'assignment'])
grp3.head()
grp3.groups #shows the dictionary

trt2 = {(k[0], k[1]): agg.kwh[v].values for k, v in grp3.groups.iteritems() if k[2] == 'T'}
ctrl2 = {(k[0], k[1]): agg.kwh[v].values for k, v in grp3.groups.iteritems() if k[2] == 'C'}

keys2 = ctrl2.keys()

# tstats and pvalues
tstats2 = DataFrame([(k, np.abs(float(ttest_ind(trt2[k], ctrl2[k], equal_var = False)[0]))) for k in keys2], columns = ['ymd', 'tstat'])
pvals2 = DataFrame([(k, (ttest_ind(trt2[k], ctrl2[k], equal_var = False)[1])) for k in keys2], columns = ['ymd', 'pval'])
t_p2 = pd.merge(tstats2, pvals2)

##sort and reset index
t_p2.sort(['ymd'], inplace = True)
t_p2.reset_index(inplace = True, drop = True)

##Plotting
fig2 = plt.figure()
p3 = fig2.add_subplot(2,1,1)
p3.plot(t_p2['tstat']) 
p3.axhline(2, color = 'r', linestyle = '--')
p3.axvline(14, color = 'g', linestyle = '--')
p3.set_title("t stats over time")

p4 = fig2.add_subplot(2,1,2)
p4.plot(t_p2['pval']) 
p4.axhline(0.05, color = 'r', linestyle = '--')
p4.axvline(14, color = 'g', linestyle = '--')
p4.set_title("p values over time")

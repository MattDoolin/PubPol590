from __future__ import division
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os
import xlrd #MISSION CRITICAL
import pytz #What is this
from datetime import datetime, timedelta
import time

main_dir = "C:\Users\Matt\Documents\Nicholas School-2nd Year\Spring 2015\Big Data Analysis"
root = main_dir + "\CER Electricity Data\CER Data\\"
excel_file = "\SME and Residential allocations.xlsx"
time_data = main_dir + "\CER Electricity Data\CER Data\\timeseries_correction.csv"

#missing = [".", "NA", "NULL", "-", "999999999"]

#import, iterating through a loop
paths3 = [os.path.join(root,v) for v in os.listdir(root) if v.startswith("File")]
dftotal = pd.concat([pd.read_table(v, names = ['panid', 'date', 'kwh'], sep = " ", nrows = 2000000) for v in paths3]) #Reads in 2,000,0000 rows of CER data
times = pd.read_csv(time_data, usecols = [2,3,4,5,6,9,10], parse_dates = [0]) #reads in time series data
###Day light savings###--------------------------------------------------------
#Splits up the date function into a day and hour columns, then renames the columns to match for common columns to merge on
hours = dftotal['date'] % 100
days = dftotal['date'] // 100
dftotal['day_cer'] = days
dftotal['hour_cer'] = hours
#ad_hour = times['hour_cer'][:48]

###IMPORTING AND MERGING ID DATA###---------------------------------------------
exl = pd.read_excel(main_dir + "\CER Electricity Data\CER Data\\" + excel_file, parse_cols = "A:E") #Brings in SME worksheet columns A-E
exl2 = exl[exl.Code == 3] #Only shows rows where Code is equal to 3
exl3 = exl.drop(exl2.index) #Drops out 'exl2' thereby dropping out any code value equal to 3
exl3.columns = ['panid', 'code', 'tariff', 'stim', 'SME'] #renames columns
del exl3['SME'] #delete SME column
excel = exl3[exl3.code == 1] #Only shows where Code is equal to 1 (Could possible remove the dropping Code 3 code)
idx = excel['stim'].isin(['1', 'E']) #Provides Boolean Index that is True for rows where stim is equal to 1 or E
excel = excel[idx] #Drops all values except those identified as True in idx code
tar = excel['tariff'].isin(['A', 'E']) #Same only for tarriff column equals to A and E
excel = excel[tar] #Drops all values except those ID'd as True in tar code

#MERGING DATA#
df = pd.merge(dftotal, excel, on = 'panid') #merges on Tarriff designation and CER data on panid column--SOMEHOW end up with more rows
del df['date'] #delete obsolete date column
#del df['day_cer']
#del df['minute']

#merges on both hour and day_cer columns.  Do this to avoid addition of rows to account for daylight savings time additional hours
df = pd.merge(df, times, on = ['hour_cer', 'day_cer']) 
#day and hour_cer cols no longer needed after merge
del df['hour_cer']
del df['day_cer']

#sorts by panid, then day, then hour but date is messed up
df.sort(['panid','day', 'hour'], inplace = True)

#df = pd.groupby(df, by=['panid', 'day', 'hour'])

#STATS#-------------------------------------------------------------------------
from scipy.stats import ttest_ind


##IS THIS NEEDED?
#defines treatment and control groups into own vector
trt = df['kwh'][df.tariff == 'E']
ctrl = df['kwh'][df.tariff == 'A']

#calculates tstats and pvalues 
t, p = ttest_ind(trt, ctrl, equal_var = False)


### Time Series
# DAILY AGGREGATION --------------------
grp = df.groupby(['month', 'year', 'panid', 'tariff']) 
agg = grp['kwh'].sum()


# reset the index (multilevel at the moment)
agg = agg.reset_index() # drop the multi-index
grp = agg.groupby(['month', 'year', 'tariff'])#was date

## split up treatment/control
trt = {k[0]: agg.kwh[v].values for k, v in grp.groups.iteritems() if k[2] == 'A'} # get set of all treatments by date (1 by day, 2 by month)
ctrl = {k[0]: agg.kwh[v].values for k, v in grp.groups.iteritems() if k[2] == 'E'} # get set of all controls by date (1 by day 2 by month)
keys = ctrl.keys()

#make more efficent data Frames
#provides dataframes with pval and tstat for each month
tdf = DataFrame([(k, np.abs(ttest_ind(trt[k], ctrl[k], equal_var = False)[0])) for k in keys], columns = ['date', 'tstat'])
pdf = DataFrame([(k, np.abs(ttest_ind(trt[k], ctrl[k], equal_var = False)[1])) for k in keys], columns = ['date', 'pval'])
#puts pvals and tstats into one dataframe and then sorts by date
t_p = pd.merge(tdf, pdf)
t_p.sort(['date'], inplace = True)
t_p.reset_index(inplace = True, drop = True)

#PLOTTING DATA# ----------------------------------------------------------------
import matplotlib.pyplot as plt

##plots two graphs on same plot with hor and vert lines and title
#Graphs 'tstat' column from dataframe t_p
fig1 = plt.figure()
p1 = fig1.add_subplot(2,1,1)
p1.plot(t_p['tstat']) 
p1.axvline(171, color = 'g', linestyle = '--')
p1.axhline(2, color = 'r', linestyle = '--')
plt.show()
p1.set_title("Daily T Stats")

p2 = fig1.add_subplot(2,1,2)
p2.plot(t_p['pval']) 
p2.axvline(171, color = 'g', linestyle = '--')
p2.axhline(.05, color = 'r', linestyle = '--')
p2.set_title("Daily P Values")
from __future__ import division
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os
import xlrd
import time

main_dir = "C:\Users\Matt\Documents\Nicholas School-2nd Year\Spring 2015\Big Data Analysis"
root = main_dir + "\Python\Data\\"

#PATHING
paths = [os.path.join(root, v) for v in os.listdir(root) if v.startswith('file_')]

#import and stack--also parses dates to become more standard and puts into "datetime" format
df = pd.concat([pd.read_csv(v, names = ['panid', 'date', 'kwh'], parse_dates = [1], header = None) for v in paths], ignore_index = True)

df_assign = pd.read_csv(root + 'sample_assignments_merging.csv', usecols = [0,1])

#MERGE
df = pd.merge(df, df_assign)
##sorts by panid and then by date value
df.sort(['panid', 'date'])
##GROUPBY aka 'split, apply, combine'

#pooling data together and comparing control vs. treatment values 
#ignores time
grp1 = df.groupby(['assignment'])
grp1.mean()
grp1.groups  #CAUTION..don't do this with super big data.  will crash
#Can assign .groups rather than looking at it
gd1 = grp1.groups

##looking at keys in dictionary gd1
gd1.keys() #shows unique keys (C, T) in dictionary
gd1['C']
gd1.values()[0] #no keys but just values in order
gd1.viewvalues() #see all possible values within dictionary.  More compact view

#iteration properties of a dictionary
#for loop that looks over all values of for loop and provides values of first
    #and second keys--same as gd1.values()
[v for v in gd1.itervalues()]

[k for k in gd1.iterkeys()] #same as gd1.keys()

[(k,v) for k,v in gd1.iteritems()] ##tuple of keys and then values of key
#same as gd1 only in list format rather than dictionary

##split and apply (pooled data)
grp1['kwh'].mean()
##split and apply (panel/time series data)
grp2 = df.groupby(['assignment', 'date'])
gd2 = grp2.groups
gd2 #dictionary structure--Assn, Date, Row values
gd2.keys() #doesn't give row values

grp2.mean() #breaks down by C or T and then date, and then gives mean kWh values
grp2['kwh'].mean() #just includes kWh variable and not panid

df['kwh'][[0,90,120]] #breaks out specific row values
df['kwh'][[0,90,120]].mean() #gives means for these values

##Testing for balance between C and T (Over Time)
from scipy.stats import ttest_ind

## ex using ttest_ind
a = [1, 4, 9, 2]
b = [1, 7, 8, 9]

#returns t and p values for data--can look at t or p individually or t,p together
t, p = ttest_ind(a, b, equal_var = False)

# set up data
grp = df.groupby(['assignment', 'date'])
##first two columns of assignment and date is the 'k' column, indeces of values is 'v' column
# get separate sets of treatment and control values by date
##left side is date and right side is values for that date given the assignment value is a T
trt = {k[1]: df.kwh[v].values for k, v in grp.groups.iteritems() if k[0] == 'T'}
##same as trt only given that assignment value is a C
ctrl = {k[1]: df.kwh[v].values for k, v in grp.groups.iteritems() if k[0] == 'C'}
keys = trt.keys()

##create dataframes of this information
tstats = DataFrame([(k, np.abs(ttest_ind(trt[k], ctrl[k], equal_var = False)[0])) for k in keys], columns = ['date', 'tstat'])

pvals = DataFrame([(k, np.abs(ttest_ind(trt[k], ctrl[k], equal_var = False)[1])) for k in keys], columns = ['date', 'pval'])

t_p = pd.merge(tstats, pvals)

#sort--inplace sorts the data and sorts the original dataframe
t_p.sort(['date'], inplace = True)
#Reset Index
t_p.reset_index(inplace = True, drop = True)


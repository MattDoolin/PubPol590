from __future__ import division
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os
import xlrd
import time

main_dir = "C:\Users\Matt\Documents\Nicholas School-2nd Year\Spring 2015\Big Data Analysis"
root = main_dir + "\Python\Data\\"

##Tracking computational time
start = time.time()
#place code here to time
end = time.time()
print 'total time', end-start, 'seconds'
#PATHING
paths = [os.path.join(root, v) for v in os.listdir(root) if v.startswith('file_')]

#import and stack
df = pd.concat([pd.read_csv(v, names = ['panid', 'date', 'kwh']) for v in paths], ignore_index = True)

df_assign = pd.read_csv(root + 'sample_assignments_merging.csv', usecols = [0,1])

#MERGE
df = pd.merge(df, df_assign)

##GROUPBY aka 'split, apply, combine'

#split by control and treatment (C/T), pooled without time
groups1 = df.groupby(['assignment']) #splitting by assignment
groups1.groups #shows what lines are assigned to each group (C or T)

#apply the mean

groups1['kwh'].apply(np.mean) #gives mean for each assignment
groups1['kwh'].mean() #uses internal function to give mean---faster!

#to time iterations of code--only use on small dataframes
%timeit -n 100 groups1['kwh'].apply(np.mean)
%timeit -n 100 groups1['kwh'].mean()

#split by C and T but pooling with time
groups2 = df.groupby(['assignment', 'date']) #splitting by assignment and time
groups2.groups #shows what lines are assigned to each group (C or T)

#apply the mean

groups2['kwh'].mean() #uses internal function to give mean---faster!

#different way of looking at means--order matters
groups2 = df.groupby(['date','assignment'])
groups2['kwh'].mean()

#UNSTACK---
gp_mean = groups2['kwh'].mean()
gp_unstack = gp_mean.unstack('assignment')
gp_unstack['T'] #means over time of the treatment group






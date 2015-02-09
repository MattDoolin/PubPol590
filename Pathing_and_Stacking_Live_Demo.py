#Initialize Script
from __future__ import division
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os

main_dir = "C:\Users\Matt\Documents\Nicholas School-2nd Year\Spring 2015\Big Data Analysis"
git_dir = "C:\Users\Matt\Documents\Nicholas School-2nd Year\Spring 2015\Big Data Analysis\GitHub\PubPol590"

##Advanced Pathing
#imports the four files needed using a loop function (pattern)
root = main_dir + "\Python\Data\\"
paths0 = [root + 'file_rand_' + str(v) + '.csv' for v in range (1,5)]
#Alternate methods
paths1 = [os.path.join(root, 'file_rand_%s.csv') % v for v in range(1,5)]
paths2 = [root + 'file_rand_%s.csv' % v for v in range(1,5)]

##super pro way
[v for v in os.listdir(root)]
[os.path.join(root, v) for v in os.listdir(root)]
[root + v for v in os.listdir(root)]
##need to find what they have in common to filter out what we don't want
[root + v for v in os.listdir(root) if v.startswith("file_")]
[v for v in os.listdir(root) if v.startswith('file_')]

paths3 = [root + v for v in os.listdir(root) if v.startswith("file_")]

##Import Data
list_of_dfs = [pd.read_csv(v, names = ['panid', 'date', 'kwh']) for v in paths3]
len(list_of_dfs)
type(list_of_dfs)
type(list_of_dfs[0])

#assignment data from class
df_assign = pd.read_csv(root + 'sample_assignments_merging.csv', usecols = [0,1])

#STACK AND MERGE

df = pd.concat(list_of_dfs, ignore_index = True)
df = pd.merge(df, df_assign)

#Dropping and changing row values
#create copy of df so when dropping rows we still have original dataset
df1 = df.copy()
df.drop(9)
df1.drop(range(0,9), inplace = True) #inplace option will change the dataframe

#gives the specific value in column
df['kwh'][0]
df.kwh[0]
df.kwh[range(0,5)]
df.kwh[[1,4,10]]

df['kwh'][[0,4,10]] = 3
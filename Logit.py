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
import statsmodels.api as sm

main_dir = "C:\Users\Matt\Documents\Nicholas School-2nd Year\Spring 2015\Big Data Analysis"
root = main_dir + "\Python\Data\\"
paths = [root + v for v in os.listdir(root) if v.startswith("08_")]

#Import Data
#header = 0 is saying that first row is header, no header would be header = null
df = pd.read_csv(paths[1], header = 0, parse_dates = [1], date_parser = np.datetime64)
df_assign = pd.read_csv(paths[0], header = 0)

##add/drop variables
df['year'] = df['date'].apply(lambda x: x.year)
df['month'] = df['date'].apply(lambda x: x.month)

# monthly aggregate
grp = df.groupby(['year', 'month', 'panid'])
df = grp['kwh'].sum().reset_index()

##Pivoting Data (Reshape)
# go from 'long' to 'wide'

#fixes the ordering of the months--For example, creates 01 for Jan which is diff from 1
df['mo_str'] = ['0' + str(v) if v < 10 else str(v) for v in df['month']]
df['kwh_ym'] = 'kwh_' + df.year.apply(str) + "_" + df.mo_str.apply(str)

# 2. pivot---long to wide data
#first thing in function is the individual identifier, in this case panid
#Second thing is the columns we want which is kwh_plus the ymd value
#Third thing is what you want at each row/column intersection, in this case kwh
df_piv = df.pivot('panid', 'kwh_ym', 'kwh')
df_piv

#clean up to make table pretty
df_piv.reset_index(inplace = True) # this makes panid its own variable
df_piv.columns.name = None #takes away column name in the first cell

# Merge Static Values (assignments, etc.)
df = pd.merge(df_assign, df_piv) #attaching order to put assignment value at the front

del df_piv, df_assign
# Generate Dummies From Qualitative Data
#pd.get_dummies() will make dummy vectors for ALL "object" or "category" types
#by default does ALL--add a list of the columns you want this to apply to
df1 = pd.get_dummies(df, columns = ['gender'] )
#because of dummy var trap, we can drop one dummy var since it is not needed
df1.drop(['gender_M'], axis = 1, inplace = True)

##Set up Data for Logit
kwh_cols = [v for v in df1.columns.values if v.startswith('kwh')]
kwh_cols = [v for v in kwh_cols if int(v[-2:]) < 4]

##Gets cols that you want to include in the regression
cols = ['gender_F'] + kwh_cols

##Set up Y, X
#y is treatment or control
y = df1['assignment']
# X is the variables that we want to use as Betas and adds constant
X = df1[cols]
X = sm.add_constant(X)

##logit--Logit is used to determine the relationships between the variables prior to running regression
#results show no relationship between the variables and the assignments
logit_model = sm.Logit(y, X)
logit_results = logit_model.fit()
print(logit_results.summary())

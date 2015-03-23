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

#IMPORT DATA----------
df = pd.read_csv(root + "07_kwh_wide.csv", header = 0)

#SIMPLE LINEAR PROBABILITY MODEL (LPM)
#lets see if consumption before a certain date determined your assignment
#making new column titled T--adds a 1 for true and 0 for false that assn = T
df['T'] = 0 + (df['assignment'] == 'T')

#breaks down subsets of data--shows values with panid 2 and assignment T
df[(df['assignment'] == 'T') & (df.panid == 2)]

##SET UP DATA
#get X matrix (left hand variables for our regression)
#df.columns.values gives the titles for each column in the labeled Dataframe
kwh_cols = [v for v in df.columns.values if v.startswith('kwh')]

##pretend trtment occurred in 2015-01-04.  we want dates before that
kwh_cols = [v for v in kwh_cols if int(v[-2:]) < 4]

#set up y and X Vars for regression
y = df['T']
X = df[kwh_cols]
X = sm.add_constant(X)

##Regression Code (OLS)
ols_model = sm.OLS(y, X) #linear probability model
#ols_model just shows that it's a model--doesn't show results
ols_results = ols_model.fit() #fit the model

print(ols_results.summary())

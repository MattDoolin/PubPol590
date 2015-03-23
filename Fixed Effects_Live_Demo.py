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
#Adds assignment T as a binary variable
df_assign.rename(columns={'assignment':'T'}, inplace = True)
"""Note: using notation from Allcott 2010"""

#Add/Drop Variables
ym = pd.DatetimeIndex(df['date']).to_period('M') #'M'=month, 'D'=day, etc.
df['ym'] = ym.values

#monthly aggregation
grp = df.groupby(['ym', 'panid'])
df = grp['kwh'].sum().reset_index()

##MERGE STATIC VARIABLES
df = pd.merge(df, df_assign)
df.reset_index(drop=True, inplace = True)

# Fixed Effects Model (demeaning)

"""demean function"""

def demean(df, cols, panid):
    """
    inputs: df (pandas dataframe), cols (list of str of column names from df),
                    panid (str of panel ids)
    output: dataframe with values in df[cols] demeaned; removes individual effects
    """

    cols = [cols] if not isinstance(cols, list) else cols
    panid = [panid] if not isinstance(panid, list) else panid
    avg = df[panid + cols].groupby(panid).aggregate(np.mean).reset_index()
    cols_dm = [v + '_dm' for v in cols]
    avg.columns = panid + cols_dm
    df_dm = pd.merge(df[panid + cols], avg)
    df_dm = DataFrame(df[cols].values - df_dm[cols_dm].values, columns=cols)
    return df_dm

#setup data for demeaning
df['log_kwh'] = df['kwh'].apply(np.log)
#seperates treatment and pretreatment time periods
df['P'] = 0 + (df['ym'] > 541)
#interaction term
df['TP'] = df['T'] * df['P']


#demean variables
cols = ['log_kwh', 'TP', 'P']
panid = 'panid'
#provides demeaned version of the data
df_dm = demean(df, cols, 'panid')

#set up regression variables
y = df_dm['log_kwh']
X = df_dm[['TP', 'P']]
X = sm.add_constant(X)
#iloc part removes the first and last columns to beat dummy trap and prevent
    #multicollinearity
mu = pd.get_dummies(df['ym'], prefix = 'ym').iloc[:, 1:-1]

#run FE model
fe_model = sm.OLS(y, pd.concat([X, mu], axis = 1))
fe_results = fe_model.fit()
print(fe_results.summary())





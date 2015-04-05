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

allocation_csv = pd.read_csv(root + "allocation_subsamp.csv", header = 0)

##Forceably creating vectors for control and all trt groups
ctrl = allocation_csv.tariff == 'E'
ctrl = allocation_csv[allocation_csv.tariff == 'E']
ctrl_vector = ctrl['ID']

trtA1 = allocation_csv[allocation_csv['tariff']== 'A']
trtA1 = trtA1[trtA1['stimulus']=='1']
trtA1_vector = trtA1['ID']

trtA3 = allocation_csv[allocation_csv['tariff']== 'A']
trtA3 = trtA3[trtA3['stimulus']=='3']
trtA3_vector = trtA3['ID']

trtB1 = allocation_csv[allocation_csv['tariff']== 'B']
trtB1 = trtB1[trtB1['stimulus']=='1']
trtB1_vector = trtB1['ID']

trtB3 = allocation_csv[allocation_csv['tariff']== 'B']
trtB3 = trtB3[trtB3['stimulus']=='3']
trtB3_vector = trtB3['ID']

##sets the seed--meaning that all answers for the class will be the same
numpy.random.seed(seed=1789)

##drawing random samples from each vector
samp_ctrl = DataFrame(np.random.choice(ctrl_vector, size = 300, replace = False))
samp_trtA1 = DataFrame(np.random.choice(trtA1_vector, size = 150, replace = False))
samp_trtA3 = DataFrame(np.random.choice(trtA3_vector, size = 150, replace = False))
samp_trtB1 = DataFrame(np.random.choice(trtB1_vector, size = 50, replace = False))
samp_trtB3 = DataFrame(np.random.choice(trtB3_vector, size = 50, replace = False))


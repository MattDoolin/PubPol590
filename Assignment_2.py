#Initialize Script
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os

main_dir = "C:\Users\Matt\Documents\Nicholas School-2nd Year\Spring 2015\Big Data Analysis"
git_dir = "C:\Users\Matt\Documents\Nicholas School-2nd Year\Spring 2015\Big Data Analysis\GitHub\PubPol590"

csv_file = "Python\Data\Missing and Duplicated Data.csv"
## Creating DataFrame
df = pd.read_csv(os.path.join(main_dir, csv_file))
df

#Converting missing values to NaN--(-) is 
missing = [".", "NA", 'NULL', '', '-']
df = pd.read_csv(os.path.join(main_dir, csv_file), na_values = missing)
#Drops any duplicated full rows
df1 = df.drop_duplicates()

empty_rows = df1['consump'].isnull()
#shows the subset of rows that have a missing consump value
df1[empty_rows]

df2 = df1[empty_rows]
df2

duplicate_date = df1.duplicated(subset = ['panid','date'])
df1[duplicate_date]
df3 = df1[duplicate_date]

df4 = df1.drop(duplicate_date)
##mean of consump variable after dropping fully duplicated rows and 
    #rows where date is duplicated and consump value is missing
df4['consump'].mean()

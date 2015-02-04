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
#Drops any duplicated FULL rows
df1 = df.drop_duplicates()

empty_rows = df1['consump'].isnull()
#shows the subset of rows that have a missing consump value
#same as below
df1[df1.consump.isnull()]
df1[empty_rows]
#Creates dataframe that is probably same as df1 since none has been dropped
df2 = df1[empty_rows]
df2

##Need to look at top to bottom and bottom to top in order to gauge where missing values are
df1[df1.duplicated(subset = ['panid', 'date'])]
df1[df1.duplicated(subset = ['panid','date'], take_last = True)]

#Creating new dataframe that drops the duplicated panid/date rows with missing consump values
df3 = df1.drop_duplicates(['panid','date'], take_last = True)
df3[df3.duplicated(['panid', 'date'])]

##mean of consump variable after dropping fully duplicated rows and 
#rows where date is duplicated and consump value is missing
df3.consump.mean()

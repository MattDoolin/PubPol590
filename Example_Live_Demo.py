# Standard Code for all scripts
from pandas import Series, DataFrame
import pandas as pd
import numpy as np

#Establishing File Paths
main_dir = "C:\Users\Matt\Documents\Nicholas School-2nd Year\Spring 2015\Big Data Analysis\Python Codes"
csv_file = "\Data\sample_data_clean.csv"
txt_file = "\Data\sample_data_clean.txt"

#Combining for full path completion
main_dir + csv_file
main_dir + txt_file

#Importing Data
#read_csv and read_table
df = pd.read_csv(main_dir + csv_file)
df2 = pd.read_table(main_dir + txt_file)

#checking object type
type(df)

#Exploring Dataframe
list(df) #quick way to get names of dataframe

##extracting data columns---These do the same thing
c = df.consump
c2 = df["consump"]

type(c)

##Boolean (Logical) Operators
#double equals (==)
c == c2
#Tests greater than
c > c2

#Other operators <, <=, >=, != (not equal to)

#Row Extraction
##row slicing
df[5:10] #df[m:n] yields frows m to n-1 Ex. this will give rows 5-9
df[0:10]
df[0:10]==df[:10]
df[10:11] #to get single row of data--gives row 10

## extracting from series--these do same thing
c[5:10]
df.consump[5:10] #would use if not assigned to c

## extraction by boolean indexing
df.panid == 4
df[df.panid == 4] #will extract subset of df where panid = 4
df[df.consump > 2]
df.panid[df.panid > 2]

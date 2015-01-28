#Initialize Script
from pandas import Series, DataFrame
import pandas as pd
import numpy as np

#Establishing File Paths
main_dir = "C:\Users\Matt\Documents\Nicholas School-2nd Year\Spring 2015\Big Data Analysis\Python Codes"
txt_file = "\Data\Assignment_1_data.txt"

df = pd.read_table(main_dir + txt_file, sep = " ") #indicating delimiter is a space
df = pd.read_table(main_dir + txt_file, sep = "/s") #does the same thing

list(df)

##Extracting Rows 60-99
df[60:100]

#Extracting rows where kwh's are greater than 30
df[df.kwh > 30] #for some reason this doesn't work for me

k = df.kwh
df[k > 30]
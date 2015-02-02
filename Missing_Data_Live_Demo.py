#Initialize Script
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os

main_dir = "C:\Users\Matt\Documents\Nicholas School-2nd Year\Spring 2015\Big Data Analysis"
git_dir = "C:\Users\Matt\Documents\Nicholas School-2nd Year\Spring 2015\Big Data Analysis\GitHub\PubPol590"

csv_file = "Python\Data\sample_missing_live_demo.csv"

# IMPORTING DATA: SETING MISSING VALUES (SENTINELS)

df = pd.read_csv(os.path.join(main_dir, csv_file))
df

df.head() #gives top 5 values
df.head(10) #head(n) gives top n rows
#slicing also works
df[:10]
df.tail(10) #tail(n) gives bottom n rows
df['consump'].head(10).apply(type) #apply function "type" to top 10 rows of consump var

## we don't want string data.  "." are common placeholders for missing data
# we need to create new missing value sentinels to adjust for this
#'na_values' to use sentinels

missing = [".", "NA", 'NULL', '']
df = pd.read_csv(os.path.join(main_dir, csv_file), na_values = missing)
#Now missing values in first 5 rows are 'NaN'
df.head(10) 
#Now type is 'float' meaning numbers
df['consump'].head(10).apply(type) 

## MISSING DATA (USING SMALLER DATAFRAME)
# quick tip: you can repeat lists by multiplying
[1,2,3]
[1,2,3]*3 #repeats list values three times

# types of missing data
None
np.nan
type(None)
type(np.nan) #type is float--missing value is considered numeric

##create a sample data set
zip1 = zip([2,4,8], [np.nan, 5, 7], [np.nan, np.nan, 22])
df1 = DataFrame(zip1, columns = ['a', 'b', 'c'])

# To see possible methods for each type of object
#type object then '.' and then Tab in main viewer

## Find missing data with Boolean Values
# search for missing data using:
df1.isnull() #pandas method to find missing data
np.isnan(df1) #numpy way--gives same result

##subset of columns
cols = ['a', 'c']
df1[cols]
df1[cols].isnull() #shows missing values for column subset

##for series--Creates boolean vector for row extraction
df1['b'].isnull()

##find non-missing values--gives opposite
df1.notnull()
df1.isnull() == df1.notnull() #perfect complements

##Filling in or Dropping Missing Values
#pandas method 'fillna'
df1.fillna(999)
df2 = df1.fillna(999)

#pandas method 'dropna'
df1.dropna() #by default this will drop entire ROW with any missing value
df1.dropna(axis = 0, how = 'any') #drop ROWS with any missing values #same as above
df1.dropna(axis = 1, how = 'any') #drop columns with any missing values
df1.dropna(axis = 0, how = 'all') #drop ROWS with all missing values # shouldn't drop anything

##try it out with object df1
df.dropna(how = 'all') #Drops tons of rows that are ENTIRELY empty

#seeing rows with missing data
df3 = df.dropna(how = 'all')
df3.head(10)
df3.isnull()
df3['consump'].isnull() #Provides Boolean Index
rows = df3['consump'].isnull()
df3[rows]


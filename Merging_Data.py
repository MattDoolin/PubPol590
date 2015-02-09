#Initialize Script
from __future__ import division
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os

main_dir = "C:\Users\Matt\Documents\Nicholas School-2nd Year\Spring 2015\Big Data Analysis"
git_dir = "C:\Users\Matt\Documents\Nicholas School-2nd Year\Spring 2015\Big Data Analysis\GitHub\PubPol590"

csv1 = "Python\Data\small_data_w_missing_duplicated.csv"
csv2 = "Python\Data\sample_assignments_merging.csv"

#IMPORT DATA
df1 = pd.read_csv(os.path.join(main_dir, csv1), na_values = ['-', 'NA'])
df2 = pd.read_csv(os.path.join(main_dir, csv2))

#CLEAN DATA
##clean df1
df1 = df1.drop_duplicates()
df1 = df1.drop_duplicates(['panid', 'date'], take_last = True)

##clean df2
df2[[0,1]]

df2 = df2[[0,1]] #reassigning df2 to a subset

# COPY DATAFRAMES
df3 = df2 #references df2--if df2 changes, df3 will change
df4 = df2.copy() #creates a copy, changes to df2 will not affect df4

#REPLACING DATA
df2.group.replace(['T', 'C'], [1,0]) #T will be replaced with a 1, C replaced with a 0 (order important) but doesn't maintain change
df2.group = df2.group.replace(['T', 'C'], [1,0]) #specifically changes group column

##df3 has changed to reflect changes to df2; df4 still contains T and C
df3
df4

#MERGING
pd.merge(df1, df2) #default 'many-to-one' merge using the intersection between the two
                    #automatically finds the keys it has in common--'panid' exists in both
#specifies what key to merge on
pd.merge(df1, df2, on = ['panid']) #chooses what columns are in both in order to merge

pd.merge(df1, df2, on = ['panid'], how = 'inner') #default state
pd.merge(df1, df2, on = ['panid'], how = 'outer') #keeps the panid (5) from df2 that is not included in df1

#df5 is now the outcome of the merge
df5 = pd.merge(df1, df2, on = ['panid'], how = 'inner')

#STACKING AND BINDING (row binds and column binds)
##'row'bind/Stacking
pd.concat([df2, df4]) #the default is to row bind
pd.concat([df2, df4], axis = 0) #same as above
pd.concat([df2, df4], axis = 0, ignore_index = True) #ignore index-True allows for rows to have different indexes (0-4,0-4 to 0-9)

#column bind--attaches second dataframe as two columns
pd.concat([df2, df4], axis = 1)



#Initialize Script
from pandas import Series, DataFrame
import pandas as pd
import numpy as np

#DUPLICATED VALUES
##create new dataframe

zip3 = zip(['red', 'green', 'blue', 'orange']*3, [5,10,20,40]*3,
        [':(', ':D', ':D']*4)
zip3
df3 = DataFrame(zip3, columns = ['A', 'B', 'C'])

##pandas method 'duplicated'
df3.duplicated() #searching from top to bottom by default
df3.duplicated(take_last = True) #searches bottom to top

## Subset duplicated values
df3.duplicated(subset = ['A', 'B'])
df3.duplicated(['A', 'B']) #same as above

##How to get all values that have duplicates (purging)
t_b = df3.duplicated() #top to bottom
b_t = df3.duplicated(take_last = True) #bottom to top
#See these compared
DataFrame([t_b, b_t])
# '~' stands for not
unique = ~(t_b | b_t) #Return true for anywhere there is at least one True in t_b or b_t
unique = ~t_b & ~b_t #Provides when both are True or both are False
unique

df3[unique] #only gives those that are never repeated
df3[b_t] #Excludes things that are unique--shows things repeated from bottom to top

##Dropping Duplicates
df3.drop_duplicates() #Returns things that are unique and were repeated but only keeping first instance of repated value
df3.drop_duplicates(take_last = True)

##below methods are the same
t_b = df3.duplicated()
df3[~t_b]

df3.drop_duplicates() == df3[~t_b]

##subset criteria
df3.drop_duplicates(['A', 'B'])

##When to use

##if you want to keep the first duplicated value (from top) and remove others
df3.drop_duplicates()

#same, but from bottom
df3.drop_duplicates(take_last = True)

##purge all values that are duplicates
t_b = df3.duplicated()
b_t = df3.duplicated(take_last = True)
unique = ~(t_b | b_t)
df3[unique]


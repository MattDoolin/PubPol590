#Initialize Script
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os

main_dir = "C:\Users\Matt\Documents\Nicholas School-2nd Year\Spring 2015\Big Data Analysis"
git_dir = "C:\Users\Matt\Documents\Nicholas School-2nd Year\Spring 2015\Big Data Analysis\GitHub\PubPol590"

csv_file = "Python\Data\sample_data_clean.csv"

# OS module

df = pd.read_csv(os.path.join(main_dir, csv_file))

## PYTHON DATA TYPES

# strings---anything surrounded in quotes
str1 = "hello, computer"
str2 = 'hello, human'
str3 = u"eep"

type(str1)
type(str2)
type(str3)

# numeric
int1 = 10
float1 = 20.56
long1 = 93939393939102984102984120498

type(int1)
type(float1)
type(long1)

# Logical
bool1 = True
notbool1 = 0
bool2 = bool(notbool1)

##Creating Lists and Tuples------------------

# in brief, lists can be changed, tuples cannot
list1 = []
list1
list2 = [1,2,3]
list2
#Gives second element but starts at 0
list2[2]
#Changing lists
list2[2] = 5 #changes second element to a 5
list2

#tuples---can't change
tup1 = (8, 3, 19)
tup1[2]
#tup1[2] = 5 #Element inside can't be changed

##convert 
list2 = list(tup1)
tup2 = tuple(list1)

##Lists can be appended and extended
list2.append([3,90]) #gives original list values plus one additional list instead of five list values

list3 = [8, 3, 90]
list3.extend([6,88]) #adds these values to list instead of adding seperate list within the list
len(list2)
#Sorts list in ascending order
list.sort(list3)
list3
len(list3)

#Converting Lists to Series and Dataframe
list4 = range(100,105) #range(n,m)--gives a list from n to m-1
list4 #output will be 5-9
list5 = range(5) #range(m)---gives list from 0 to m-1
list5 #ouput will be 0-4
list6 = ['q', 'r', 's', 't', 'u']
list6

##list to series
s1 = Series(list4)
s2 = Series(list5)
s3 = Series(list6)
s1
s2
s3
##lists to DataFrame
# only works with vectors of the same length

zip(list4, list5)
list7 = range(60,65)
zip1 = zip(list4, list5, list7)

df1 = DataFrame(zip1)

df2 = DataFrame(zip1, columns = ['two', 'apple', ':)']) #gives names to columns
df2['two'] #extracts column 'two' # quotation marks are necessary

df3 = DataFrame(zip1, columns = [2, '2', ':)'])
#shows that column names can be int or str
#calling rows
df2[1:3] #slices [n,m] n to m-1, show
df3[['2',':)']][3:4] #pulls row 3 from columns '2' and ':)' the bracket order matters here

## make dataframe using dict notation

df4 = DataFrame({':(': list4, 9:list6}) # {} makes a dictionary in python, the first item is ken
#notation {key1: item(s) in key1, key2: items in key2}
#Initialize Script
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os

main_dir = "C:\Users\Matt\Documents\Nicholas School-2nd Year\Spring 2015\Big Data Analysis\Python\Data"
git_dir = "C:\Users\Matt\Documents\Nicholas School-2nd Year\Spring 2015\Big Data Analysis\GitHub\PubPol590"

csv_file = "\Python\Data\sample_data_clean.csv"

# OS module

df = pd.read_csv(os.path.join(main_dir, csv_file))

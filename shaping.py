import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 

import matplotlib.lines as mlines
import matplotlib.transforms as mtransforms

columns = 'columns'
df1_mode =  lambda x:x.value_counts().index[0]

# ---- READING JSON FILE ---- # 
#  Users/bexa/Documents/Compsci/Advanced Programming/Summative/facilities.json

# ask user for json file location
enter_json = input ('Please enter the file location of your cleaned JSON file:')
# read as pandas dataframe
df1 = pd.read_json(enter_json)


# ---- EXPORT AS JSON ---- #

def export_json(file, type):
    try:
        file_name = input("Please enter a file name you'd like to use:")
        new_json_name = file_name + ".json"
        file.to_json(new_json_name, index='true', orient=type) 

    except NameError:
        print("You have not loaded or cleaned your files to export yet!")

    


# ---- SEATING MEAN, MEDIAN, MODE SCORE ----- #

# making grouped by activity date first, then seating
grouped = df1.groupby(['ACTIVITY DATE', 'SEATING'])


# make activity date by YEAR 
# using score to calculate
group_df1 = grouped['SCORE']


# Calculating Mode by using value counts then finding the first value in row

# calculating mean, median 
df1_mean = group_df1.agg([('MEAN', 'mean'), ('MEDIAN','median'), ('MODE', df1_mode)])

# turn mean/median/mode groupby table into DataFrame 
df1_1 = pd.DataFrame(df1_mean)

print(df1_1)



# ---- ZIP CODES MEAN, MEDIAN, MODE SCORE ----- #


# making grouped by activity date first, then seating
grouped = df1.groupby(['ACTIVITY DATE', 'ZIP CODES'])

# using score to calculate
group_df2 = grouped['SCORE']

# Calculating Mode by using value counts then finding the first value in row

# calculating mean, median 
df2_mean = group_df2.agg([('MEAN', 'mean'), ('MEDIAN','median'), ('MODE', df1_mode)])

# turn mean/median/mode groupby table into DataFrame 
df2_1 = pd.DataFrame(df2_mean)

print(df2_1)

# ----TEST / CHECKS ----- #

# print("VIOLATION MERGE: ", df6_merge.loc[df6_merge['VIOLATION CODE'] == 'F001'])
# print("VIOLATION CODE: ", df6_merge.loc[df6_merge['FACILITY ID'] == 'FA0170678'])
# print("FACILITY FA0019271: ", df5_cleaned.loc[df5_cleaned['FACILITY ID'] == 'FA0019271'])
# print("FACILITY df3 FA0019271: ", df3.loc[df3['FACILITY ID'] == 'FA0019271'])


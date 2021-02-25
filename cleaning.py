import pandas as pd
import numpy as np

columns = 'columns'

# ----- IMPORT CSV FILES ---- #

print("Hello welcome to the data cleaning tool. Please upload your files:")
inventory_file = input("Please enter the full file location for the inventory file:")
violation_file = input("Please enter the full file location for the violation file:")
inspection_file = input("Please enter the full file location for the inspection file:")

# /Users/bexa/Documents/Compsci/Advanced Programming/Summative/DataSet1/inventroy.csv
# /Users/bexa/Documents/Compsci/Advanced Programming/Summative/DataSet1/violations.csv
# /Users/bexa/Documents/Compsci/Advanced Programming/Summative/DataSet1/Inspections.csv

# missing values
missing_values = ["NA", "N/A", "na", r"^\s*$", "", " ", "NaN"]

inventory = pd.read_csv(inventory_file, keep_default_na=False, na_values=missing_values)
violation = pd.read_csv(violation_file, keep_default_na=False, na_values=missing_values)
inspection = pd.read_csv(inspection_file, keep_default_na=False, na_values=missing_values)

# ---- CLEAN FILE ---- #

def clean(df):

    # Dropping data with over 50% null to avoid errors 
    print("...10% Dropping empty cells")
    df.dropna(inplace = True) 

    # Replace NaN, missing values etc with 0
    df.fillna(0)
    print("...20% Neatening missing values")

    print("...30% Stripping spaces")
    # Regex finds spaces 2 or more & changes to 1 and strips space before/after 
    df.columns = [col.strip().replace('  ', ' ') for col in df.columns]

    print("...40% Converting all to uppercase")
    df.columns = [x.upper() for x in df.columns]
    # print(csv_df.columns) to check if it works :)


    if "PE DESCRIPTION" in df:
        print("...60% Slicing out & cleaning seating column")

        # Seating numbers only
        new_seat_col = df['PE DESCRIPTION'].str.extract('.*\((.*)\).*') # print(new_seat_col)

        # Remove seating numbers leave behind rest
        df['PE DESCRIPTION'] = df['PE DESCRIPTION'].str.replace(r" \(.*\)","") # print(pe_list)

        # New headers
        df['SEATING'] = new_seat_col

        # Remove Alpha, Commas, Full stop and Spacing

        df['SEATING'] = df['SEATING'].str.replace('[a-zA-Z,. ]', '')

        
    if "SCORE" in df:
        print("...70% Converting to correct data types")
        df["SCORE"] = df["SCORE"].apply(np.int64) 

    if "ZIP CODES" in df:
        print("...80% Cleaning last bits")
        df["ZIP CODES"] = df["ZIP CODES"].apply(np.int64) 
        # int_df = df["ZIP CODES"].astype(int)

    if "ACTIVITY DATE" in df:
        print("...90% Formatting dates")
        df['ACTIVITY DATE'] =  pd.to_datetime(df['ACTIVITY DATE'], format='%m/%d/%Y')


    print("...100% Done!")
    
    print(df.head(5))

    # print(df.head(5))

    return df


def second_clean(df):
    
    print("...Implementing a second clean")

    
    if "PROGRAM STATUS" in df:
        print("...30% Removing inactive accounts")
        df = df[df['PROGRAM STATUS'] != 'INACTIVE']


    if "ACTIVITY DATE" in df:
        print("...60% Formatting dates")
        df['ACTIVITY DATE'] =  pd.to_datetime(df['ACTIVITY DATE'], format='%m/%d/%Y')

        # this returns only the year
        df['ACTIVITY DATE'] = df['ACTIVITY DATE'].dt.year

    if "SERIAL NUMBER" and "FACILITY ID" in df:
        print("...90% Drop duplicates")
        df = df.drop_duplicates(subset=['ACTIVITY DATE', 'FACILITY ID', 'SERIAL NUMBER'], keep='last')
        
    print(".. 100% Second clean done!")

    return df


# ---- EXPORT AS JSON ---- #

def export_json(file, type):
    try:
        file_name = input("Please enter a file name you'd like to use:")
        new_json_name = file_name + ".json"
        file.to_json(new_json_name, index='true', orient=type) 

    except NameError:
        print("You have not loaded or cleaned your files to export yet!")

    


# ---- LETS GO!!! CLEAN DATAFRAMES ----- #


df1 = clean(inventory)
df2 = clean(violation)
df3 = clean(inspection)


# ---- HEADER NAMES ----- #

# Inventory
inventory_headers = ["FACILITY ID", "ZIP CODES"]
# Violation
violation_headers = ['SERIAL NUMBER', 'VIOLATION CODE']
# Inspection 
inspection_headers = ["ACTIVITY DATE", "FACILITY ID", "SERIAL NUMBER", "PROGRAM STATUS", "SCORE", "SEATING", "PE DESCRIPTION"]


# ---- NEW HEADERS ----- #

df1_1 = pd.DataFrame(df1, columns=inventory_headers)
# print(df1_1.dtypes)


df2_1 = pd.DataFrame(df2, columns=violation_headers)
# print(df2_1.dtypes)

df3_1 = pd.DataFrame(df3, columns=inspection_headers)
# print(df3_1.dtypes)

# print(df1_1.head(10), df2_1.head(10), df3_1.head(10))


# ----MERGE INTO 1 FILE  ----- #

# merge. common columns = facility id for ZIP CODES
df4_merge = pd.merge(df3_1,df1_1, how='inner', on='FACILITY ID')
# merge columns so serial number becomes the violation code 
df4_merge2 = pd.merge(df4_merge,df2_1, how='inner', on='SERIAL NUMBER')


# print("SERIAL df4_merge2: ", df4_merge.loc[df4_merge['SERIAL NUMBER'] == 'DA2FXQNN6'])
# df4_merge2 = df4_merge2.pop('SERIAL NUMBER')

# second clean
df4_cleaned = second_clean(df4_merge2)
df4_cleaned = df4_cleaned.reset_index(drop=True)

print("Top 100 of final clean\n", df4_cleaned.head(50))

# remove duplicates
# df4_cleaned = df4_cleaned.drop_duplicates(subset=['FACILITY ID'], keep='last')


# ----EXPORT TO JSON  ----- #

export_json(df4_cleaned, columns)

print("Congratulations, your data has been clean and exported into the same folder")




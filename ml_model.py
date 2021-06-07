import pandas as pd
#from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.model_selection import train_test_split
#import numpy as np

def predict(list_price,bedroom,washroom,additional,kitchens,style,housetype,fam,contractdate,garage):

       # Importing the data from SQLite database into a DataFrame
       house_df = pd.read_sql_table('sold_homes', 'sqlite:///sold_homes.db').drop(columns=['index'])

       # Drop the non-beneficial columns
       house_df = house_df.drop(["#","LSC","EC","St#","Dir","Municipality","Community","MLS#","Abbr","List Brokerage","Co op Brokerage","Street Name","Heat","A/C","Sold Date"],1)

       # Converting "List Price" and "Sold Price" to integer type
       house_df["List Price"] = house_df["List Price"].replace('[\$,]', '', regex=True).astype(int)
       house_df["Sold Price"] = house_df["Sold Price"].replace('[\$,]', '', regex=True).astype(int)

       # Converting the 'Contract Date' and 'Sold Date' to interger type
       house_df['Contract Date'] = house_df['Contract Date'].replace('[\/]', '', regex=True).astype(int) 
       # house_df['Sold Date'] = house_df['Sold Date'].replace('[\/]', '', regex=True).astype(int)

       # Determine the number of unique values in each column with object datatype
       house_cat = house_df.dtypes[house_df.dtypes == "object"].index.tolist()

       # Create a OneHotEncoder instance
       enc = OneHotEncoder(sparse=False)

       # Fit and transform the OneHotEncoder using the categorical variable list
       encode_df = pd.DataFrame(enc.fit_transform(house_df[house_cat]))

       # Add the encoded variable names to the dataframe
       encode_df.columns = enc.get_feature_names(house_cat)

       # Merge one-hot encoded features and drop the originals
       house_df = house_df.merge(encode_df,left_index=True, right_index=True)
       house_df = house_df.drop(house_cat,1)

       # Split our preprocessed data into our features and target arrays
       y = house_df["Sold Price"].values
       X = house_df.drop(columns=["Sold Price"]).values

       # Split the preprocessed data into a training and testing dataset
       X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1,train_size=0.9, random_state=5)

       # Created the model and fitted the data in the model
       model = LinearRegression()
       model.fit(X_train, y_train)

       # The model creates predicted y values based on X values from test dataset
       y_pred = model.predict(X_test)

       #Converting inputs to integer type
       list_price = int(list_price) 
       bedroom = int(bedroom) 
       washroom = int(washroom)
       additional = int(additional) 
       kitchens = int(kitchens) 
       
       t = (list_price, bedroom, additional, washroom, kitchens, contractdate)

       # Creating dataframe 
       new_df = pd.DataFrame(t)
       new_df1 = new_df.T
       new_df1.columns=['List Price', 'Br', 'Additional', 'Wr', 'Kit', 'Contract Date']

       new_df1["List Price"] = new_df1["List Price"].replace('[\$,]', '', regex=True).astype(int)
       #new_df1["Sold Price"] = new_df1["Sold Price"].replace('[\$,]', '', regex=True).astype(int)
       new_df1['Contract Date'] = new_df1['Contract Date'].replace('[\/]', '', regex=True).astype(int) 
       #new_df1['Sold Date'] = new_df1['Sold Date'].replace('[\/]', '', regex=True).astype(int)
       new_df1['Br'] = new_df1['Br'].astype(int)
       new_df1['Wr'] = new_df1['Wr'].astype(int)
       new_df1['Kit'] = new_df1['Kit'].astype(int)
       new_df1['Additional'] = new_df1['Additional'].astype(int)

       new_df1["Type_Semi-Detac"] = 0
       new_df1["Type_Att/Row/Tw"] = 0
       new_df1["Type_Detached"] = 0
       new_df1["Type_Vacant Lan"] = 0
       new_df1["Type_Link"] = 0

       new_df1["Style_1 1/2 Stor"] = 0
       new_df1["Style_2-Storey"] = 0
       new_df1["Style_2 1/2 Stor"] = 0
       new_df1["Style_3-Storey"] = 0
       new_df1["Style_Backsplit"] = 0
       new_df1["Style_Bungalow"] = 0
       new_df1["Style_Bungaloft"] = 0
       new_df1["Style_Bungalow-R"] = 0
       new_df1["Style_Sidesplit"] = 0
       new_df1["Style_Other"] = 0

       new_df1["Fam_Y"] = 0
       new_df1["Fam_N"] = 0
       new_df1["Garage Type_Attach"] = 0
       new_df1["Garage Type_Built-"] = 0
       new_df1["Garage Type_Carpor"] = 0
       new_df1["Garage Type_Detach"] = 0
       new_df1["Garage Type_None"] = 0
       new_df1["Garage Type_Other"] = 0

       style_comb = "Style_" + style
       new_df1[style_comb] = 1

       type_comb = "Type_" + housetype
       new_df1[type_comb] = 1

       fam_comb = "Type_" + fam
       new_df1[fam_comb] = 1

       garage_comb = "Type_" + garage
       new_df1[garage_comb] = 1

       new_df1 = new_df1[['List Price', 'Br', 'Additional', 'Wr', 'Kit', 'Contract Date', 'Type_Att/Row/Tw', 'Type_Detached', 'Type_Link',
              'Type_Semi-Detac', 'Type_Vacant Lan', 'Style_1 1/2 Stor',
              'Style_2 1/2 Stor', 'Style_2-Storey', 'Style_3-Storey',
              'Style_Backsplit', 'Style_Bungaloft', 'Style_Bungalow',
              'Style_Bungalow-R', 'Style_Other', 'Style_Sidesplit', 'Fam_N', 'Fam_Y',
              'Garage Type_Attach', 'Garage Type_Built-', 'Garage Type_Carpor',
              'Garage Type_Detach', 'Garage Type_None', 'Garage Type_Other']]

       house_cat = new_df1.dtypes[new_df1.dtypes == "object"].index.tolist()

       # Create a OneHotEncoder instance
       enc = OneHotEncoder(sparse=False)

       # Fit and transform the OneHotEncoder using the categorical variable list
       encode_df = pd.DataFrame(enc.fit_transform(new_df1[house_cat]))

       # Add the encoded variable names to the dataframe
       encode_df.columns = enc.get_feature_names(house_cat)

       # Merge one-hot encoded features and drop the originals
       new_df1 = new_df1.merge(encode_df,left_index=True, right_index=True)
       new_df1 = new_df1.drop(house_cat,1)

       new_df2 = new_df1.values

       sold_price = model.predict(new_df2)
       soldprice = float("{:.2f}".format(sold_price[0]))
       difference = float("{:.2f}".format(soldprice - new_df2[0,0]))

       return soldprice, difference

       

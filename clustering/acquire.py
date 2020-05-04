import pandas as pd
import numpy as np
import env

def get_db_url(database):
    from env import host, user, password
    url = f'mysql+pymysql://{user}:{password}@{host}/{database}'
    return url

def get_zillow_data():
    query = """
    SELECT * FROM properties_2017
    RIGHT JOIN `predictions_2017` USING (`parcelid`)
    LEFT JOIN `architecturalstyletype` USING (`architecturalstyletypeid`) 
    LEFT JOIN `buildingclasstype` USING (`buildingclasstypeid`)
    LEFT JOIN `heatingorsystemtype` USING (`heatingorsystemtypeid`)
    LEFT JOIN `propertylandusetype` USING (`propertylandusetypeid`)
    LEFT JOIN `storytype` USING (`storytypeid`)
    LEFT JOIN `airconditioningtype` USING (`airconditioningtypeid`)
    LEFT JOIN `typeconstructiontype` USING (`typeconstructiontypeid`) 
    WHERE properties_2017.latitude IS NOT NULL OR  properties_2017.longitude IS NOT NULL
    """
    df = pd.read_sql(query, get_db_url('zillow'))
    # Drop one of the duplicate column named id
    df = pd.concat([
    df.iloc[:, :11], # all the rows, and up to, but not including the index of the column to drop
    df.iloc[:, 11 + 1:] # all the rows, and everything after the column to drop
    ], axis=1)
    #sort values by parcelid and transactiondate
    df = df.sort_values(["parcelid", "transactiondate"])

    # drop duplicates
    df = df.drop_duplicates(subset=["parcelid"],keep='last')
    return df

def rows_missing(df):
    df1 = pd.DataFrame(df.isnull().sum(), columns = ['num_rows_missing'])
    df1['pct_rows_missing'] = df1.num_rows_missing/df.shape[0]
    return df1  

def cols_missing(df):
    """function that takes in a dataframe of observations and attributes and returns a dataframe where each row is
    an atttribute name, the first column is the number of rows with missing values for that attribute, 
    and the second column is percent of total rows that have missing values for that attribute"""
    df['total'] = df.apply(lambda row: row.isnull().sum(), axis =1)
    df2 = df[['total']]
    df2 = df2.reset_index()
    df2 = df2.groupby('total').count()
    df2= df2.reset_index()
    df2.rename(columns = {'total': 'num_cols_missing', 'index': 'num_rows'}, inplace = True)
    df2['pct_cols_missing'] = df2.num_cols_missing/df.shape[1]
    return df2
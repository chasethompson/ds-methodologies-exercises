import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np 
from env import host, user, password

# function to contact database

def get_db_url(db_name):
    return f"mysql+pymysql://{user}:{password}@{host}/{db_name}"

# function to query db and return df

def wrangle_zillow():
    url = get_db_url('zillow')
    query = '''
    SELECT prop.*, 
       pred1.logerror, 
       pred1.transactiondate, 
       air.airconditioningdesc, 
       arch.architecturalstyledesc, 
       build.buildingclassdesc, 
       heat.heatingorsystemdesc, 
       landuse.propertylandusedesc, 
       story.storydesc, 
       construct.typeconstructiondesc 
FROM   properties_2017 prop 
       LEFT JOIN predictions_2017 pred1 USING (parcelid) 
       INNER JOIN (SELECT parcelid, 
                          Max(transactiondate) maxtransactiondate 
                   FROM   predictions_2017 
                   GROUP  BY parcelid) pred2 
               ON pred1.parcelid = pred2.parcelid 
                  AND pred1.transactiondate = pred2.maxtransactiondate 
       LEFT JOIN airconditioningtype air USING (airconditioningtypeid) 
       LEFT JOIN architecturalstyletype arch USING (architecturalstyletypeid) 
       LEFT JOIN buildingclasstype build USING (buildingclasstypeid) 
       LEFT JOIN heatingorsystemtype heat USING (heatingorsystemtypeid) 
       LEFT JOIN propertylandusetype landuse USING (propertylandusetypeid) 
       LEFT JOIN storytype story USING (storytypeid) 
       LEFT JOIN typeconstructiontype construct USING (typeconstructiontypeid) 
WHERE  prop.latitude IS NOT NULL 
	   AND prop.longitude IS NOT NULL; 
    '''

    zillow = pd.read_sql(query,url)
    return zillow

def measure_na_columns(df):
    na_column_df = pd.DataFrame(df.isna().sum(), columns=['num_na_rows'])
    na_column_df['pct_na_rows'] = df.isna().sum() / len(df.index)
    return na_column_df

def measure_na_rows(df):
    na_row_df = pd.DataFrame(df.isna().sum(axis=1).value_counts(sort=False), 
                      columns=['num_rows'])
    na_row_df = na_row_df.reset_index()
    na_row_df = na_row_df.rename(columns={'index': 'num_col_missing'})
    na_row_df['pct_cols_missing'] = na_row_df.num_col_missing / len(df.columns.tolist())
    return na_row_df

def handle_missing_values(df, prop_required_column = .5, prop_required_row = .75):
    threshold = int(round(prop_required_column*len(df.index),0))
    df.dropna(axis=1, thresh=threshold, inplace=True)
    threshold = int(round(prop_required_row*len(df.columns),0))
    df.dropna(axis=0, thresh=threshold, inplace=True)
    return df

def remove_columns(df, cols_to_remove):  
    df = df.drop(columns=cols_to_remove)
    return df

def label_county(row):
    if row['fips'] == 6037:
        return 'Los Angeles'
    elif row['fips'] == 6059:
        return 'Orange'
    elif row['fips'] == 6111:
        return 'Ventura'

def prep_zillow(cols_to_remove=['calculatedbathnbr', 'heatingorsystemtypeid', 'regionidneighborhood'], prop_required_column=.5, prop_required_row=.75):
    zillow = wrangle_zillow()
    
    #insure that this is a single unit property
    zillow = zillow[zillow.propertylandusetypeid
                             .isin([261, 262, 263, 264, 266, 268, 273, 276, 279])
                            ]
    zillow = zillow[(zillow.bedroomcnt > 0) & (zillow.bathroomcnt > 0)]
    zillow = remove_columns(zillow, cols_to_remove)
    zillow = handle_missing_values(zillow, prop_required_column, prop_required_row)
    
    # Set nulls to specific value
    zillow.calculatedfinishedsquarefeet[zillow.calculatedfinishedsquarefeet.isna()] = zillow.calculatedfinishedsquarefeet.median()
    
    zillow.buildingqualitytypeid = zillow.buildingqualitytypeid.fillna(6)
    zillow.finishedsquarefeet12 = zillow.finishedsquarefeet12.fillna(1456.0)
    
    zillow.lotsizesquarefeet = zillow.lotsizesquarefeet.fillna(zillow.lotsizesquarefeet.median())
    
    zillow = zillow.dropna(subset=['regionidcity', 'regionidzip', 'censustractandblock'])
    
    zillow.propertyzoningdesc = zillow.propertyzoningdesc.fillna('LAR1')
    
    zillow.heatingorsystemdesc = zillow.propertyzoningdesc.fillna('N/A')
    
    zillow.structuretaxvaluedollarcnt = zillow.structuretaxvaluedollarcnt.fillna(zillow.structuretaxvaluedollarcnt.median())
    
    zillow.yearbuilt = zillow.yearbuilt.fillna(zillow.yearbuilt.median())
    
    zillow.taxamount = zillow.taxamount.fillna(zillow.taxamount.median())
    
    zillow.unitcnt = zillow.unitcnt.fillna(1.0)
    
    zillow['County'] = zillow.apply(lambda row: label_county(row), axis=1)

    zillow['State'] = 'CA'
    
    zillow = zillow.dropna(axis=1)
    
    return zillow
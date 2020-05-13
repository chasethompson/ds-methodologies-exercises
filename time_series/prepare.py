import pandas as pd
import numpy as np
import requests
import os.path
import acquire

# ~~~~~ Prepare Data ~~~~~ #

# ----------------- #
#  PREP STORE DATA  #
# ----------------- #

def prepare_sale():
    df = acquire.get_store_data()
    df['month'] = df.index.month
    df['weekday'] = df.index.day_name()
    df['total_sales'] = df.sale_amount * df.item_price
    df = (df.astype({'sale_id': object, 
                     'store_id': object, 
                     'store_zipcode': object, 
                     'item_id': object, 
                     'item_upc12': object, 
                     'item_upc14': object, 
                     'month': 'category', 
                     'weekday': 'category'}))
    sales_sum = df.resample("D")[['total_sales']].sum()
    sales_sum['sales_differences'] = sales_sum['total_sales'].diff()
    return df, sales_sum

# ----------------- #
#  PREP ENERGY DATA #
# ----------------- #

def prepped_energy():
    """
    Function the acquires and returns 
    a prepared df for the OPS German Energy data
    and displays historgrams for numeric columns
    """
    # Acquire Datetime df
    gdf = german_energy_csv()
    
    # Create new date part columns as category dtypes
    gdf['month'] = gdf.index.month.astype('category')
    gdf['year'] = gdf.index.year.astype('category')
    
    return gdf
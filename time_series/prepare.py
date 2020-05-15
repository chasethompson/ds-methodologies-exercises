import pandas as pd
import numpy as np
import requests
import os.path
import acquire
import matplotlib.pyplot as plt


# ~~~~~ Prepare Data ~~~~~ #


#-----------#
#  Helpers  #
#-----------#

def set_datetime_index(df, col):
    df[col] = pd.to_datetime(df[col], format='%a, %d %b %Y %H:%M:%S %Z')
    df = df.sort_values(col).set_index(col)
    return df

def make_year_col(df):
    df['year'] = df.index.year
    return df

def make_month_col(df):
    df['month'] = df.index.month
    return df

def make_day_col(df):
    df['day_of_week'] = df.index.day_name()
    return df

def make_sales_total_col(df):
    df['sales_total'] = df.sale_amount * df.item_price
    return df

def make_sales_diff_col(df):
    df['day_sales_diff'] = df.sale_amount.diff(1)
    return df

#--------------#
#  Sales Data  #
#--------------#

#def prep_store_data():
    df = acquire.get_store_data()
    # prep df per instructions: set sale_date as datetime column, make it the index, make new month col based on the sale_date index, make new day col based on sale_date index
    df = set_datetime_index(df, 'sale_date')    
    df = make_month_col(df)
    df = make_day_col(df)
    # create a new column derived from sale_amount (total items) and item_price
    df = make_sales_total_col(df)
    # create a new column that is the result of the current sales - the previous days sales
    df = make_sales_diff_col(df)
    # write modified df to new csv file
    df.to_csv('prepped_store_data.csv')
    return df

#---------------------#
#  German Power Data  #
#---------------------#

def prep_ops_data():
    df = acquire.read_german()
    # prep df per instructions: set Date as datetime column, make it the index, make new month col based on the Date index, make new year col based on Date index
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').set_index('Date')   
    df = make_month_col(df)
    df = make_year_col(df)
    # write modified df to new csv file
    df.to_csv('prepped_ops_data.csv')
    return df

#------------------#
#  Visualizations  #
#------------------#

def hist_plot(df, col, bins):
    """
    function takes in a DataFrame, 
    a string for column name or list, and 
    integer for number of bins and
    displays a histogram of the column
    """
    plt.hist(df[col], bins=bins, color='thistle')
    plt.title('Distribution of ' + col)
    plt.xlabel('')
    plt.ylabel('Count')
    plt.show()
    
def numeric_hists(df, bins=20):
    """
    Function to take in a DataFrame, bins default 20,
    select only numeric dtypes, and
    display histograms for each numeric column
    """
    num_df = df.select_dtypes(include=np.number)
    num_df.hist(bins=bins, color='thistle')
    plt.suptitle('Numeric Column Distributions')
    plt.show()

#-------------------------#
#  Class Prophet Prepare  #
#-------------------------#

def remove_columns(df, cols_to_remove):
    df = df.drop(columns=cols_to_remove)
    return df

def handle_missing_values(df, prop_required_column = .5, prop_required_row = .75):
    threshold = int(round(prop_required_column*len(df.index),0))
    df.dropna(axis=1, thresh=threshold, inplace=True)
    threshold = int(round(prop_required_row*len(df.columns),0))
    df.dropna(axis=0, thresh=threshold, inplace=True)
    return df

def prep_store_data_prophet(df: pd.DataFrame) -> pd.DataFrame:
    return (df.assign(ds=pd.to_datetime(df.sale_date)).sort_values('ds')
            .assign(y=df.sale_amount * df.item_price)\
            .groupby(['ds'])['y'].sum().reset_index().set_index('ds'))

def prep_store_data(df):
    # parse the date column and set it as the index
    # fmt = '%a, %d %b %Y %H:%M:%S %Z'
    # df.sale_date = pd.to_datetime(df.sale_date, format=fmt)
    df.sale_date = pd.to_datetime(df.sale_date)
    df = df.sort_values(by='sale_date').set_index('sale_date')

    # add some time components as features
    # df['month'] = df.index.strftime('%m-%b')
    # df['weekday'] = df.index.strftime('%w-%a')

    # derive the total sales
    df['sales_total'] = df.sale_amount * df.item_price
    
    return df

def get_sales_by_day(df):
    sales_by_day = df.resample('D')[['sales_total']].sum()
    sales_by_day['diff_with_last_day'] = sales_by_day.sales_total.diff()
    return sales_by_day
    
def split_store_data(df, train_prop=.66): 
    train_size = int(len(df) * train_prop)
    train, test = df[0:train_size].reset_index(), df[train_size:len(df)].reset_index()
    return train, test
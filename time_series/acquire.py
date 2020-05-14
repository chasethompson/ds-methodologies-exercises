import pandas as pd
import numpy as np
import requests
import os.path

# ~~~~~ Acquire Sales Data ~~~~~ #

# ----------------- #
#  GET STORE DATA   #
# ----------------- #

def get_stores():
    '''
    Reads values direct from stores pages on https://python.zach.lol/api/v1 and saves csv file with new data,
    basically making a mini-db 
    args:
    None
    Returns:
    None
    '''
    url = 'https://python.zach.lol/api/v1/stores'
    response = requests.get(url)
    page = response.json()['payload']
    stores = []
    while True:
        stores += page['stores']
        if page['next_page'] == None:
            break
        page_url = url + page['next_page']
        page = requests.get(page_url).json()['payload']
    stores_df = pd.DataFrame(stores)
    stores_df.to_csv('stores.csv', index= False)

def get_store_df():
    if os.path.isfile('stores.csv'):
        store_df = pd.read_csv('stores.csv')
    else:
        get_stores()
        store_df = pd.read_csv('stores.csv')
    return store_df


# ----------------- #
#  GET ITEM DATA    #
# ----------------- #

def get_items():
    '''
    Read values from items pages on https://python.zach.lol/api/v1 and writes a csv file, making
    a mini-db of for items
    args: None
    Returns: None
    '''
    base_url = 'https://python.zach.lol'
    api_url = base_url + '/api/v1/items'
    response = requests.get(api_url)
    page = response.json()['payload']
    items = []
    while True:
        items += page['items']
        if page['next_page'] == None:
            break
        page_url = base_url + page['next_page']
        response = requests.get(page_url)
        page = response.json()['payload']
    items_df = pd.DataFrame(items)
    items_df.to_csv('items.csv', index= False)

def get_item_df():
    if os.path.isfile('items.csv'):
        item_df = pd.read_csv('items.csv')
    else:
        get_items()
        item_df = pd.read_csv('items.csv')
    return item_df


# ----------------- #
#  GET SALES DATA   #
# ----------------- #

def get_sales():
    '''
    Read values from sales pages on https://python.zach.lol/api/v1 and creates a csv file, basically
    a mini-db.
    arg: None
    Returns: None
    '''
    base_url = 'https://python.zach.lol'
    api_url = base_url + '/api/v1/sales'
    response = requests.get(api_url)
    page = response.json()['payload']

    page['next_page'] # url extension for the next page
    sales = []

    while True:
        sales += page['sales']
        if page['next_page'] == None:
            break
        page_url = base_url + page['next_page']
        response = requests.get(page_url)
        page = response.json()['payload']
    sales_df = pd.DataFrame(sales)
    sales_df.to_csv('sales.csv', index = False)

def get_sales_df():
    if os.path.isfile('sales.csv'):
        sales_df = pd.read_csv('sales.csv')
    else:
        get_sales()
        sales_df = pd.read_csv('sales.csv')
    return sales_df

# ~~~~~ Get Full Sales DataFrame ~~~~~ #

def get_all_sales_data():
    '''
    This functions reads all the csvs for items, sales, and stores, then merges them into a single 
    dataframe.
    args: None
    returns: DataFrame
    '''

    stores = get_store_df()
    items = get_item_df()
    sales = get_sales_df()

    sales.rename(columns={'store' : 'store_id', 'item' : 'item_id'}, inplace = True)
    df = sales.merge(stores.set_index('store_id'), on = 'store_id')
    df = df.merge(items.set_index('item_id'), on = 'item_id')

    return df

# ------------------- #
# German Energy Data  #
# ------------------- #

def german_energy_csv():
    """
    This function returns a df with a datetime index
    using the opsd_germany url/csv.
    """
    if os.path.isfile('german_energy.csv'):
        df = pd.read_csv('german_energy.csv', parse_dates=True, index_col='Date').sort_index()
    else:
        url = 'https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv'
        df = pd.read_csv(url, parse_dates=True, index_col="Date").sort_index()
        df.to_csv('german_energy.csv')
    return df

# ---------------------- #
# Faith Acquire Strategy #
# ---------------------- #

def get_df(name):
    """
    This function takes in the string
    'items', 'stores', or 'sales' and
    returns a df containing all pages and
    creates a .csv file for future use.
    """
    base_url = 'https://python.zach.lol'
    api_url = base_url + '/api/v1/'
    response = requests.get(api_url + name)
    data = response.json()
    
    # create list from 1st page
    my_list = data['payload'][name]
    
    # loop through the pages and add to list
    while data['payload']['next_page'] != None:
        response = requests.get(base_url + data['payload']['next_page'])
        data = response.json()
        my_list.extend(data['payload'][name])
    
    # Create DataFrame from list
    df = pd.DataFrame(my_list)
    
    # Write DataFrame to csv file for future use
    df.to_csv(name + '.csv')
    return df

def get_store_data():
    '''
    This functions checks for the csv file for items, sales, and stores - if there isn't one, it creates the csv. After finding or creating the csv, it merges the csvs into a single dataframe, then creates that into its own csv.

    Once that dataframe is made converts sale_date to a date, then sets the index with that date. Finally, it returns a dataframe.

    args: None
    returns: dataframe
    '''
    
    # check for csv files or create them
    if os.path.isfile('items.csv'):
        items_df = pd.read_csv('items.csv', index_col=0)
    else:
        items_df = get_df('items')
        
    if os.path.isfile('stores.csv'):
        stores_df = pd.read_csv('stores.csv', index_col=0)
    else:
        stores_df = get_df('stores')
        
    if os.path.isfile('sales.csv'):
        sales_df = pd.read_csv('sales.csv', index_col=0)
    else:
        sales_df = get_df('sales')
        
    if os.path.isfile('big_df.csv'):
        df = pd.read_csv('big_df.csv', parse_dates=True, index_col='sale_date')
        df = df.drop(columns=['Unnamed: 0'])
        return df
    else:
        # merge all of the DataFrames into one
        df = pd.merge(sales_df, stores_df, left_on='store', right_on='store_id').drop(columns={'store'})
        df = pd.merge(df, items_df, left_on='item', right_on='item_id').drop(columns={'item'})

        # convert sale_date to DateTime Index
        df['sale_date'] = pd.to_datetime(df.sale_date)
        df = df.set_index('sale_date').sort_index()

        # write merged DateTime df with all data to directory for future use
        df.to_csv('big_df.csv')
        return df


# ---------------------- #
#   Acquire Energy Data  #
# ---------------------- #


# def german_energy_csv():
#     """
#     This function returns a df with a datetime index
#     using the opsd_germany url/csv.
#     """
#     if os.path.isfile('german_energy.csv'):
#         df = pd.read_csv('german_energy.csv', parse_dates=True, index_col=0)
#     else:
#         url = 'https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv'
#         df = pd.read_csv(url, parse_dates=True).set_index('Date').sort_index()
#         df.to_csv('german_energy.csv')
#     return df
import pandas as pd
import numpy as np
import requests

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
    def refresh_items():
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


    #iterates through pages till the last page and appends sales inforation, breaks when 'next_page' == None 
    while True:
        sales += page['sales']
        if page['next_page'] == None:
            break
        page_url = base_url + page['next_page']
        response = requests.get(page_url)
        page = response.json()['payload']
    sales_df = pd.DataFrame(sales)

    sales_df.to_csv('sales.csv', index=False)

def get_sales_df():
    sales_df = pd.read_csv('sales.csv')
    return sales_df


# ~~~~~ Get Full Sales DataFrame ~~~~~ #

def get_all_sales_data():
    '''
    This functions reads all the csvs for items, sales, and stores, then merges them into a single 
    dataframe.
    args: 
    reads sales, items, and stores csv files and joins information into one data frame
    args:
    refresh: if True, will pull current data from the original source, else will read from local csv files
    returns:
    dataframe
    '''

    stores = get_store_df()
    items = get_item_df()
    sales = get_sales_df()

    sales.rename(columns={'store' : 'store_id', 'item' : 'item_id'}, inplace = True)
    df = sales.merge(stores.set_index('store_id'), on = 'store_id')
    df = df.merge(items.set_index('item_id'), on = 'item_id')

    return df
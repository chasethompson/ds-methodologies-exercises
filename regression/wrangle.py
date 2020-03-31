from env import host, user, password
import pandas as pd
import numpy as np

def get_db_url(username, hostname, password, db_name):
    return f'mysql+pymysql://{username}:{password}@{hostname}/{db_name}'

def wrangle_telco():
    url = get_db_url(user, host, password, 'telco_churn')
    query = '''
    SELECT customer_id, monthly_charges, tenure, total_charges
    FROM customers
    WHERE contract_type_id = 3;
    '''
    telco = pd.read_sql(query,url)
    telco['total_charges'] = telco['total_charges'].replace(r'^\s*$', '0', regex=True)
    telco['total_charges'] = telco['total_charges'].astype(float)
    telco.dropna(inplace=True)
    return telco

if __name__ == '__main__':
    wrangle_telco()
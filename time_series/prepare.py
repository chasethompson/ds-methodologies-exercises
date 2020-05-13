import pandas as pd
import numpy as np
import requests
import os.path

# ~~~~~ Prepare Store Data ~~~~~ #

# ----------------- #
#  PREP STORE DATA  #
# ----------------- #

def prepare_sale():
    df = acquire.get_store_data()
    df['month'] = df.index.month
    df['day_of_week'] = df.index.weekday
    df['total_sales'] = df.sale_amount * df.item_price
    sales_sum = df.resample("D")[['total_sales']].sum()
    sales_sum['sales_differences'] = sales_sum['total_sales'].diff()
    return df, sales_sum
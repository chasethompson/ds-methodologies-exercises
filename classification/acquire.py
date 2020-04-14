import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np 
from env import host, user, password

# function to contact database

def get_db_url(db_name):
    return f"mysql+pymysql://{user}:{password}@{host}/{db_name}"

# function to query db and return df

def get_titanic_data():
    url = get_db_url('titanic_db')
    query = """
    SELECT
        *
    FROM
        passengers
    """
    titanic = pd.read_sql(query,url)
    return titanic

def get_iris_data():
    url = get_db_url('iris_db')
    query = """
    SELECT
        *
    FROM
        species
    JOIN
        measurements USING(species_id)
    """
    iris_db = pd.read_sql(query,url)
    return iris_db
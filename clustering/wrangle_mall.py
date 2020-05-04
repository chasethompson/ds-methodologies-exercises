from env import host, user, password
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, MinMaxScaler

# ----------------- #
#      Acquire      #
# ----------------- #

def get_db_url(db_name):
    return f"mysql+pymysql://{user}:{password}@{host}/{db_name}"

def get_mall_data():
    url = get_db_url('mall_customers')
    query = query = """
    SELECT *
    FROM customers
    """
    df = pd.read_sql(query,url)
    return df

# ------------------ #
#       Prep         #
# ------------------ #

# Find outliers
def get_upper_outliers(s, k):
    '''
    Given a series and a cutoff value, k, returns the upper outliers for the
    series.
    The values returned will be either 0 (if the point is not an outlier), or a
    number that indicates how far away from the upper bound the observation is.
    '''
    q1, q3 = s.quantile([.25, .75])
    iqr = q3 - q1
    upper_bound = q3 + k * iqr
    return s.apply(lambda x: max([x - upper_bound, 0]))

def add_upper_outlier_columns(df, k):
    '''
    Add a column with the suffix _outliers for all the numeric columns
    in the given dataframe.
    '''
    # outlier_cols = {col + '_outliers': get_upper_outliers(df[col], k)
    #                 for col in df.select_dtypes('number')}
    # return df.assign(**outlier_cols)

    for col in df.select_dtypes('number'):
        df[col + '_outliers'] = get_upper_outliers(df[col], k)

    return df


# Encode
def ohe(col, X_train, X_test):
    ''' 
    Function to fit and transform a OneHotEncoder to encode columns and replace the new values in our train, validate, and test df
    '''
    # Creates and fits that encoder
    encoder = OneHotEncoder().fit(X_train[[col]])
    
    # Transforms and replaced the new columns back to the dataframes
    m = encoder.transform(X_train[[col]]).todense()
    X_train = pd.concat([X_train, pd.DataFrame(m, columns= col +"_"+ encoder.categories_[0], index=X_train.index)], axis = 1)
    
    m = encoder. transform(X_test[[col]]).todense()
    X_test = pd.concat([X_test, pd.DataFrame(m, columns=col +"_"+ encoder.categories_[0], index = X_test.index)], axis = 1)
    
    X_train.drop(columns=col,inplace=True)
    X_test.drop(columns=col, inplace=True)
    
    return X_train, X_test
    
# Scale
def return_values(scaler, train, test):
    '''
    Helper function used to updated the scaled arrays and transform them into usable dataframes
    '''
    train_scaled = pd.DataFrame(scaler.transform(train), columns=train.columns.values).set_index([train.index.values])
    test_scaled = pd.DataFrame(scaler.transform(test), columns=test.columns.values).set_index([test.index.values])
    return scaler, train_scaled, test_scaled

# Linear scaler
def min_max_scaler(train, test):
    '''
    Helper function that scales that data. Returns scaler, as well as the scaled dataframes
    '''
    scaler = MinMaxScaler().fit(test)
    scaler, train_scaled, test_scaled = return_values(scaler, train, test)
    return scaler, train_scaled, test_scaled

def prep_mall_data(df):
    # Split
    train, test = train_test_split(df, random_state=123, train_size=.8)

    # Encode
    train, test = ohe("gender", train, test)

    # Scale
    train_scaled = train.drop(columns=["gender_Male", "gender_Female"])
    test_scaled = test.drop(columns=["gender_Male", "gender_Female"])

    _, train_scaled, test_scaled = min_max_scaler(train_scaled, test_scaled)

    train_scaled["gender_male"] = train["gender_Male"]
    train_scaled["gender_female"] = train["gender_Female"]

    test_scaled["gender_male"] = test["gender_Male"]
    test_scaled["gender_female"] = test["gender_Female"]

    return train_scaled, test_scaled
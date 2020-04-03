import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from math import sqrt
from scipy import stats
from sklearn.model_selection import train_test_split
from pydataset import data

from env import host, user, password
from wrangle import wrangle_telco

def split_my_data(df, train_pct):
    train, test = train_test_split(df, train_size=train_pct)
    return train, test

# def split_my_data(X, y, train_pct):
#     """
#     Take in X_train, X_test, y_train, y_test

#     When calling the function name the variables:
#     X_train, X_test, y_train, y_test = split_my_data(X, y, .8)

#     """
#     return (train_test_split(X, y, train_size = train_pct))

def standard_scaler(train, test):
    """

    When calling the function rename the variables to maintain original:
    scaler, X_train_scaled, X_test_scaled = standard_scaler(X_train, X_test)

    """
    scaler = StandardScaler(copy=True, with_mean=True, with_std=True).fit(train)
    train_scaled = pd.DataFrame(scaler.transform(train), columns=train.columns.values).set_index([train.index.values])
    test_scaled = pd.DataFrame(scaler.transform(test), columns=test.columns.values).set_index([test.index.values])
    return scaler, train_scaled, test_scaled

def scale_inverse(train_scaled, test_scaled, scaler):
    """
    Takes in the scaler, X_train_scaled and X_test_scaled DataFrames. Then it returns the X_train_unscaled and X_test_unscaled.

    When calling the function rename the variables to maintain original:
    X_train_unscaled, X_test_unscaled = scale_inverse(train_scaled, test_scaled, scaler)

    """
    train_unscaled = pd.DataFrame(scaler.inverse_transform(train_scaled), columns=train_scaled.columns.values).set_index([train_scaled.index.values])
    test_unscaled = pd.DataFrame(scaler.inverse_transform(test_scaled), columns=test_scaled.columns.values).set_index([test_scaled.index.values])
    return train_unscaled, test_unscaled

def uniform_scaler(train, test):
    """
    Quantile transformer, non -linear transformation - uniform.
    Reduces impact of outliears, smooths out unusual distributions.

    When calling the function rename the variables to maintain original:
    X_train_uniform_scaled, X_test_uniform_scaled = uniform_scaler(X_train, X_test)

    """
    scaler = QuantileTransformer(n_quantiles=100, output_distribution='uniform', random_state=123, copy=True).fit(train)
    train_scaled = pd.DataFrame(scaler.transform(train), columns=train.columns.values).set_index([train.index.values])
    test_scaled = pd.DataFrame(scaler.transform(test), columns=test.columns.values).set_index([test.index.values])
    return train_scaled, test_scaled


def gaussian_scaler(train, test):
    """
    Transforms and then normalizes data.
    yeo_johnson allows for negative data, box_cox allows for positive data only.

    When calling the function rename the variables to maintain original:
    scaler, X_train_gaussian_scaled, X_test_gaussian_scaled = gaussian_scaler(X_train, X_test)

    """    
    scaler = PowerTransformer(method='yeo-johnson', standardize=False, copy=True).fit(train)
    train_scaled = pd.DataFrame(scaler.transform(train), columns=train.columns.values).set_index([train.index.values])
    test_scaled = pd.DataFrame(scaler.transform(test), columns=test.columns.values).set_index([test.index.values])
    return scaler, train_scaled, test_scaled

def min_max_scaler(train, test):
    """

    When calling the function rename the variables to maintain original:
    X_train_min_max_scaled, X_test_min_max_scaled = min_max_scaler(X_train, X_test)

    """  

    scaler = MinMaxScaler(copy=True, feature_range=(0,1)).fit(train)
    train_scaled = pd.DataFrame(scaler.transform(train), columns=train.columns.values).set_index([train.index.values])
    test_scaled = pd.DataFrame(scaler.transform(test), columns=test.columns.values).set_index([test.index.values])
    return train_scaled, test_scaled

def iqr_robust_scaler(train, test):
    """
    Scales features using stats that are robust to outliers by removing the median and scaling data to the IQR.

    When calling the function rename the variables to maintain original:
    X_train_iqr_robust_scaled, X_test_iqr_robust_scaled = iqr_robust_scaler(X_train, X_test)

    """ 
    scaler = RobustScaler(quantile_range=(25.0,75.0), copy=True, with_centering=True, with_scaling=True).fit(train)
    train_scaled = pd.DataFrame(scaler.transform(train), columns=train.columns.values).set_index([train.index.values])
    test_scaled = pd.DataFrame(scaler.transform(test), columns=test.columns.values).set_index([test.index.values])
    return train_scaled, test_scaled


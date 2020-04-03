import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score
from sklearn.linear_model import LinearRegression

from math import sqrt
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler

import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pydataset
import scipy.stats as stats
import sklearn.metrics
from statsmodels.formula.api import ols

#Setup Functions

def residuals(actual, predicted):
    return predicted - actual

def sse(actual, predicted):
    return (residuals(actual, predicted) ** 2).sum()

def mse(actual, predicted):
    n = actual.shape[0]
    return sse(actual, predicted) / n

def rmse(actual, predicted):
    return math.sqrt(mse(actual, predicted))

def ess(actual, predicted):
    return ((predicted - actual.mean()) ** 2).sum()

def tss(actual):
    return ((actual - actual.mean()) ** 2).sum()

def r2_score(actual, predicted):
    return ess(actual, predicted) / tss(actual)

# Evaluation Functions

def plot_residuals(df):
    sns.scatterplot(x="yhat", y="residual", data=df)
    return plt.show()

# regression_errors(y, yhat): returns the following values:
# sum of squared errors (SSE)
# explained sum of squares (ESS)
# total sum of squares (TSS)
# mean squared error (MSE)
# root mean squared error (RMSE)

def regression_errors(df):
    """
    Return a DataFrame with the SSE, ESS, TSS, MSE, RMSE for the y variable
    
    """
    #SSE
    SSE = mean_squared_error(df.y, df.yhat) * len(df)
    #ESS
    ESS = sum((df.yhat - df['y'].mean())**2)
    #TSS
    TSS = SSE + ESS
    #MSE
    MSE = mean_squared_error(df.y, df.yhat)
    #RMSE
    RMSE = sqrt(mean_squared_error(df.y, df.yhat))
    
    return SSE, ESS, TSS, MSE, RMSE

# baseline_mean_errors(y): computes the SSE, MSE, and RMSE for the baseline model

def baseline_mean_errors(df):
    """
    Return a DataFrame with the SSE, ESS, TSS, MSE, RMSE for the baseline
    
    """
    df['yhat_baseline'] = df['y'].mean()
    #SSE
    SSE_baseline = mean_squared_error(df.y, df.yhat_baseline) * len(df)
    #MSE
    MSE_baseline = mean_squared_error(df.y, df.yhat_baseline)
    #RMSE
    RMSE_baseline = sqrt(mean_squared_error(df.y, df.yhat_baseline))
    
    return SSE_baseline, MSE_baseline, RMSE_baseline

# better_than_baseline(y, yhat): returns true if your model performs better than the baseline, otherwise false

def better_than_baseline(df):
    """
    Returns TRUE if your model peforms better than the baseline, else FALSE
    
    """
    RMSE = sqrt(mean_squared_error(df.y, df.yhat))
    RMSE_baseline = sqrt(mean_squared_error(df.y, df.yhat_baseline))
    
    if RMSE < RMSE_baseline:
        return True
    else:
        return False

# model_significance(ols_model): that takes the ols model as input and returns the amount of variance
# explained in your model, and the value telling you whether your model is significantly better than the
# baseline model (Hint: use the rsquared and f_pvalue properties from the ols model)

def model_significance(ols_model):
    """
    Returns the R^2 and p-value based on the model
    
    """
    r2 = ols_model.rsquared
    p = ols_model.f_pvalue
    return print("p-value =", round(p,3), "R-squared =", round(r2, 3))

# # Class Version

#     def plot_residuals(actual, predicted):
#     residuals = actual - predicted
#     plt.hlines(0, actual.min(), actual.max(), ls=':')
#     plt.scatter(actual, residuals)
#     plt.ylabel('residual ($y - \hat{y}$)')
#     plt.xlabel('actual value ($y$)')
#     plt.title('Actual vs Residual')
#     return plt.gca()

# def regression_errors(actual, predicted):
#     return {
#         'sse': sse(actual, predicted),
#         'ess': ess(actual, predicted),
#         'tss': tss(actual),
#         'mse': mse(actual, predicted),
#         'rmse': rmse(actual, predicted),
#     }

# def baseline_mean_errors(actual):
#     predicted = actual.mean()
#     return {
#         'sse': sse(actual, predicted),
#         'mse': mse(actual, predicted),
#         'rmse': rmse(actual, predicted),
#     }

# def better_than_baseline(actual, predicted):
#     sse_baseline = sse(actual, actual.mean())
#     sse_model = sse(actual, predicted)
#     return sse_model < sse_baseline

# def model_significance(ols_model):
#     return {
#         'r^2 -- variance explained': ols_model.rsquared,
#         'p-value -- P(data|model == baseline)': ols_model.f_pvalue,
#     }
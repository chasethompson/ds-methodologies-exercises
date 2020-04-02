import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import warnings
warnings.filterwarnings("ignore")

from env import host, user, password
from wrangle import wrangle_telco
import split_scale

def plot_variable_pairs(df, hue=None):
    g = sns.pairplot(df, hue=hue, kind="reg")
    g.map_diag(plt.hist)
    g.map_offdiag(plt.scatter);

# # Different Version

# def plot_variable_pairs(df):
#     g = sns.pairplot(df, kind='reg', plot_kws = {'line_kws': {'color' : 'orange'}})

# # Class Option
# def plot_variable_pairs(df):
#     g = sns.pairplot(df, kind="reg", corner=True, diag_kind="kde"
#     g.fig.suptitle("Scatterplot with Regression for Continuous Variables")
#     plt.show())

# Use this to check the version

sns.__version__

def months_to_years(df):
    df['tenure_years'] = df.tenure // 12
    df['tenure_years'] = df.tenure_years.astype('category')
    return df

# #Class version
# def months_to_years(n_months, df, rounding=False):
#     if rounding:
#         df["tenure_years"] = np.round(n_months / 12)
#         return df
#     else:
#         df["tenure_years"] = n_months // 12
#         return df

def plot_categorical_and_continuous_vars(categorical_var, continuous_var, df):
    xvals=categorical_var
    yvals=continuous_var
    plt.figure(figsize=(16,9))
    plt.subplot(1,3,1)
    p1 = sns.boxenplot(x=xvals, y=yvals, data=df)
    plt.subplot(1,3,2)
    p2 = sns.scatterplot(x=xvals, y=yvals, data=df)
    plt.subplot(1,3,3)
    p3 = sns.stripplot(x=xvals, y=yvals, data=df)
    plt.show()

# # Extra function from Jeremy

# def do_a_pandas_profile(df, name):
#     from pandas_profiling import ProfileReport
#     profile = ProfileReport(df, title=name, html={'style':{'full_width':True}})
#     return profile.to_widgets(), profile.to_notebook_iframe()
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import sklearn.preprocessing
import sklearn.model_selection
import sklearn.impute
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, MinMaxScaler

import env
import acquire
import split_scale

###  IRIS DATA ###

# def encode_species(train, test):
#     encoder = sklearn.preprocessing.OneHotEncoder()
#     encoder.fit(train[['species']])
    
#     cols = ['species_' + c for c in encoder.categories_[0]]
    
#     m = encoder.transform(train[['species']]).todense()

#     train = pd.concat([train,pd.DataFrame(m, columns=cols, index=train.index)], axis=1)
    
#     m = encoder.transform(test[['species']]).todense()
    
#     test = pd.concat([test,pd.DataFrame(m, columns=cols, index=test.index)], axis=1)
    
#     return train, test

# def prep_iris(df):
#     df = df.drop(columns=['species_id'])
#     df = df.rename(columns={'species_name':'species'})
#     train, test = sklearn.model_selection.train_test_split(df, train_size=.8)
#     train, test = encode_species(train, test)
#     return train, test


def label_encode(train, test):
    le = LabelEncoder()
    train['species'] = le.fit_transform(train.species)
    test['species'] = le.transform(test.species)
    return le, train, test


def prep_iris(df):
    df = df.drop(columns='species_id')
    df = df.rename(columns={'species_name': 'species'})
    train, test = train_test_split(df, train_size=.75, stratify=df.species, random_state=123)
    train, test, le = label_encode(train, test)
    return train, test, le


def inverse_encode(train, test, le):
    train['species'] = le.inverse_transform(train.species)
    test['species'] = le.inverse_transform(test.species)
    return train, test


###  TITANIC DATA ###

def drop_columns(df):
    return df.drop(columns="deck")

def fill_na(df):
    df.embark_town = df.embark_town.fillna('Southampton')
    df.embarked = df.embarked.fillna('S')
    return df
    
def encode_titanic(train, test):
    encoder = sklearn.preprocessing.OneHotEncoder()
    encoder.fit(train[["embarked"]])

    m1 = encoder.transform(train[["embarked"]]).todense()

    train = pd.concat([train, pd.DataFrame(m1, columns=encoder.categories_[0], index=train.index)], axis=1)

    m2 = encoder.transform(test[["embarked"]]).todense()

    test = pd.concat([test, pd.DataFrame(m2, columns=encoder.categories_[0], index=test.index)], axis=1)

    return train, test

def impute_titanic(train, test):
    imputer = sklearn.impute.SimpleImputer(strategy='mean')
    imputer.fit(train[['age']])
    train.age = imputer.transform(train[['age']])
    test.age = imputer.transform(test[['age']])

    return train, test

def scale_titanic(train, test):
    train_scaled = train[['age', 'fare']]
    test_scaled = test[['age', 'fare']]
    scaler, train_scaled, test_scaled = split_scale.min_max_scaler(train_scaled, test_scaled)
    return scaler, train_scaled, test_scaled

def prep_titanic(df):
    df = drop_columns(df)
    df = fill_na(df)
    train, test = sklearn.model_selection.train_test_split(df, random_state=19, train_size = .8)
    train, test = encode_titanic(train, test)
    train, test = impute_titanic(train, test)
    scaler, train_scaled, test_scaled = scale_titanic(train, test)
    train.update(train_scaled)
    test.update(test_scaled)
    return scaler, train, test

def prep_titanic_no_scale(df):
    df = drop_columns(df)
    df = fill_na(df)
    train, test = sklearn.model_selection.train_test_split(df, train_size = .8)
    train, test = encode_titanic(train, test)
    train, test = impute_titanic(train, test)
    #scaler, train_scaled, test_scaled = scale_titanic(train, test)
    #train.update(train_scaled)
    #test.update(test_scaled)
    return train, test
# -*- coding: utf-8 -*-

import os
import configparser
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
import numpy as np
import time
import logging
import pandas as pd
#import plotex
import datetime as DT
from importlib import resources
from tsf import constants


config = configparser.ConfigParser()
config.read_string(resources.read_text("tsf", "config.ini"))

value_column = config.get('TIMESERIES', 'ENDOG_COLUMN')
date_column = config.get('TIMESERIES', 'DATE_COLUMN')


def imputation(ts, column, imputation_var):
    interpolate_model = constants.INTERPOLATE_MODELS
    mse_final = constants.MSE_FINAL
    logging.info("Performing Imputations for %s column: %s, using methods: %s",
                 imputation_var, column, str(interpolate_model))
    for model in interpolate_model:
        timeseries = ts.copy()
        if (model == 'spline'):
            order = int(config.get('INTERPOLATE', 'ORDER'))
            timeseries[column].interpolate(
                method=model, order=order, inplace=True)
            mse, _ = reference_model(timeseries, column)
            if (mse < mse_final):
                temp = ts.copy()
                mse_final = mse
                temp[column].interpolate(
                    method=model, order=order, inplace=True)
        elif (model == 'ffill'):
            timeseries[column] = timeseries[column].ffill()
            mse, _ = reference_model(timeseries, column)
            if (mse < mse_final):
                temp = ts.copy()
                mse_final = mse
                temp[column] = temp[column].ffill()
        elif (model == 'bfill'):
            timeseries[column] = timeseries[column].bfill()
            mse, _ = reference_model(timeseries, column)
            if (mse < mse_final):
                temp = ts.copy()
                mse_final = mse
                temp[column] = temp[column].bfill()
        else:
            timeseries[column].interpolate(method=model, inplace=True)
            mse, _ = reference_model(timeseries, column)
            if (mse < mse_final):
                temp = ts.copy()
                mse_final = mse
                temp[column].interpolate(method=model, inplace=True)
    return(temp)


def reference_model(ts, column):
    X_ts = pd.DataFrame(pd.to_datetime(ts.index, format='%Y-%m-%d %H:%M:%S'))
    X_ts['Timestamp'] = X_ts['Timestamp'].apply(
        lambda x: time.mktime(x.timetuple()))
    ts = ts.reset_index()
    Y_ts = np.asarray(ts[column])
    regr = linear_model.LinearRegression()
    regr.fit(X_ts, Y_ts)
    Y_pred = regr.predict(X_ts)
    mse = mean_squared_error(Y_ts, Y_pred)
    return (mse, Y_pred)


def check_numeric(ts):
    #ts = ts.loc[ts[value_column].notnull()]
    ts["check_value"] = pd.to_numeric(
        ts[value_column], errors='coerce').notnull()  # .all()
    return (ts)


def finding_index(resample_period=int(config.get('TIMESERIES', 'RESAMPLE_PERIOD'))):
    index_parameter = config.get('TIMESERIES', 'RESAMPLE')
    if (index_parameter == 'H'):
        timedel = DT.timedelta(hours=resample_period)
    elif(index_parameter == 'm'):
        timedel = DT.timedelta(minutes=resample_period)
    elif(index_parameter == 's'):
        timedel = DT.timedelta(seconds=resample_period)
    elif(index_parameter == 'W'):
        timedel = DT.timedelta(weeks=resample_period)
    elif(index_parameter == 'D'):
        timedel = DT.timedelta(days=resample_period)
    elif(index_parameter == 'M'):
        timedel = DT.timedelta(month=resample_period)
    elif(index_parameter == 'Y'):
        timedel = DT.timedelta(years=resample_period)
    return (timedel)


def sanity_check(data_df):
    data_df = check_numeric(data_df)
    data_df = data_df.drop(data_df[data_df.check_value != True].index)
    data_df = data_df[~data_df[date_column].duplicated(keep='first')]
    data_df = data_df.drop(["check_value"], axis=1)
    data_df = data_df.reset_index(drop=True)
    data_df[value_column] = data_df[value_column].astype(float)
    return (data_df)

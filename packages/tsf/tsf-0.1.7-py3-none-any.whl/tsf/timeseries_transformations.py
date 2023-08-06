# -*- coding: utf-8 -*-

import sys
import os
import numpy as np
import logging
import configparser
from importlib import resources
from tsf import constants


config = configparser.ConfigParser()
config.read_string(resources.read_text("tsf", "config.ini"))

value_column = config.get('TIMESERIES', 'ENDOG_COLUMN')


def log_transformation(timeseries):
    try:
        """
        Input: Non- stationary Error series 
        Output: Log Transformation of the series
        """
        minimum_value = min(timeseries[value_column])
        timeseries_log = np.log(timeseries[value_column]+1-minimum_value)
        print("transformed")
        return timeseries_log
    except Exception:
        logging.error("Log Transformation has issue")
        return False


def moving_average(timeseries):
    try:
        """
        Input: Non- stationary Error series 
        Output: Moving Average Transformation of the series
        """
        moving_avg = timeseries[value_column].rolling(3).mean()
        ts_moving_avg_diff = timeseries[value_column] - moving_avg
        ts_moving_avg_diff.dropna(inplace=True)
        return ts_moving_avg_diff
    except Exception:
        logging.error("Moving Average has issue")
        return False


def exponentially_weighted_moving_average(timeseries):
    try:
        """
        Input: Non- stationary Error series 
        Output: Exponentially weighted Moving Average Transformation of the series
        """
        halflife = 6
        alpha = 1-np.exp(np.log(0.5)/halflife)
        expwighted_avg = timeseries[value_column].ewm(
            alpha=alpha, adjust=False).mean()
        ts_ewma_diff = timeseries[value_column] - expwighted_avg
        return ts_ewma_diff
    except Exception:
        logging.error("Exponentially weighted moving average has issue")
        return False


def differencing(timeseries):
    try:
        """
        Input: Non- stationary Error series 
        Output: Differencing Transformation of the series
        """
        ts_diff = timeseries[value_column] - timeseries[value_column].shift()
        ts_diff.dropna(inplace=True)
        return ts_diff
    except Exception:
        logging.error("Differencing has issue")
        return False


def differencing_second_order(timeseries):
    try:
        """
        Input: Non- stationary Error series 
        Output:Second order Differencing Transformation of the series
        """
        ts_diff_secondorder = timeseries[value_column] - \
            timeseries[value_column].shift(periods=2)
        ts_diff_secondorder.dropna(inplace=True)
        return ts_diff_secondorder
    except Exception:
        logging.error("Second order Differencing has issue")
        return False

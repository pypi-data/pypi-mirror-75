# -*- coding: utf-8 -*-

import os
from arch.unitroot import ADF
import sys
import configparser
import pandas as pd
from importlib import resources
from tsf import constants


config = configparser.ConfigParser()
config.read_string(resources.read_text("tsf", "config.ini"))

value_column = config.get('TIMESERIES', 'ENDOG_COLUMN')

# DisablePrint


def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# RestorePrint


def enablePrint():
    sys.stdout = sys.__stdout__


def test_stationarity(timeseries):
    try:
        """
        Input: Takes the original error series
        Output: Performs Augmented Dickey Fuller Test, 1 if stationary ; 0 if not stationary
        """
        blockPrint()
        timeseries = pd.Series(timeseries[value_column])
        adf = ADF(timeseries)
        enablePrint()
        stat_value = round(adf.stat, 3)
        crit_value = adf.critical_values
        crit_value = crit_value[constants.TIMESERIES_THRESHOLD_CRITICAL_VALUE]
        if (stat_value < crit_value):
            return 1
        else:
            return 0
    except Exception:
        print("Issue in calculating statistical value")
        return False

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 17:37:49 2018
Modified on Thu Oct 25 17:12:08 2018
Modified on Fri Nov 16 12:08:00 2018
@author: Tanushree Halder
@credit: Pronojit Saha

Modified on Wed Jul 5 16:08:00 2020
@author: Pronojit Saha
@maintainer: Pronojit Saha
"""

import pandas as pd
import configparser
from importlib import resources
from tsf import constants
from tsf.forecaster import TimeSeriesForecaster as tsf
import warnings
warnings.filterwarnings('ignore')

config = configparser.ConfigParser()
config.read_string(resources.read_text("tsf", "config.ini"))


def main():
    filepath = config.get('TIMESERIES', 'FILEPATH')
    column = config.get('TIMESERIES', 'ENDOG_COLUMN')
    forecast_points = config.get('TIMESERIES', 'FORECAST_POINTS')
    forecast_points = int(forecast_points)
    data_df = pd.read_csv(filepath, na_values='Null', keep_default_na=True)
    tsf_model = tsf()
    Forecast, _, _ = tsf_model.forecast(
        data_df, column, forecast_points)
    print("The number of predictions requested is {0} and predictions are as below:".format(
        forecast_points))
    print(Forecast)


if __name__ == "__main__":
    main()

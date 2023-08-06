# -*- coding: utf-8 -*-[]

import pandas as pd
import os
import sys
import logging
from importlib import resources
import configparser

from sklearn.metrics import mean_squared_error
from math import sqrt
from statsmodels.tsa.api import Holt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.arima_model import ARIMA
import statsmodels.api as sm
from pmdarima.arima import auto_arima
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

from tsf import constants
from tsf import helper


config = configparser.ConfigParser()
config.read_string(resources.read_text("tsf", "config.ini"))

value_column = config.get('TIMESERIES', 'ENDOG_COLUMN')


def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}


def calculatingrmse(final_series_for_modeling, forecast_points, exog_data_adjusted):
    """ 
    This function carries out modeling using different techniques, finds the method with the least rmse 
    and then returns the forecast of that model
    """
    try:
        dict_values = {}
        final_series_for_modelingresult, predicted_trainingresult, rms = modelhwl(
            final_series_for_modeling, forecast_points)
        dict_values[rms] = {
            "Method": "HWL", "forecast": final_series_for_modelingresult, "training": predicted_trainingresult}
        final_series_for_modelingresult, predicted_trainingresult, rms = modelhwt(
            final_series_for_modeling, forecast_points)
        dict_values[rms] = {
            "Method": "HWT", "forecast": final_series_for_modelingresult, "training": predicted_trainingresult}
        final_series_for_modelingresult, predicted_trainingresult, rms = modelarima(
            final_series_for_modeling, forecast_points)
        dict_values[rms] = {
            "Method": "ARIMA", "forecast": final_series_for_modelingresult, "training": predicted_trainingresult}
        final_series_for_modelingresult, predicted_trainingresult, rms = modelarimax(
            final_series_for_modeling, forecast_points, exog_data_adjusted)
        dict_values[rms] = {
            "Method": "ARIMAX", "forecast": final_series_for_modelingresult, "training": predicted_trainingresult}
        final_series_for_modelingresult, predicted_trainingresult, rms = modelautoarima(
            final_series_for_modeling, forecast_points)
        dict_values[rms] = {"Method": "AUTOARIMA",
                            "forecast": final_series_for_modelingresult, "training": predicted_trainingresult}
        final_series_for_modelingresult, predicted_trainingresult, rms = modellr(
            final_series_for_modeling, forecast_points, exog_data_adjusted)
        dict_values[rms] = {"Method": "LinearRegression",
                            "forecast": final_series_for_modelingresult, "training": predicted_trainingresult}
        final_series_for_modelingresult, predicted_trainingresult, rms = modelrf(
            final_series_for_modeling, forecast_points, exog_data_adjusted)
        dict_values[rms] = {"Method": "RandomForest",
                            "forecast": final_series_for_modelingresult, "training": predicted_trainingresult}
        dict_values = without_keys(dict_values, constants.INVALID)
        if (dict_values):
            key = min(dict_values.keys())
            logging.info("The root mean square error for the forecast is {0} and method is {1}".format(
                round(key, 3), dict_values[key]["Method"]))
            final_series_for_modeling = dict_values[key]["forecast"]
            predicted_training = dict_values[key]["training"]
            rmse = dict_values[key]["Method"]
            return final_series_for_modeling, predicted_training, rmse
        else:
            """
            If all the keys are False i.e no model worked on timeseries
            """
            return False, False
    except Exception as my_error:
        _, _, exc_tb = sys.exc_info()
        logging.error(
            "Issue with calculating rmse: %s at lineno %s", my_error, exc_tb.tb_lineno)
        return False, False


def modelhwl(final_series_for_modeling, forecast_points):
    try:
        """
        Input: Either stationary original series or Transformed stationary series
        Output: Forecast Error for next period for the transformed/original series 
        ModeledData variable saves the forecast error at its location specified by TIMESERIRES_PREDICTED_MONTH_NUMBER
        """
        smoothing_level = float(
            config.get('HOLT_WINTERS_LINEAR', 'SMOOTHING_LEVEL'))
        smoothing_slope = float(
            config.get('HOLT_WINTERS_LINEAR', 'SMOOTHING_SLOPE'))
        fit2 = Holt(final_series_for_modeling, damped=True).fit(
            smoothing_level=smoothing_level, smoothing_slope=smoothing_slope)
        predicted_training = fit2.predict(
            start=final_series_for_modeling.index[0], end=final_series_for_modeling.index[-1])
        predicted_training = pd.DataFrame(
            predicted_training, columns=[value_column])
        rms = sqrt(mean_squared_error(
            final_series_for_modeling, predicted_training))
        y_pred = fit2.forecast(steps=forecast_points)
        final_series_for_modeling = pd.concat(
            [final_series_for_modeling, pd.DataFrame(y_pred)], axis=0)
        final_series_for_modeling.columns = [value_column]
        logging.info("Prediction Complete using HWL")
        return final_series_for_modeling, predicted_training, rms
    except Exception as my_error:
        _, _, exc_tb = sys.exc_info()
        logging.error(
            "Issue with HWL modeling: %s at lineno %s", my_error, exc_tb.tb_lineno)
        return False, False, False


def modelhwt(final_series_for_modeling, forecast_points):
    try:
        """
        Input: Either stationary original series or Transformed stationary series
        Output: Forecast Error for next period for the transformed/original series
        ModeledData variable saves the forecast error at its location specified by TIMESERIRES_PREDICTED_MONTH_NUMBER
        """
        trend = config.get('HOLT_WINTERS_TREND', 'TREND')
        seasonal = config.get('HOLT_WINTERS_TREND', 'SEASONAL')
        model = ExponentialSmoothing(
            final_series_for_modeling, trend=trend, seasonal=seasonal)
        fit2 = model.fit()
        predicted_training = fit2.predict(
            start=final_series_for_modeling.index[0], end=final_series_for_modeling.index[-1])
        predicted_training = pd.DataFrame(
            predicted_training, columns=[value_column])
        rms = sqrt(mean_squared_error(
            final_series_for_modeling, predicted_training))
        y_pred = fit2.forecast(steps=forecast_points)
        final_series_for_modeling = pd.concat(
            [final_series_for_modeling, pd.DataFrame(y_pred)], axis=0)
        final_series_for_modeling.columns = [value_column]
        logging.info("Prediction Complete using HWT")
        return final_series_for_modeling, predicted_training, rms
    except Exception as my_error:
        _, _, exc_tb = sys.exc_info()
        logging.error(
            "Issue with HWT modeling: %s at lineno %s", my_error, exc_tb.tb_lineno)
        return False, False, False


def modelarima(final_series_for_modeling, forecast_points):
    try:
        """
        Input: Either stationary original series or Transformed stationary series
        Output: Forecast Error for next period for the transformed/original series 
        ModeledData variable saves the forecast error at its location specified by TIMESERIRES_PREDICTED_MONTH_NUMBER
        """
        p = int(config.get('ARIMA', 'P'))
        d = int(config.get('ARIMA', 'D'))
        q = int(config.get('ARIMA', 'Q'))
        model = ARIMA(final_series_for_modeling, order=(p, d, q))
        fit2 = model.fit(disp=0)
        predicted_training = fit2.predict()
        predicted_training = pd.DataFrame(
            predicted_training, columns=[value_column])
        rms = sqrt(mean_squared_error(
            final_series_for_modeling, predicted_training))
        y_pred = fit2.forecast(steps=forecast_points)[0]
        final_series_for_modeling = pd.concat([final_series_for_modeling, pd.DataFrame(y_pred,
                                                                                       index=[final_series_for_modeling.index[-1] + helper.finding_index(timedels+1)
                                                                                              for timedels in range(forecast_points)])], axis=0)
        final_series_for_modeling.columns = [value_column]
        logging.info("Prediction Complete using ARIMA")
        return final_series_for_modeling, predicted_training, rms
    except Exception as my_error:
        _, _, exc_tb = sys.exc_info()
        logging.error(
            "Issue with ARIMA modeling: %s at lineno %s", my_error, exc_tb.tb_lineno)
        return False, False, False


def modelarimax(final_series_for_modeling, forecast_points, exog_data_adjusted):
    try:
        """
        Input: Either stationary original series or Transformed stationary series
        Output: Forecast Error for next period for the transformed/original series 
        ModeledData variable saves the forecast error at its location specified by TIMESERIRES_PREDICTED_MONTH_NUMBER
        """
        p = int(config.get('ARIMA', 'P'))
        d = int(config.get('ARIMA', 'D'))
        q = int(config.get('ARIMA', 'Q'))
        exog_data_prediction = exog_data_adjusted[-forecast_points:]
        exog_sample = exog_data_adjusted.sample(n=forecast_points)
        exog_data_adjusted = exog_data_adjusted.shift(periods=forecast_points)
        # removing nans due to shift by random sample
        exog_data_adjusted.iloc[:forecast_points] = exog_sample.iloc[:forecast_points].values
        model = sm.tsa.statespace.SARIMAX(final_series_for_modeling, order=(p, d, q), seasonal_order=(0, 0, 0, 0),
                                          enforce_stationarity=True, enforce_invertibility=False, exog=exog_data_adjusted)
        fit2 = model.fit(disp=0)
        predicted_training = fit2.predict()
        predicted_training = pd.DataFrame(
            predicted_training, columns=[value_column])
        rms = sqrt(mean_squared_error(
            final_series_for_modeling, predicted_training))
        y_pred = fit2.forecast(steps=forecast_points,
                               exog=exog_data_prediction)
        final_series_for_modeling = pd.concat([final_series_for_modeling, pd.DataFrame(y_pred,
                                                                                       index=[final_series_for_modeling.index[-1] + helper.finding_index(timedels+1)
                                                                                              for timedels in range(forecast_points)])], axis=0)
        final_series_for_modeling.columns = [value_column]
        logging.info("Prediction Complete using ARIMAX")
        return final_series_for_modeling, predicted_training, rms
    except Exception as my_error:
        _, _, exc_tb = sys.exc_info()
        logging.error(
            "Issue with ARIMAX modeling: %s at lineno %s", my_error, exc_tb.tb_lineno)
        return False, False, False


def modelautoarima(final_series_for_modeling, forecast_points):
    try:
        """
        Input: Either stationary original series or Transformed stationary series
        Output: Forecast Error for next period for the transformed/original series 
        ModeledData variable saves the forecast error at its location specified by TIMESERIRES_PREDICTED_MONTH_NUMBER
        """
        model = auto_arima(final_series_for_modeling, stepwise=True, trace=False, error_action='ignore',
                           suppress_warnings=True, out_of_sample_size=forecast_points)
        predicted_training = model.predict_in_sample()
        predicted_training = pd.DataFrame(
            predicted_training, columns=[value_column], index=final_series_for_modeling.index)
        rms = sqrt(mean_squared_error(
            final_series_for_modeling, predicted_training))
        y_pred = model.predict(forecast_points)
        final_series_for_modeling = pd.concat([final_series_for_modeling, pd.DataFrame(y_pred,
                                                                                       index=[final_series_for_modeling.index[-1] + helper.finding_index(timedels+1)
                                                                                              for timedels in range(forecast_points)])], axis=0)
        logging.info("Prediction Complete using Auto ARIMA")
        return final_series_for_modeling, predicted_training, rms
    except Exception as my_error:
        _, _, exc_tb = sys.exc_info()
        logging.error(
            "Issue with Auto ARIMA modeling: %s at lineno %s", my_error, exc_tb.tb_lineno)
        return False, False, False


def modellr(final_series_for_modeling, forecast_points, exog_data_adjusted):
    try:
        exog_data_prediction = exog_data_adjusted[-forecast_points:]
        exog_sample = exog_data_adjusted.sample(n=forecast_points)
        exog_data_adjusted = exog_data_adjusted.shift(periods=forecast_points)
        # removing nans due to shift by random sample
        exog_data_adjusted.iloc[:forecast_points] = exog_sample.iloc[:forecast_points].values
        model = LinearRegression().fit(exog_data_adjusted, final_series_for_modeling)
        predicted_training = model.predict(exog_data_adjusted)
        predicted_training = pd.DataFrame(predicted_training, columns=[
                                          value_column], index=final_series_for_modeling.index)
        rms = sqrt(mean_squared_error(
            final_series_for_modeling, predicted_training))
        y_pred = model.predict(exog_data_prediction)
        final_series_for_modeling = pd.concat([final_series_for_modeling, pd.DataFrame(y_pred,
                                                                                       index=[final_series_for_modeling.index[-1] + helper.finding_index(timedels+1)
                                                                                              for timedels in range(forecast_points)])], axis=0)
        final_series_for_modeling.columns = [value_column]
        logging.info("Prediction Complete using Linear Regression")
        return final_series_for_modeling, predicted_training, rms
    except Exception as my_error:
        _, _, exc_tb = sys.exc_info()
        logging.error(
            "Issue with Linear Regression modeling: %s at lineno %s", my_error, exc_tb.tb_lineno)
        return False, False, False


def modelrf(final_series_for_modeling, forecast_points, exog_data_adjusted):
    try:
        exog_data_prediction = exog_data_adjusted[-forecast_points:]
        exog_sample = exog_data_adjusted.sample(n=forecast_points)
        exog_data_adjusted = exog_data_adjusted.shift(periods=forecast_points)
        # removing nans due to shift by random sample
        exog_data_adjusted.iloc[:forecast_points] = exog_sample.iloc[:forecast_points].values

        model = RandomForestRegressor(n_estimators=1000, random_state=0)
        model.fit(exog_data_adjusted, final_series_for_modeling)
        predicted_training = model.predict(exog_data_adjusted)
        predicted_training = pd.DataFrame(predicted_training, columns=[
                                          value_column], index=final_series_for_modeling.index)
        rms = sqrt(mean_squared_error(
            final_series_for_modeling, predicted_training))
        y_pred = model.predict(exog_data_prediction)
        final_series_for_modeling = pd.concat([final_series_for_modeling, pd.DataFrame(y_pred,
                                                                                       index=[final_series_for_modeling.index[-1] + helper.finding_index(timedels+1)
                                                                                              for timedels in range(forecast_points)])], axis=0)
        final_series_for_modeling.columns = [value_column]
        logging.info("Prediction Complete using Random Forest")
        return final_series_for_modeling, predicted_training, rms
    except Exception as my_error:
        _, _, exc_tb = sys.exc_info()
        logging.error(
            "Issue with Random Forest modeling: %s at lineno %s", my_error, exc_tb.tb_lineno)
        return False, False, False

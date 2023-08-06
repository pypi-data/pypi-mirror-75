# -*- coding: utf-8 -*-

import os
import numpy as np
import logging
import pandas as pd
from datetime import timedelta

from tsf import constants
from tsf import helper


def log_transformation(predicted_timeseries, original_timeseries, forecast_points):
    try:
        """
        Input: Log Transformed series with the additional forecast value
        Output: Scaled to original series
        """
        datapoints_retrieved = -(forecast_points)
        timeseries_exp = np.exp(predicted_timeseries)
        minimum_timeseries = min(original_timeseries)
        predicted_timeseries = timeseries_exp+minimum_timeseries-1
        predicted_reverse_transformed_values = predicted_timeseries.iloc[datapoints_retrieved:]
        return predicted_reverse_transformed_values
    except Exception as my_error:
        logging.error("Reverse Log Transformation throws %s", my_error)
        return False


def moving_average(predicted_timeseries, original_timeseries, forecast_points):
    try:
        """
        Input: Moving Average Transformed series with the additional forecast value
        Output: Scaled to original series
        """
        datapoints_retrieved = -(forecast_points)
        moving_average = original_timeseries.rolling(3).mean()
        timedel = helper.finding_index()
        for i in range(forecast_points):
            moving_average = moving_average.append(pd.Series(
                [(original_timeseries.iloc[-1]+original_timeseries.iloc[-2]+np.average(original_timeseries))/3], index=[moving_average.index[-1] + timedel]))
        moving_average.dropna(inplace=True)
        predicted_timeseries = predicted_timeseries.add(moving_average)
        predicted_reverse_transformed_values = (
            predicted_timeseries.iloc[datapoints_retrieved:])
        return predicted_reverse_transformed_values
    except Exception as my_error:
        logging.error("Reverse Moving Average throws %s", my_error)
        return False


def exponentially_weighted_moving_average(predicted_timeseries, original_timeseries, forecast_points):
    try:
        """for i in range(forecast_points):
        Input: Exponentially Weighted Moving Average Transformed series with the additional forecast value
        Output: Scaled to original series
        """
        datapoints_retrieved = -(forecast_points)
        timedel = helper.finding_index()
        for i in range(forecast_points):
            original_timeseries = original_timeseries.append(pd.Series([np.average(
                original_timeseries)], index=[original_timeseries.index[-1] + timedel]))
        alpha = 1-np.exp(np.log(constants.DECAY_LOG_CONSTANT) /
                         constants.HALFLIFE)
        expwighted_avg = original_timeseries.ewm(
            alpha=alpha, adjust=False).mean()
        predicted_timeseries = predicted_timeseries.add(expwighted_avg)
        predicted_reverse_transformed_values = (
            predicted_timeseries.iloc[datapoints_retrieved:])
        return predicted_reverse_transformed_values
    except Exception as my_error:
        logging.error(
            "Reverse Exponentially Weighted Moving Average throws %s", my_error)
        return False


def differencing(predicted_timeseries, original_timeseries, forecast_points):
    try:
        """
        Input: Differencing Transformed series with the additional forecast value
        Output: Scaled to original series
        """
        datapoints_retrieved = -(forecast_points)
        original_timeseries_shift = original_timeseries.shift()
        timedel = helper.finding_index()
        for i in range(forecast_points):
            original_timeseries_shift = original_timeseries_shift.append(pd.Series(
                [original_timeseries.iloc[-1]], index=[original_timeseries_shift.index[-1] + timedel]))
        original_timeseries_shift.dropna(inplace=True)
        predicted_timeseries = predicted_timeseries.add(
            original_timeseries_shift)
        predicted_reverse_transformed_values = (
            predicted_timeseries.iloc[datapoints_retrieved:])
        return predicted_reverse_transformed_values
    except Exception as my_error:
        logging.error("Differencing throws %s", my_error)
        return False


def differencing_second_order(predicted_timeseries, original_timeseries, forecast_points):
    try:
        """
        Input: Second Order Differencing Transformed series with the additional forecast value
        Output: Scaled to original series
        """
        datapoints_retrieved = -(forecast_points)
        original_timeseries_shift = original_timeseries.shift(periods=2)
        timedel = helper.finding_index()
        for i in range(forecast_points):
            original_timeseries_shift = original_timeseries_shift.append(pd.Series(
                [original_timeseries.iloc[-2]], index=[original_timeseries_shift.index[-1] + timedel]))
        original_timeseries_shift.dropna(inplace=True)
        predicted_timeseries = predicted_timeseries.add(
            original_timeseries_shift)
        predicted_reverse_transformed_values = (
            predicted_timeseries.iloc[datapoints_retrieved:])
        return predicted_reverse_transformed_values
    except Exception as my_error:
        logging.error("Second Order Differencing throws %s", my_error)
        return False


def log_transformation_training(predicted_training, original_timeseries):
    try:
        """
        Input: Log Transformed series with the additional forecast value
        Output: Scaled to original series
        """
        timeseries_exp = np.exp(predicted_training)
        minimum_timeseries = min(original_timeseries)
        predicted_training_reverse_transformed = timeseries_exp+minimum_timeseries-1
        return predicted_training_reverse_transformed
    except Exception as my_error:
        logging.error("Reverse Log Transformation throws %s", my_error)
        return False


def moving_average_training(predicted_training, original_timeseries):
    try:
        """
        Input: Moving Average Transformed series with the additional forecast value
        Output: Scaled to original series
        """
        moving_average = original_timeseries.rolling(3).mean()
        moving_average = moving_average.fillna(method='backfill')
        predicted_training = predicted_training.reindex(predicted_training.index.insert(
            0, predicted_training.index[0]+timedelta(days=-1)), method='bfill')
        predicted_training = predicted_training.reindex(predicted_training.index.insert(
            0, predicted_training.index[0]+timedelta(days=-1)), method='bfill')
        predicted_training = predicted_training.fillna(method='backfill')
        predicted_training = predicted_training.add(moving_average)
        predicted_training_reverse_transformed = predicted_training.fillna(
            method='backfill')
        return predicted_training_reverse_transformed
    except Exception as my_error:
        logging.error("Reverse Moving Average throws %s", my_error)
        return False


def exponentially_weighted_moving_average_training(predicted_training, original_timeseries):
    try:
        """
        Input: Exponentially Weighted Moving Average Transformed series with the additional forecast value
        Output: Scaled to original series
        """
        alpha = 1-np.exp(np.log(constants.DECAY_LOG_CONSTANT) /
                         constants.HALFLIFE)
        expwighted_avg = original_timeseries.ewm(
            alpha=alpha, adjust=False).mean()
        predicted_training_reverse_transformed = predicted_training.add(
            expwighted_avg)
        return predicted_training_reverse_transformed
    except Exception as my_error:
        logging.error(
            "Reverse Exponentially Weighted Moving Average throws %s", my_error)
        return False


def differencing_training(predicted_training, original_timeseries):
    try:
        """
        Input: Differencing Transformed series with the additional forecast value
        Output: Scaled to original series
        """
        original_timeseries_shift = original_timeseries.shift()
        original_timeseries_shift = original_timeseries_shift.fillna(
            method='bfill')
        predicted_training.index += timedelta(days=2)
        predicted_training_reverse_transformed = predicted_training.add(
            original_timeseries_shift)
        predicted_training_reverse_transformed = predicted_training_reverse_transformed.fillna(
            method='bfill')
        return predicted_training_reverse_transformed
    except Exception as my_error:
        logging.error("Differencing throws %s", my_error)
        return False


def differencing_second_order_training(predicted_training, original_timeseries):
    try:
        """
        Input: Second Order Differencing Transformed series with the additional forecast value
        Output: Scaled to original series
        """
        original_timeseries_shift = original_timeseries.shift(periods=2)
        original_timeseries_shift = original_timeseries_shift.fillna(
            method='bfill')
        predicted_training.index += timedelta(days=2)
        predicted_training_reverse_transformed = predicted_training.add(
            original_timeseries_shift)
        predicted_training_reverse_transformed = predicted_training_reverse_transformed.fillna(
            method='bfill')
        return predicted_training_reverse_transformed
    except Exception as my_error:
        logging.error("Second Order Differencing throws %s", my_error)
        return False

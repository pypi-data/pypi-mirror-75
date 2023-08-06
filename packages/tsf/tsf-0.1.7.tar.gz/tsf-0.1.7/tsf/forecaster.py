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

import os
import os.path
import sys
import pandas as pd
import configparser
import ast
import numpy as np
import logging
from importlib import resources

from tsf import timeseries_transformations
from tsf import timeseries_stat_test
from tsf import timeseries_modeling
from tsf import timeseries_reverse_transformations
from tsf import constants
from tsf import helper


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s')
config = configparser.ConfigParser()
config.read_string(resources.read_text("tsf", "config.ini"))

date_column = config.get('TIMESERIES', 'DATE_COLUMN')
exog_column = ast.literal_eval(config.get("TIMESERIES", "EXOG_COLUMN"))
resample = config.get('TIMESERIES', 'RESAMPLE')


class DataPrep:
    def __init__(self):
        pass

    def treatment_exog(self, data_df, exog, list_numeric_column, list_categorical_column):
        total_length = len(data_df)
        nan_data = pd.isna(data_df[exog]).sum()
        non_numeric_data = pd.to_numeric(
            data_df[exog], errors='coerce').isna().sum()
        character_data = non_numeric_data - nan_data
        if character_data > int(constants.DECIDE_CAT_NUM_THRESHOLD*total_length):
            data_df.loc[pd.to_numeric(
                data_df[exog], errors='coerce').isna() == False, exog] = np.nan
            data_df[exog] = data_df[exog].fillna(data_df[exog].mode()[0])
            dummy_columns = pd.get_dummies(data_df[exog])
            data_df = pd.concat([data_df, dummy_columns], axis=1)
            data_df = data_df.drop([exog], axis=1)
            list_categorical_column.append(list(dummy_columns.columns))
        else:
            data_df.loc[pd.to_numeric(
                data_df[exog], errors='coerce').isna() == True, exog] = np.nan
            list_numeric_column.append(exog)
        return (data_df, list_numeric_column, list_categorical_column)

    def feature_creation(self, data_df, forecast_feature):
        """
        Prepare the exogenous variables based on whether its categorical or numerical and perform imputation
        Prepare the endogenous variable and perform imputation

        Args:
            data_df ([DataFrame]): DataFrame containing the full data
            forecast_feature ([Text]): The endogenous variable to be forecasted

        Returns:
            [DataFrame]: The time series, categorical exogenous dataframe, numerical endogenous dataframe, month-day-week dataframe
        """
        data_df = helper.sanity_check(data_df)
        exog_data_numerical, exog_data_categorical = pd.DataFrame(), pd.DataFrame()
        list_numeric_column = []
        list_categorical_column = []
        if (len(exog_column) != 0):
            for exog in exog_column:
                data_df, list_numeric_column, list_categorical_column = self.treatment_exog(
                    data_df, exog, list_numeric_column, list_categorical_column)
                list_categorical_column = [
                    item for sublist in list_categorical_column for item in sublist]
        else:
            pass

        ts = data_df
        ts["Timestamp"] = pd.to_datetime(ts[date_column])
        ts = ts.set_index('Timestamp')
        ts = ts.drop([date_column], axis=1)

        if (len(list_numeric_column) != 0):
            exog_data_numerical = ts.loc[:,
                                         ts.columns.isin(list_numeric_column)]
            ts = ts.drop(list_numeric_column, axis=1)
        if (len(list_categorical_column) != 0):
            exog_data_categorical = ts.loc[:, ts.columns.isin(
                list_categorical_column)]
            ts = ts.drop(list_categorical_column, axis=1)

        ts = ts.resample(resample).mean()
        ts = helper.imputation(ts, forecast_feature, 'endog')

        if (len(exog_data_numerical) != 0):
            exog_data_numerical = exog_data_numerical.ffill()
            exog_data_numerical = exog_data_numerical.astype(
                int).resample(resample).mean()
            for column in list_numeric_column:
                exog_data_numerical = helper.imputation(
                    exog_data_numerical, column, 'exog')
        if (len(exog_data_categorical) != 0):
            exog_data_categorical = exog_data_categorical.resample(
                resample).bfill()
            '''Handling Rare Levels'''
            total_length = len(exog_data_categorical)
            rare_levels = exog_data_categorical.agg(['sum'])/total_length
            exog_data_categorical['Others'] = 0
            for col in ((rare_levels.columns).to_list()):
                if (rare_levels[col]['sum'] <= constants.RARE_LEVEL_THRESHOLD):
                    exog_data_categorical['Others'] = np.where(
                        exog_data_categorical[col] == 1, 1, exog_data_categorical['Others'])
                    exog_data_categorical = exog_data_categorical.drop(
                        col, axis=1)

        exog_data_extracted = pd.DataFrame({'month': np.asarray(ts.index.month),
                                            'day': np.asarray(ts.index.day),
                                            'week': np.asarray(ts.index.week)}, index=ts.index)

        return ts, exog_data_numerical, exog_data_categorical, exog_data_extracted


class TimeSeriesForecaster(DataPrep):
    def __init__(self):
        pass

    def __repr__(self):
        return "A time series forecasting object!"

    def forecast(self, ts_data, forecast_feature, forecast_periods):
        try:
            """
            Input: TS series
            Output: Reverse Transformed Forecast Error
            """
            ts, exog_data_numerical, exog_data_categorical, exog_data_extracted = DataPrep.feature_creation(self,
                                                                                                            ts_data, forecast_feature)
            exog_data = pd.concat(
                [exog_data_numerical, exog_data_categorical, exog_data_extracted], axis=1)
            """
            Setting ReverseTransformedSeries variable to a default value which is set if there Modeling is performed on it
            """
            reversetransformedseries = constants.NO_TIMESERIES_FLAG

            """
            Checking Stationarity on the original series
            """

            ret_value = timeseries_stat_test.test_stationarity(ts)
            try:
                if (ret_value == 1):
                    logging.info(
                        "Timeseries has stationarity in the original series")
                    """"If stationary, then perform the if condition"""
                    final_series_for_modeling = pd.Series(ts[forecast_feature])
                    #final_series_for_modeling.index.freq = None
                    """predicted_timeseries: The variable for Forecast Error using Holt Winter Linear model"""
                    predicted_timeseries, predicted_training, rmse = timeseries_modeling.calculatingrmse(
                        final_series_for_modeling, forecast_periods, exog_data)
                    predicted_timeseries = pd.Series(
                        predicted_timeseries[forecast_feature], index=predicted_timeseries.index)
                    predicted_training = pd.Series(
                        predicted_training[forecast_feature], index=predicted_training.index)
                    """ReverseTransformedSeries has the predicted error for the next period """
                    reversetransformedseries = predicted_timeseries.iloc[-(
                        forecast_periods):]
                    predicted_training_reverse_transformed = predicted_training

                elif (ret_value == 0):
                    """
                                        if the original series is non-stationary then perform the transformations---> Stop at the function which acheieves stationarity--->
                    Perform Holt Winter Linear Modeling --> Get the forecastt error for the next period ---> 
                    Reverse Transform the transformed errors to bring back o original scale
                                        """

                    """Func_list: all transformations"""
                    func_list = [timeseries_transformations.log_transformation, timeseries_transformations.moving_average,
                                 timeseries_transformations.differencing, timeseries_transformations.differencing_second_order,
                                 timeseries_transformations.exponentially_weighted_moving_average]
                    reverse_func_dictionary = {'log_transformation': timeseries_reverse_transformations.log_transformation,
                                               'moving_average': timeseries_reverse_transformations.moving_average,
                                               'differencing': timeseries_reverse_transformations.differencing,
                                               'differencing_second_order': timeseries_reverse_transformations.differencing_second_order,
                                               'exponentially_weighted_moving_average': timeseries_reverse_transformations.exponentially_weighted_moving_average}

                    reverse_training_func_dictionary = {'log_transformation': timeseries_reverse_transformations.log_transformation_training,
                                                        'moving_average': timeseries_reverse_transformations.moving_average_training,
                                                        'differencing': timeseries_reverse_transformations.differencing_training,
                                                        'differencing_second_order': timeseries_reverse_transformations.differencing_second_order_training,
                                                        'exponentially_weighted_moving_average': timeseries_reverse_transformations.exponentially_weighted_moving_average_training}

                    for func in func_list:
                        func_name = str(func).split()[1]
                        final_series_for_modeling = func(ts)
                        exog_data_adjusted = exog_data[exog_data.index.isin(
                            final_series_for_modeling.index)]
                        original_timeseries = pd.Series(
                            ts[forecast_feature], index=ts.index)
                        predicted_training_reverse_transformed = []
                        try:
                            if(isinstance(final_series_for_modeling, bool) != True):
                                """Timseries Transformation is successful"""
                                return_value = timeseries_stat_test.test_stationarity(
                                    pd.DataFrame({forecast_feature: final_series_for_modeling}))
                                if (return_value == 1):
                                    """Transformed series is stationary"""
                                    logging.info(
                                        "Timeseries has stationarity in the first transformed series with function %s", func_name)
                                    """
                                    Perform Modeling using Holt Winter Linear
                                    Predict on the trained model for the training data
                                    """
                                    predicted_timeseries, predicted_training, rmse = timeseries_modeling.calculatingrmse(
                                        final_series_for_modeling, forecast_periods, exog_data_adjusted)
                                    predicted_timeseries = pd.Series(
                                        predicted_timeseries[forecast_feature], index=predicted_timeseries.index)
                                    predicted_training = pd.Series(
                                        predicted_training[forecast_feature], index=predicted_training.index)

                                    """reverse_the_predicted_func: call the timeseries_reverse_transformations module"""
                                    reverse_the_predicted_func = reverse_func_dictionary[func_name]
                                    """ReverseTransformedSeries: The forecast and reverse transformed error"""
                                    reversetransformedseries = reverse_the_predicted_func(
                                        predicted_timeseries, original_timeseries, forecast_periods)
                                    reverse_the_predicted_func = reverse_training_func_dictionary[
                                        func_name]
                                    predicted_training_reverse_transformed = reverse_the_predicted_func(
                                        predicted_training, original_timeseries)
                                    break
                        except Exception as my_error:
                            _, _, exc_tb = sys.exc_info()
                            logging.error(
                                "Issue for timeseries in output_creation module is %s at lineno %s", my_error, exc_tb.tb_lineno)
                return reversetransformedseries, predicted_training_reverse_transformed, rmse
            except Exception as my_error:
                _, _, exc_tb = sys.exc_info()
                logging.error(
                    "Return value error is : %s at lineno %s", my_error, exc_tb.tb_lineno)
                return False, False
        except Exception as my_error:
            _, _, exc_tb = sys.exc_info()
            logging.error(
                "Transformations cannot be done because %s: at line no %s", my_error, exc_tb.tb_lineno)
            return False, False

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import boxcox
from statsmodels.stats.stattools import jarque_bera, durbin_watson
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tsa import holtwinters

from datup.timeseries.timeseries_errors import (
    compute_mae,
    compute_maep,
    compute_mape,
    compute_mase,
    compute_rmse,
    compute_rmsep,
    compute_smape
)

from datup.io.dataio import (
    upload_log,
    delete_items,
    upload_model
)

class ExponentialSmoothing:

    def __init__(self,FREQ="W-SUN",H_STEPS=4,T_SEASONS=52,LAGS=104):
        self.FREQ = FREQ
        self.H_STEPS = H_STEPS
        self.T_SEASONS = T_SEASONS
        self.LAGS = LAGS

    def logger_debug(self,cls):
        cls.logger.debug(f'Init variables: Freq={self.FREQ},Seasons={self.T_SEASONS},Future steps={self.H_STEPS},Lags={self.LAGS}')

    def split_ts_train_test(
        self,
        timeseries,
    ):
        """
        Return a training and testing series
        
        THIS METHOD HAS BE TESTED

        Parameters
        ----------
            self: ExponentialSmoothing
                It is the object type ExponentialSmoothing 
            timeseries: Serie
                It is the Serie with which want to work

        :return: Return a train timeserie
        :rtype: Serie
        :return: Return a test timeserie
        :rtype: Serie

        Examples
        --------
        >>> import datup as dt
        >>> sm=dt.ExponentialSmoothing()
        >>> sm.split_ts_train_test(timeseries)        
        """
        try:        
            train_data = timeseries.values[:-self.H_STEPS]
            train_index = pd.to_datetime(timeseries.index[:-self.H_STEPS])
            train_index.freq = pd.tseries.frequencies.to_offset(self.FREQ)
            train_timeseries = pd.DataFrame(train_data, index=train_index, columns=['value'])
            test_data = timeseries.values[-self.H_STEPS:]
            test_index = pd.to_datetime(timeseries.index[-self.H_STEPS:])
            test_index.freq = pd.tseries.frequencies.to_offset(self.FREQ)
            test_timeseries = pd.DataFrame(test_data, index=test_index, columns=['value'])
        except IOError as error:
            print(f'Exception found: {error}')
            raise
        return train_timeseries, test_timeseries

    def transform_ts_offset(
        self,
        timeseries
    ):
        """
        Return a dataframe containing input timeseries adding the minimum value to the whole
        
        THIS METHOD HAS BE TESTED

        Parameters
        ----------
            self: ExponentialSmoothing
                It is the object type ExponentialSmoothing 
            timeseries: Serie
                It is the Serie with which want to work

        :return: The DataFrame returned contains the input timeseries
        :rtype: DataFrame
        :return: The minimum value to the whole
        :rtype: Float

        Examples
        --------
        >>> import datup as dt
        >>> sm=dt.ExponentialSmoothing()
        >>> sm.transform_ts_offset(timeseries)
        """
        try:
            values = []
            minimum = timeseries.iloc[:,0].min()
            offset = timeseries.iloc[:,0] + abs(minimum) + 1
            [values.append(v) for v in offset]
            idx = pd.to_datetime(timeseries.index)
            idx.freq = pd.tseries.frequencies.to_offset(self.FREQ)
            df_offset = pd.DataFrame(values, index=idx, columns=['value'])
        except IOError as error:
            print(f'Exception found: {error}')
            raise
        return df_offset, minimum

    def transform_ts_log(
        self,
        timeseries
    ):
        """
        Return a dataframe consisting of the input timeseries transformed using Box-Cox
        
        THIS METHOD HAS BE TESTED

        Parameters
        ----------
            self: ExponentialSmoothing
                It is the object type ExponentialSmoothing 
            timeseries: Serie
                It is the Serie with which want to work

        :return: The DataFrame returned contains the input timeseries transformed using Box-Cox
        :rtype: DataFrame
        :return: The first value
        :rtype: Float

        Examples
        --------
        >>> import datup as dt
        >>> sm=dt.ExponentialSmoothing()
        >>> sm.transform_ts_log(timeseries)
        """
        try:
            values = []
            transformed = np.log(timeseries.iloc[:,0])        
            [values.append(v) for v in transformed]
            idx = pd.to_datetime(timeseries.index)
            idx.freq = pd.tseries.frequencies.to_offset(self.FREQ)
            df_transformed = pd.DataFrame(values, index=idx, columns=['value'])
            first_value = df_transformed.iloc[0,0]
        except IOError as error:
            print(f'Exception found: {error}')
            raise
        return df_transformed, first_value

    def transform_ts_difference(
        self,
        timeseries
    ):
        """
        Return a dataframe consisting of the input timeseries differenced one shift
        
        THIS METHOD HAS BE TESTED
        
        Parameters
        ----------
            self: ExponentialSmoothing
                It is the object type ExponentialSmoothing 
            timeseries: Serie
                It is the Serie with which want to work

        :return: A dataframe consisting of the input timeseries differenced one shift
        :rtype: DataFrame

        Examples
        --------
        >>> import datup as dt
        >>> sm=dt.ExponentialSmoothing()
        >>> sm.transform_ts_difference(timeseries)        
        """
        try:
            values = []
            differenced = timeseries.iloc[:,0].diff().fillna(0)
            [values.append(v) for v in differenced]
            idx = pd.to_datetime(timeseries.index)
            idx.freq = pd.tseries.frequencies.to_offset(self.FREQ)
            df_differenced = pd.DataFrame(values, index=idx, columns=['value'])
        except IOError as error:
            print(f'Exception found: {error}')
            raise
        return df_differenced

    def transform_ts_log_difference_offset(
        self,
        timeseries
    ):
        """
        Return a timeseries transformed using log, dfferenced and offset
        
        THIS METHOD HAS BE TESTED
        
        Parameters
        ----------
            self: ExponentialSmoothing
                It is the object type ExponentialSmoothing 
            timeseries: Serie
                It is the Serie with which want to work

        :return: A timeseries transformed using log
        :rtype: Serie
        :return: The first value
        :rtype: Float
        :return: The minimum value to the whole
        :rtype: Float

        Examples
        --------
        >>> import datup as dt
        >>> sm=dt.ExponentialSmoothing()
        >>> sm.transform_ts_log_difference_offset(timeseries)
        """
        try:
            timeseries_log, first_value_log = self.transform_ts_log(timeseries)                
            timeseries_diff = self.transform_ts_difference(timeseries_log)        
            timeseries_off, min_value_off = self.transform_ts_offset(timeseries_diff)
        except IOError as error:
            print(f'Exception found: {error}')
            raise
        return timeseries_off, first_value_log, min_value_off

    def inverse_ts_offset(
        self,
        timeseries,
        minimum
    ):
        """
        Return a dataframe consisting of input timeseries transformed back from difference offset
        
        THIS METHOD HAS BE TESTED
        
        Parameters
        ----------
            self: ExponentialSmoothing
                It is the object type ExponentialSmoothing 
            timeseries: Serie
                It is the Serie with which want to work

        :return: A dataframe consisting of input timeseries transformed back from difference offset
        :rtype: DataFrame

        Examples
        --------
        >>> import datup as dt
        >>> sm=dt.ExponentialSmoothing()
        >>> sm.inverse_ts_offset(timeseries)
        """
        try:
            values = []
            inverse = timeseries.iloc[:,0] - abs(minimum)
            [values.append(v) for v in inverse]
            idx = pd.to_datetime(timeseries.index)
            idx.freq = pd.tseries.frequencies.to_offset(self.FREQ)
            df_inverse = pd.DataFrame(values, index=idx, columns=['value'])
        except IOError as error:
            print(f'Exception found: {error}')
            raise
        return df_inverse

    def inverse_ts_difference(
        self,
        differenced,
        first_value_log
    ):
        """
        Return a dataframe consisting of input timeseries transformed back from difference
        
        THIS METHOD HAS BE TESTED
        
        Parameters
        ----------
            self: ExponentialSmoothing
                It is the object type ExponentialSmoothing 
            timeseries: Serie
                It is the Serie with which want to work

        :return: A dataframe consisting of input timeseries transformed back from difference 
        :rtype: DataFrame

        Examples
        --------
        >>> import datup as dt
        >>> sm=dt.ExponentialSmoothing()
        >>> sm.inverse_ts_difference(timeseries)
        """
        try:
            values = []
            differenced.iloc[0,0] = first_value_log
            inverse = differenced.iloc[:,0].cumsum()
            [values.append(v) for v in inverse]
            idx = pd.to_datetime(differenced.index)
            idx.freq = pd.tseries.frequencies.to_offset(self.FREQ)
            df_inverse = pd.DataFrame(values, index=idx, columns=['value'])
        except IOError as error:
            print(f'Exception found: {error}')
            raise
        return df_inverse

    def inverse_ts_log(
        self,
        timeseries
    ):
        """
        Return a dataframe consisting of the input timeseries transformed back from Box-Cox
        
        THIS METHOD HAS BE TESTED
        
        Parameters
        ----------
            self: ExponentialSmoothing
                It is the object type ExponentialSmoothing 
            timeseries: Serie
                It is the Serie with which want to work

        :return: A dataframe consisting of the input timeseries transformed back from Box-Cox 
        :rtype: DataFrame

        Examples
        --------
        >>> import datup as dt
        >>> sm=dt.ExponentialSmoothing()
        >>> sm.inverse_ts_log(timeseries)        
        """
        try:
            values = []
            inverse = np.exp(timeseries.iloc[:,0])        
            [values.append(v) for v in inverse]
            idx = pd.to_datetime(timeseries.index)
            idx.freq = pd.tseries.frequencies.to_offset(self.FREQ)
            df_inverse = pd.DataFrame(values, index=idx, columns=['value'])
        except IOError as error:
            print(f'Exception found: {error}')
            raise
        return df_inverse

    def reverse_ts_log_difference_offset(
        self,
        timeseries,
        first_value_log,
        min_value_off
    ):
        """
        Return a timeseries reverse transformed from offset, differenced and log
        
        THIS METHOD HAS BE TESTED
        
        Parameters
        ----------
            self: ExponentialSmoothing
                It is the object type ExponentialSmoothing 
            timeseries: Serie
                It is the Serie with which want to work
            first_value_log: float
                This value is given by the transform_ts_log_difference_offset method
            min_value_off: float
                This value is given by the transform_ts_log_difference_offset method

        :return: A Serie reverse transformed from offset, differenced and log
        :rtype: Serie

        Examples
        --------
        >>> import datup as dt
        >>> sm=dt.ExponentialSmoothing()
        >>> sm.reverse_ts_log_difference_offset(timeseries,firs_value_log,min_value_off) 
        """
        try:
            timeseries_invoff = self.inverse_ts_offset(timeseries,min_value_off)
            timeseries_invdiff = self.inverse_ts_difference(timeseries_invoff,first_value_log)
            timeseries_invlog = self.inverse_ts_log(timeseries_invdiff)
        except IOError as error:
            print(f'Exception found: {error}')
            raise
        return timeseries_invlog

    def train_ann(
        self,
        timeseries,
        transform
    ):
        """
        Return the simple exponential smoothing with additive errors (ANN) object and performance metrics vector
        
        THIS METHOD HAS BE TESTED
        
        Parameters
        ----------
            self: ExponentialSmoothing
                It is the object type ExponentialSmoothing 
            timeseries: Serie
                It is the Serie with which want to work
            transform: bool
                The transform flag indicates if timeserie need be transformed if True then invoke the 
                transform_ts_log_difference_offset

        :return: A SimpleExpSmoothing object
        :rtype: holtwinters.SimpleExpSmoothing
        :return: A list with some model attributes including rmse, rmsep, mae, maep, mape, mase errors
        :rtype: List

        Examples
        --------
        >>> import datup as dt
        >>> sm=dt.ExponentialSmoothing()
        >>> sm.train_ann(timeseries,transform)
        """
        try:    
            if transform:
                model_name = 'ann-ht'
                timeseries, first_val, min_val  = self.transform_ts_log_difference_offset(timeseries)           
                model = holtwinters.SimpleExpSmoothing(timeseries.iloc[:,0]).fit(optimized=True)
                prediction = pd.DataFrame(model.fittedvalues, index=timeseries.index, columns=['value'])
                prediction = self.reverse_ts_log_difference_offset(prediction, first_val, min_val)                
            else: 
                model_name = 'ann-hw'      
                model = holtwinters.SimpleExpSmoothing(timeseries.iloc[:,0]).fit(optimized=True)
                prediction = pd.DataFrame(model.fittedvalues, index=timeseries.index, columns=['value']) 
            model_rmse = compute_rmse(timeseries, prediction)
            model_rmsep = compute_rmsep(timeseries, prediction)
            model_mae = compute_mae(timeseries, prediction)
            model_maep = compute_maep(timeseries, prediction)
            model_mase = compute_mase(timeseries, prediction)
            model_mape = compute_mape(timeseries, prediction)
            model_smape = compute_smape(timeseries, prediction)
            metrics = [model_name, model.aic, model.aicc, model.sse, model_rmse, model_rmsep, model_mae, model_maep, model_mape, model_smape, model_mase]        
        except IOError as error:
            print(f'Exception found: {error}')
            raise
        return model, metrics

    def train_aan(
        self,
        timeseries,
        transform
    ):
        """
        Return the Holt’s linear method with additive errors (AAN) object and performance metrics vector
        
        THIS METHOD HAS BE TESTED
        
        Parameters
        ----------
            self: ExponentialSmoothing
                It is the object type ExponentialSmoothing 
            timeseries: Serie
                It is the Serie with which want to work
            transform: bool
                The transform flag indicates if timeserie need be transformed if True then invoke the 
                transform_ts_log_difference_offset

        :return: A Holt object
        :rtype: holtwinters.Holt
        :return: A list with some model attributes including rmse, rmsep, mae, maep, mape, mase errors
        :rtype: List

        Examples
        --------
        >>> import datup as dt
        >>> sm=dt.ExponentialSmoothing()
        >>> sm.train_aan(timeseries,transform)        
        """
        try:
            if transform:
                model_name = 'aan-ht'
                timeseries, first_val, min_val  = self.transform_ts_log_difference_offset(timeseries)
                model = holtwinters.Holt(timeseries.iloc[:,0], exponential=True, damped=False).fit(optimized=True)
                prediction = pd.DataFrame(model.fittedvalues, index=timeseries.index, columns=['value'])
                prediction = self.reverse_ts_log_difference_offset(prediction, first_val, min_val)              
            else: 
                model_name = 'aan-hw'      
                model = holtwinters.Holt(timeseries.iloc[:,0], exponential=True, damped=False).fit(optimized=True)
                prediction = pd.DataFrame(model.fittedvalues, index=timeseries.index, columns=['value'])   
            model_rmse = compute_rmse(timeseries, prediction)
            model_rmsep = compute_rmsep(timeseries, prediction)
            model_mae = compute_mae(timeseries, prediction)
            model_maep = compute_maep(timeseries, prediction)
            model_mase = compute_mase(timeseries, prediction)
            model_mape = compute_mape(timeseries, prediction) 
            model_smape = compute_smape(timeseries, prediction)
            metrics = [model_name, model.aic, model.aicc, model.sse, model_rmse, model_rmsep, model_mae, model_maep, model_mape, model_smape, model_mase]       
        except IOError as error:
            print(f'Exception found: {error}')
            raise
        return model, metrics

    def train_adn(
        self,
        timeseries,
        transform
    ):
        """
        Return the Additive damped trend method (ADN) object and performance metrics vector
        
        THIS METHOD HAS BE TESTED
        
        Parameters
        ----------
            self: ExponentialSmoothing
                It is the object type ExponentialSmoothing 
            timeseries: Serie
                It is the Serie with which want to work
            transform: bool
                The transform flag indicates if timeserie need be transformed if True then invoke the 
                transform_ts_log_difference_offset

        :return: A Holt object
        :rtype: holtwinters.Holt
        :return: A list with some model attributes including rmse, rmsep, mae, maep, mape, mase errors
        :rtype: List

        Examples
        --------
        >>> import datup as dt
        >>> sm=dt.ExponentialSmoothing()
        >>> sm.train_adn(timeseries,transform)
        """
        try:    
            if transform:
                model_name = 'adn-ht'
                timeseries, first_val, min_val  = self.transform_ts_log_difference_offset(timeseries)     
                model = holtwinters.Holt(timeseries.iloc[:,0], exponential=True, damped=True).fit(optimized=True)
                prediction = pd.DataFrame(model.fittedvalues, index=timeseries.index, columns=['value'])
                prediction = self.reverse_ts_log_difference_offset(prediction, first_val, min_val)                
            else: 
                model_name = 'adn-hw'      
                model = holtwinters.Holt(timeseries.iloc[:,0], exponential=True, damped=True).fit(optimized=True)
                prediction = pd.DataFrame(model.fittedvalues, index=timeseries.index, columns=['value'])   
            model_rmse = compute_rmse(timeseries, prediction)
            model_rmsep = compute_rmsep(timeseries, prediction)
            model_mae = compute_mae(timeseries, prediction)
            model_maep = compute_maep(timeseries, prediction)
            model_mase = compute_mase(timeseries, prediction)
            model_mape = compute_mape(timeseries, prediction) 
            model_smape = compute_smape(timeseries, prediction)
            metrics = [model_name, model.aic, model.aicc, model.sse, model_rmse, model_rmsep, model_mae, model_maep, model_mape, model_smape, model_mase]       
        except IOError as error:
            print(f'Exception found: {error}')
            raise
        return model, metrics  

    def train_ana(
        self,
        timeseries,
        transform
    ):
        """
        Return the Error additive, none trend and seasonality additive (ANA) object and performance metrics 
        vector
        
        THIS METHOD HAS BE TESTED
        
        Parameters
        ----------
            self: ExponentialSmoothing
                It is the object type ExponentialSmoothing 
            timeseries: Serie
                It is the Serie with which want to work
            transform: bool
                The transform flag indicates if timeserie need be transformed if True then invoke the 
                transform_ts_log_difference_offset

        :return: A ExponentialSmoothing object
        :rtype: holtwinters.ExponentialSmoothing
        :return: A list with some model attributes including rmse, rmsep, mae, maep, mape, mase errors
        :rtype: List

        Examples
        --------
        >>> import datup as dt
        >>> sm=dt.ExponentialSmoothing()
        >>> sm.train_ana(timeseries,transform)
        """
        try:      
            if transform:
                model_name = 'ana-ht'
                timeseries, first_val, min_val  = self.transform_ts_log_difference_offset(timeseries)     
                model = holtwinters.ExponentialSmoothing(timeseries.iloc[:,0], seasonal_periods=self.T_SEASONS, trend=None, damped=False, seasonal='add').fit(use_boxcox=False)
                prediction = pd.DataFrame(model.fittedvalues, index=timeseries.index, columns=['value'])
                prediction = self.reverse_ts_log_difference_offset(prediction, first_val, min_val)              
            else: 
                model_name = 'ana-hw'      
                model = holtwinters.ExponentialSmoothing(timeseries.iloc[:,0], seasonal_periods=self.T_SEASONS, trend=None, damped=False, seasonal='add').fit(use_boxcox=False)
                prediction = pd.DataFrame(model.fittedvalues, index=timeseries.index, columns=['value'])   
            model_rmse = compute_rmse(timeseries, prediction)
            model_rmsep = compute_rmsep(timeseries, prediction)
            model_mae = compute_mae(timeseries, prediction)
            model_maep = compute_maep(timeseries, prediction)
            model_mase = compute_mase(timeseries, prediction)
            model_mape = compute_mape(timeseries, prediction) 
            model_smape = compute_smape(timeseries, prediction)
            metrics = [model_name, model.aic, model.aicc, model.sse, model_rmse, model_rmsep, model_mae, model_maep, model_mape, model_smape, model_mase]       
        except IOError as error:
            print(f'Exception found: {error}')
            raise
        return model, metrics

    def train_statespace_ana(
        self,
        timeseries,
        transform
    ):
        """
        Return the Error additive, none trend and seasonality additive (ANA) statespace object and performance 
        metrics vector
        
        THIS METHOD HAS BE TESTED
        
        Parameters
        ----------
            self: ExponentialSmoothing
                It is the object type ExponentialSmoothing 
            timeseries: Serie
                It is the Serie with which want to work
            transform: bool
                The transform flag indicates if timeserie need be transformed if True then invoke the 
                transform_ts_log_difference_offset

        :return: A ExponentialSmoothing object
        :rtype: statespace.ExponentialSmoothing
        :return: A list with some model attributes including rmse, rmsep, mae, maep, mape, mase errors
        :rtype: List

        Examples
        --------
        >>> import datup as dt
        >>> sm=dt.ExponentialSmoothing()
        >>> sm.train_statespace_ana(timeseries,transform)
        """
        try:
            if transform:
                model_name = 'ana-st'
                timeseries, first_val, min_val  = self.transform_ts_log_difference_offset(timeseries) 
                model = sm.tsa.statespace.ExponentialSmoothing(timeseries.iloc[:,0], seasonal=self.T_SEASONS, trend=None, damped_trend=False).fit(use_boxcox=False)
                prediction = pd.DataFrame(model.fittedvalues, index=timeseries.index, columns=['value'])
                prediction = self.reverse_ts_log_difference_offset(prediction, first_val, min_val)                
            else: 
                model_name = 'ana-ss'      
                model = sm.tsa.statespace.ExponentialSmoothing(timeseries.iloc[:,0], seasonal=self.T_SEASONS, trend=None, damped_trend=False).fit(use_boxcox=False)
                prediction = pd.DataFrame(model.fittedvalues, index=timeseries.index, columns=['value'])   
            model_rmse = compute_rmse(timeseries, prediction)
            model_rmsep = compute_rmsep(timeseries, prediction)
            model_mae = compute_mae(timeseries, prediction)
            model_maep = compute_maep(timeseries, prediction)
            model_mase = compute_mase(timeseries, prediction)
            model_mape = compute_mape(timeseries, prediction) 
            model_smape = compute_smape(timeseries, prediction)
            metrics = [model_name, model.aic, model.aicc, model.sse, model_rmse, model_rmsep, model_mae, model_maep, model_mape, model_smape, model_mase]        
        except IOError as error:
            print(f'Exception found: {error}')
            raise
        return model, metrics 

    def train_aaa(
        self,
        timeseries,
        transform
    ):
        """
        Return the Error additive, additive trend and seasonality additive (AAA) object and performance metrics 
        vector
        
        THIS METHOD HAS BE TESTED
        
        Parameters
        ----------
            self: ExponentialSmoothing
                It is the object type ExponentialSmoothing 
            timeseries: Serie
                It is the Serie with which want to work
            transform: bool
                The transform flag indicates if timeserie need be transformed if True then invoke the 
                transform_ts_log_difference_offset

        :return: A ExponentialSmoothing object
        :rtype: holtwinters.ExponentialSmoothing
        :return: A list with some model attributes including rmse, rmsep, mae, maep, mape, mase errors
        :rtype: List

        Examples
        --------
        >>> import datup as dt
        >>> sm=dt.ExponentialSmoothing()
        >>> sm.train_aaa(timeseries,transform)
        """
        try:
            if transform:
                model_name = 'aaa-ht'
                timeseries, first_val, min_val  = self.transform_ts_log_difference_offset(timeseries)   
                model = holtwinters.ExponentialSmoothing(timeseries.iloc[:,0], seasonal_periods=self.T_SEASONS, trend='add', damped=False, seasonal='add').fit(use_boxcox=False)
                prediction = pd.DataFrame(model.fittedvalues, index=timeseries.index, columns=['value'])
                prediction = self.reverse_ts_log_difference_offset(prediction, first_val, min_val)               
            else: 
                model_name = 'aaa-hw'      
                model = holtwinters.ExponentialSmoothing(timeseries.iloc[:,0], seasonal_periods=self.T_SEASONS, trend='add', damped=False, seasonal='add').fit(use_boxcox=False)
                prediction = pd.DataFrame(model.fittedvalues, index=timeseries.index, columns=['value'])   
            model_rmse = compute_rmse(timeseries, prediction)
            model_rmsep = compute_rmsep(timeseries, prediction)
            model_mae = compute_mae(timeseries, prediction)
            model_maep = compute_maep(timeseries, prediction)
            model_mase = compute_mase(timeseries, prediction)
            model_mape = compute_mape(timeseries, prediction) 
            model_smape = compute_smape(timeseries, prediction)
            metrics = [model_name, model.aic, model.aicc, model.sse, model_rmse, model_rmsep, model_mae, model_maep, model_mape, model_smape, model_mase]        
        except IOError as error:
            print(f'Exception found: {error}')
            raise
        return model, metrics 

    def train_statespace_aaa(
        self,
        timeseries,
        transform
    ):
        """
        Return the Error additive, additive trend and seasonality additive (ANA) statespace object and 
        performance metrics vector
        
        THIS METHOD HAS BE TESTED
        
        Parameters
        ----------
            self: ExponentialSmoothing
                It is the object type ExponentialSmoothing 
            timeseries: Serie
                It is the Serie with which want to work
            transform: bool
                The transform flag indicates if timeserie need be transformed if True then invoke the 
                transform_ts_log_difference_offset

        :return: A ExponentialSmoothing object
        :rtype: statespace.ExponentialSmoothing
        :return: A list with some model attributes including rmse, rmsep, mae, maep, mape, mase errors
        :rtype: List

        Examples
        --------
        >>> import datup as dt
        >>> sm=dt.ExponentialSmoothing()
        >>> sm.train_statespace_aaa(timeseries,transform)
        """
        try:
            if transform:
                model_name = 'aaa-st'
                timeseries, first_val, min_val  = self.transform_ts_log_difference_offset(timeseries)
                model = sm.tsa.statespace.ExponentialSmoothing(timeseries.iloc[:,0], seasonal=self.T_SEASONS, trend='add', damped_trend=False).fit(use_boxcox=False)
                prediction = pd.DataFrame(model.fittedvalues, index=timeseries.index, columns=['value'])
                prediction = self.reverse_ts_log_difference_offset(prediction, first_val, min_val)                
            else: 
                model_name = 'aaa-ss'      
                model = sm.tsa.statespace.ExponentialSmoothing(timeseries.iloc[:,0], seasonal=self.T_SEASONS, trend='add', damped_trend=False).fit(use_boxcox=False)
                prediction = pd.DataFrame(model.fittedvalues, index=timeseries.index, columns=['value'])   
            model_rmse = compute_rmse(timeseries, prediction)
            model_rmsep = compute_rmsep(timeseries, prediction)
            model_mae = compute_mae(timeseries, prediction)
            model_maep = compute_maep(timeseries, prediction)
            model_mase = compute_mase(timeseries, prediction)
            model_mape = compute_mape(timeseries, prediction) 
            model_smape = compute_smape(timeseries, prediction)
            metrics = [model_name, model.aic, model.aicc, model.sse, model_rmse, model_rmsep, model_mae, model_maep, model_mape, model_smape, model_mase]       
        except IOError as error:
            print(f'Exception found: {error}')
            raise
        return model, metrics

    def train_ada(
        self,
        timeseries,
        transform
    ):
        """
        Return the Error additive, damped trend and seasonality additive (ADA) object and performance metrics 
        vector
        
        THIS METHOD HAS BE TESTED
        
        Parameters
        ----------
            self: ExponentialSmoothing
                It is the object type ExponentialSmoothing 
            timeseries: Serie
                It is the Serie with which want to work
            transform: bool
                The transform flag indicates if timeserie need be transformed if True then invoke the 
                transform_ts_log_difference_offset

        :return: A ExponentialSmoothing object
        :rtype: holtwinters.ExponentialSmoothing
        :return: A list with some model attributes including rmse, rmsep, mae, maep, mape, mase errors
        :rtype: List

        Examples
        --------
        >>> import datup as dt
        >>> sm=dt.ExponentialSmoothing()
        >>> sm.train_ada(timeseries,transform)
        """
        try:      
            if transform:
                model_name = 'ada-ht'
                timeseries, first_val, min_val  = self.transform_ts_log_difference_offset(timeseries)  
                model = holtwinters.ExponentialSmoothing(timeseries.iloc[:,0], seasonal_periods=self.T_SEASONS, trend='add', damped=True, seasonal='add').fit(use_boxcox=False)
                prediction = pd.DataFrame(model.fittedvalues, index=timeseries.index, columns=['value'])
                prediction = self.reverse_ts_log_difference_offset(prediction, first_val, min_val)               
            else: 
                model_name = 'ada-hw'      
                model = holtwinters.ExponentialSmoothing(timeseries.iloc[:,0], seasonal_periods=self.T_SEASONS, trend='add', damped=True, seasonal='add').fit(use_boxcox=False)
                prediction = pd.DataFrame(model.fittedvalues, index=timeseries.index, columns=['value'])   
            model_rmse = compute_rmse(timeseries, prediction)
            model_rmsep = compute_rmsep(timeseries, prediction)
            model_mae = compute_mae(timeseries, prediction)
            model_maep = compute_maep(timeseries, prediction)
            model_mase = compute_mase(timeseries, prediction)
            model_mape = compute_mape(timeseries, prediction) 
            model_smape = compute_smape(timeseries, prediction)
            metrics = [model_name, model.aic, model.aicc, model.sse, model_rmse, model_rmsep, model_mae, model_maep, model_mape, model_smape, model_mase]      
        except IOError as error:
            print(f'Exception found: {error}')
            raise
        return model, metrics 

    def train_statespace_ada(
        self,
        timeseries,
        transform
    ):
        """
        Return the Error additive, damped trend and seasonality additive (ADA) statespace object and performance metrics 
        vector
        
        THIS METHOD HAS BE TESTED
        
        Parameters
        ----------
            self: ExponentialSmoothing
                It is the object type ExponentialSmoothing 
            timeseries: Serie
                It is the Serie with which want to work
            transform: bool
                The transform flag indicates if timeserie need be transformed if True then invoke the 
                transform_ts_log_difference_offset

        :return: A ExponentialSmoothing object
        :rtype: statespace.ExponentialSmoothing
        :return: A list with some model attributes including rmse, rmsep, mae, maep, mape, mase errors
        :rtype: List

        Examples
        --------
        >>> import datup as dt
        >>> sm=dt.ExponentialSmoothing()
        >>> sm.train_ada(timeseries,transform)
        """
        try:
            if transform:
                model_name = 'ada-st'
                timeseries, first_val, min_val  = self.transform_ts_log_difference_offset(timeseries)     
                model = sm.tsa.statespace.ExponentialSmoothing(timeseries.iloc[:,0], seasonal=self.T_SEASONS, trend='add', damped_trend=True).fit(use_boxcox=False)
                prediction = pd.DataFrame(model.fittedvalues, index=timeseries.index, columns=['value'])
                prediction = self.reverse_ts_log_difference_offset(prediction, first_val, min_val)                
            else: 
                model_name = 'ada-ss'      
                model = sm.tsa.statespace.ExponentialSmoothing(timeseries.iloc[:,0], seasonal=self.T_SEASONS, trend='add', damped_trend=True).fit(use_boxcox=False)
                prediction = pd.DataFrame(model.fittedvalues, index=timeseries.index, columns=['value'])   
            model_rmse = compute_rmse(timeseries, prediction)
            model_rmsep = compute_rmsep(timeseries, prediction)
            model_mae = compute_mae(timeseries, prediction)
            model_maep = compute_maep(timeseries, prediction)
            model_mase = compute_mase(timeseries, prediction)
            model_mape = compute_mape(timeseries, prediction) 
            model_smape = compute_smape(timeseries, prediction)
            metrics = [model_name, model.aic, model.aicc, model.sse, model_rmse, model_rmsep, model_mae, model_maep, model_mape, model_smape, model_mase]       
        except IOError as error:
            print(f'Exception found: {error}')
            raise
        return model, metrics

    def select_best_model(
        self,
        cls,
        eval_metric,
        *args
    ):
        """
        Return the model with the best performance
        
        THIS METHOD HAS BE TESTED
        
        Parameters
        ----------
            self: ExponentialSmoothing
                It is the object type ExponentialSmoothing 
            cls: Datup
                It is the object type Datup necessary to download using aws credentials and write the log. The 
                default folder for log is /tmp/
            eval_metric: str
                It is the metric which the model will be evaluated
            *args: List
                A serie of arguments that normally are the errors metrics names into a list

        :return: A List with an index and the name of the best model 
        :rtype: List
        :return: A list with the best error metrics perfomance
        :rtype: List

        Examples
        --------
        >>> import datup as dt
        >>> sm=dt.ExponentialSmoothing()
        >>> ins=dt.Datup()
        >>> sm.select_best_model(ins,eval_metric='metric',*args)
        """
        try:
            metrics = []
            [metrics.append(arg) for arg in args]
            df_metrics = pd.DataFrame(metrics, columns=['model', 'aic', 'aicc', 'sse', 'rmse', 'rmsep', 'mae', 'maep', 'mape', 'smape', 'mase'])
            df_metrics = df_metrics.fillna(99999)        
            best_model_idx = df_metrics.loc[:, eval_metric].idxmin(axis='columns')
            best_model = df_metrics.loc[best_model_idx, 'model']
            best_metrics = [df_metrics.loc[best_model_idx,'model'], df_metrics.loc[best_model_idx,'aic'], df_metrics.loc[best_model_idx,'aicc'], df_metrics.loc[best_model_idx,'rmse'], 
                            df_metrics.loc[best_model_idx,'rmsep'], df_metrics.loc[best_model_idx,'mae'], df_metrics.loc[best_model_idx,'mape'], df_metrics.loc[best_model_idx,'maep'], 
                            df_metrics.loc[best_model_idx,'smape'], df_metrics.loc[best_model_idx,'mase']]
            cls.logger.debug(df_metrics[['model', 'aicc', 'rmse', 'rmsep', 'mae', 'mape', 'smape', 'mase']])
            cls.logger.debug('Best model {name}: AIC={aic:.3f}, AICc={aicc:.3f}, SSE={sse:.3f}, RMSE={rmse:.3f}, RMSEP={rmsep:.3f}, MAE={mae:.3f}, MAEP={maep:.3f}, MAPE={mape:.3f}, SMAPE={smape:.3f}, MASE={mase:.3f}'\
                        .format(name=df_metrics.loc[best_model_idx,'model'], aic=df_metrics.loc[best_model_idx,'aic'], aicc=df_metrics.loc[best_model_idx,'aicc'],
                                sse=df_metrics.loc[best_model_idx,'sse'], rmse=df_metrics.loc[best_model_idx,'rmse'], rmsep=df_metrics.loc[best_model_idx,'rmsep'],
                                mae=df_metrics.loc[best_model_idx,'mae'], maep=df_metrics.loc[best_model_idx,'maep'], mape=df_metrics.loc[best_model_idx,'mape'], smape=df_metrics.loc[best_model_idx,'smape'], mase=df_metrics.loc[best_model_idx,'mase']))
        except IOError as error:
            cls.logger.exception(f'Exception found: {error}')
            raise 
        return best_model, best_metrics

    def upload_best_model(
        self,
        cls,        
        best_model,
        item_id,
        stage,
        *args,
        **kwargs
    ):
        """
        Return the model object with the best performance uploaded to the datalake
        
        THIS METHOD HAS BE TESTED
        
        Parameters
        ----------
            self: ExponentialSmoothing
                It is the object type ExponentialSmoothing 
            cls: Datup
                It is the object type Datup necessary to download using aws credentials and write the log. The 
                default folder for log is /tmp/            
            best_model: str
                Is the name of the best model given by select_best_model method
            item_id: str
                Is the path where item if found for delete the old one and replace it with the actual best model
            stage: str,
                It is the set of folders after the datalake to the file that is required to upload
            *args: List
                A serie of arguments that normally are the errors metrics names into a list
            **kwargs: List
                A serie of arguments that normally are the errors models into a list

        :return: Is the model object to upload
        :rtype: Object

        Examples
        --------
        >>> import datup as dt
        >>> sm=dt.ExponentialSmoothing()
        >>> ins=dt.Datup()
        >>> sm.upload_best_model(ins,best_model='model_name',item_id='item_id',stage='stage',*args,**kwargs)
        """
        try:
            delete_items(cls, stage, item_id)
            for model_name, model_obj in kwargs.items():
                if best_model == model_name:
                    upload_model(cls, model_obj, stage, item_id, model_name)
                    cls.logger.debug('{model} fitted complete timeseries and uploaded to datalake'.format(model=model_name))
                else:
                    'No valid model. Try again...'        
        except IOError as error:
            cls.logger.exception(f'Exception found: {error}')
            upload_log(cls,logfile=cls.log_filename, stage='output/logs')
            raise 
        return model_obj

    def compute_ets_residuals(
        self,
        cls,
        timeseries,
        model
    ):
        """
        Return a series listing the residuals of actual and fitted datapoints of ETS models
        
        THIS METHOD HAS BE TESTED
        
        Parameters
        ----------
            self: ExponentialSmoothing
                It is the object type ExponentialSmoothing 
            cls: Datup
                It is the object type Datup necessary to download using aws credentials and write the log. The 
                default folder for log is /tmp/
            timeseries: Serie
                It is the Serie with which want to work
            model: Object
                Is the model object returned by some holtwinters fitted method

        :return: Is a Serie of a resdiuals errors 
        :rtype: Serie

        Examples
        --------
        >>> import datup as dt
        >>> sm=dt.ExponentialSmoothing()
        >>> ins=dt.Datup()
        >>> sm.compute_ets_residuals(ins,timeseries,model)
        """
        try:        
            residuals = model.resid       
        except IOError as error:
            cls.logger.exception(f'Exception found: {error}')
            upload_log(cls,logfile=cls.log_filename, stage='output/logs')
            raise 
        return residuals

    def compute_forecast_intervals(
        self,
        cls,
        timeseries,
        forecast,
        model_name,
        model,
        confidence_pct
    ):
        """
        Return the forecast intervals for ETS model h steps
        
        THIS METHOD HAS BE TESTED
        
        Parameters
        ----------
            self: ExponentialSmoothing
                It is the object type ExponentialSmoothing
            cls: Datup
                It is the object type Datup necessary to download using aws credentials and write the log. The 
                default folder for log is /tmp/ 
            timeseries: Serie
                It is the Serie with which want to work
            forecast: Object
                It is the Serie forecasted
            model_name: str
                Is the name of the model
            model: Object
                Is the model object given by some holtwinters fitted method
            confidence_pct: Float
                Is a confidence interval to fit with the model

        :return: Is a computed interval
        :rtype: Serie

        Examples
        --------
        >>> import datup as dt
        >>> sm=dt.ExponentialSmoothing()
        >>> ins=dt.Datup()
        >>> sm.compute_forecast_intervals(ins,timeseries,forecast,model_name='model_name',model,confidence_pct)
        """
        try:    
            ci_upper = []
            ci_lower = []
            c = 0
            if confidence_pct == 60: factor = 0.84
            elif confidence_pct == 80: factor = 1.28
            elif confidence_pct == 95: factor = 1.96
            else: cls.logger.debug('Invalid confidence percentile. Please try again...')
            if model_name == 'ann-hw' or model_name == 'ann-ht':
                c = 0
                for idx, step in enumerate(forecast.iloc[:,0]):    
                    variance = np.var(list(timeseries.iloc[:,0])+list(forecast.iloc[:idx+1,0]))
                    if idx==0:
                        ci_upper.append(forecast.iloc[idx,0] + factor*np.sqrt(variance))
                        ci_lower.append(forecast.iloc[idx,0] - factor*np.sqrt(variance))
                    else:
                        alpha = model.params['smoothing_level']
                        c = c+alpha**2
                        ci_upper.append(forecast.iloc[idx,0] + factor*np.sqrt(variance*(1+c)))
                        ci_lower.append(forecast.iloc[idx,0] - factor*np.sqrt(variance*(1+c)))
                ci = pd.DataFrame(list(zip(ci_upper, ci_lower)), index=forecast.index, columns=['Pronostico Sup'+str(confidence_pct), 'Pronostico Inf'+str(confidence_pct)])
                
            elif model_name == 'aan-hw' or model_name == 'aan-ht':
                c = 0
                for idx, step in enumerate(forecast.iloc[:,0]):    
                    variance = np.var(list(timeseries.iloc[:,0])+list(forecast.iloc[:idx+1,0]))
                    if idx==0:
                        ci_upper.append(forecast.iloc[idx,0] + factor*np.sqrt(variance))
                        ci_lower.append(forecast.iloc[idx,0] - factor*np.sqrt(variance))
                    else:
                        alpha = model.params['smoothing_level']
                        beta = model.params['smoothing_slope']
                        c = c + (alpha + beta)**2
                        ci_upper.append(forecast.iloc[idx,0] + factor*np.sqrt(variance*(1 + c)))
                        ci_lower.append(forecast.iloc[idx,0] - factor*np.sqrt(variance*(1 + c)))
                ci = pd.DataFrame(list(zip(ci_upper, ci_lower)), index=forecast.index, columns=['Pronostico Sup'+str(confidence_pct), 'Pronostico Inf'+str(confidence_pct)])
            
            elif model_name == 'adn-hw' or model_name == 'adn-ht':
                c = 0
                phi = 0
                for idx, step in enumerate(forecast.iloc[:,0]):    
                    variance = np.var(list(timeseries.iloc[:,0])+list(forecast.iloc[:idx+1,0]))
                    if idx==0:
                        ci_upper.append(forecast.iloc[idx,0] + factor*np.sqrt(variance))
                        ci_lower.append(forecast.iloc[idx,0] - factor*np.sqrt(variance))
                    else:
                        alpha = model.params['smoothing_level']
                        beta = model.params['smoothing_slope']
                        phi = phi + model.params['damping_slope']**idx
                        c = c + (alpha + beta*phi)**2
                        ci_upper.append(forecast.iloc[idx,0] + factor*np.sqrt(variance*(1 + c)))
                        ci_lower.append(forecast.iloc[idx,0] - factor*np.sqrt(variance*(1 + c)))
                ci = pd.DataFrame(list(zip(ci_upper, ci_lower)), index=forecast.index, columns=['Pronostico Sup'+str(confidence_pct), 'Pronostico Inf'+str(confidence_pct)])
                
            elif model_name == 'ana-hw' or model_name == 'ana-ss' or model_name == 'ana-ht' or model_name == 'ana-st':
                c = 0
                for idx, step in enumerate(forecast.iloc[:,0]):    
                    variance = np.var(list(timeseries.iloc[:,0])+list(forecast.iloc[:idx+1,0]))
                    if idx==0:
                        ci_upper.append(forecast.iloc[idx,0] + factor*np.sqrt(variance))
                        ci_lower.append(forecast.iloc[idx,0] - factor*np.sqrt(variance))
                    else:
                        alpha = model.params['smoothing_level']
                        gamma = model.params['smoothing_seasonal']
                        c = c + (alpha + gamma)**2
                        ci_upper.append(forecast.iloc[idx,0] + factor*np.sqrt(variance*(1 + c)))
                        ci_lower.append(forecast.iloc[idx,0] - factor*np.sqrt(variance*(1 + c)))
                ci = pd.DataFrame(list(zip(ci_upper, ci_lower)), index=forecast.index, columns=['Pronostico Sup'+str(confidence_pct), 'Pronostico Inf'+str(confidence_pct)])
            
            elif model_name == 'aaa-hw' or model_name == 'aaa-ht':
                c = 0
                for idx, step in enumerate(forecast.iloc[:,0]):    
                    variance = np.var(list(timeseries.iloc[:,0])+list(forecast.iloc[:idx+1,0]))
                    if idx==0:
                        ci_upper.append(forecast.iloc[idx,0] + factor*np.sqrt(variance))
                        ci_lower.append(forecast.iloc[idx,0] - factor*np.sqrt(variance))
                    else:
                        alpha = model.params['smoothing_level']
                        beta = model.params['smoothing_slope']
                        gamma = model.params['smoothing_seasonal']
                        c = c + (alpha + beta + gamma)**2
                        ci_upper.append(forecast.iloc[idx,0] + factor*np.sqrt(variance*(1 + c)))
                        ci_lower.append(forecast.iloc[idx,0] - factor*np.sqrt(variance*(1 + c)))
                ci = pd.DataFrame(list(zip(ci_upper, ci_lower)), index=forecast.index, columns=['Pronostico Sup'+str(confidence_pct), 'Pronostico Inf'+str(confidence_pct)])
            
            elif model_name == 'aaa-ss' or model_name == 'aaa-st':
                c = 0
                for idx, step in enumerate(forecast.iloc[:,0]):    
                    variance = np.var(list(timeseries.iloc[:,0])+list(forecast.iloc[:idx+1,0]))
                    if idx==0:
                        ci_upper.append(forecast.iloc[idx,0] + factor*np.sqrt(variance))
                        ci_lower.append(forecast.iloc[idx,0] - factor*np.sqrt(variance))
                    else:
                        alpha = model.params['smoothing_level']
                        beta = model.params['smoothing_trend']
                        gamma = model.params['smoothing_seasonal']
                        c = c + (alpha + beta + gamma)**2
                        ci_upper.append(forecast.iloc[idx,0] + factor*np.sqrt(variance*(1 + c)))
                        ci_lower.append(forecast.iloc[idx,0] - factor*np.sqrt(variance*(1 + c)))
                ci = pd.DataFrame(list(zip(ci_upper, ci_lower)), index=forecast.index, columns=['Pronostico Sup'+str(confidence_pct), 'Pronostico Inf'+str(confidence_pct)])
                
            elif model_name == 'ada-hw' or model_name == 'ada-ht':
                phi = 0
                c = 0
                for idx, step in enumerate(forecast.iloc[:,0]):    
                    variance = np.var(list(timeseries.iloc[:,0])+list(forecast.iloc[:idx+1,0]))
                    if idx==0:
                        ci_upper.append(forecast.iloc[idx,0] + factor*np.sqrt(variance))
                        ci_lower.append(forecast.iloc[idx,0] - factor*np.sqrt(variance))
                    else:
                        alpha = model.params['smoothing_level']
                        beta = model.params['smoothing_slope']
                        phi = phi + model.params['damping_slope']**idx
                        gamma = model.params['smoothing_seasonal']
                        c = c + (alpha + beta*phi + gamma)**2
                        ci_upper.append(forecast.iloc[idx,0] + factor*np.sqrt(variance*(1 + c)))
                        ci_lower.append(forecast.iloc[idx,0] - factor*np.sqrt(variance*(1 + c)))
                ci = pd.DataFrame(list(zip(ci_upper, ci_lower)), index=forecast.index, columns=['Pronostico Sup'+str(confidence_pct), 'Pronostico Inf'+str(confidence_pct)])
            
            elif model_name == 'ada-ss' or model_name == 'ada-st':
                phi = 0
                c = 0
                for idx, step in enumerate(forecast.iloc[:,0]):    
                    variance = np.var(list(timeseries.iloc[:,0])+list(forecast.iloc[:idx+1,0]))
                    if idx==0:
                        ci_upper.append(forecast.iloc[idx,0] + factor*np.sqrt(variance))
                        ci_lower.append(forecast.iloc[idx,0] - factor*np.sqrt(variance))
                    else:
                        alpha = model.params['smoothing_level']
                        beta = model.params['smoothing_trend']
                        phi = phi + model.params['damping_trend']**idx
                        gamma = model.params['smoothing_seasonal']
                        c = c + (alpha + beta*phi + gamma)**2
                        ci_upper.append(forecast.iloc[idx,0] + factor*np.sqrt(variance*(1 + c)))
                        ci_lower.append(forecast.iloc[idx,0] - factor*np.sqrt(variance*(1 + c)))
                ci = pd.DataFrame(list(zip(ci_upper, ci_lower)), index=forecast.index, columns=['Pronostico Sup'+str(confidence_pct), 'Pronostico Inf'+str(confidence_pct)])
            else:
                print('No valid model. Try again...')  
        except IOError as error:
            cls.logger.exception(f'Exception found: {error}')
            raise
        return ci

    def ets_forecast(
        self,
        cls,
        timeseries,
        model_name,
        model,
        confidence
    ):
        """
        Return a series forecasting the specified steps using the input model
        
        THIS METHOD HAS BE TESTED
        
        Parameters
        ----------
            self: ExponentialSmoothing
                It is the object type ExponentialSmoothing
            cls: Datup
                It is the object type Datup necessary to download using aws credentials and write the log. The 
                default folder for log is /tmp/ 
            timeseries: Serie
                It is the Serie with which want to work
            model_name: str
                Is the name of the model
            model: Object
                Is the model object given by some holtwinters fitted method
            confidence: Float
                Is a forecast interval to fit with the model

        :return: A DataFrame with forecast
        :rtype: DataFrame
        :return: Is the frequence of intervals
        :rtype: Serie

        Examples
        --------
        >>> import datup as dt
        >>> sm=dt.ExponentialSmoothing()
        >>> ins=datup()
        >>> sm.ets_forecast(ins,timeseries, model_name='model_name', model, steps, confidence)
        """
        try:      
            prediction = model.forecast(steps=self.H_STEPS)              
            df_prediction = pd.DataFrame(prediction.values, index=prediction.index, columns=['Ctd Pronostico']) 
            if model_name[0][4:6] != 'hw' or model_name[0][4:6] != 'ss': 
                timeseries, first_value, min_value = self.transform_ts_log_difference_offset(timeseries)                    
                self.reverse_ts_log_difference_offset(df_prediction, first_value, min_value)                              
            forecast_intervals = self.compute_forecast_intervals(cls,timeseries, df_prediction, model_name[0], model, confidence_pct=confidence)                          
        except IOError as error:
            cls.logger.exception(f'Exception found: {error}')
            raise
        return df_prediction, forecast_intervals

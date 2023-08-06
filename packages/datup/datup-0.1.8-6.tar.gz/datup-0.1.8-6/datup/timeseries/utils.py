import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import grangercausalitytests
from statsmodels.tsa.stattools import adfuller

def format_timeseries(
    df,
    dateindex,
    item,
    kpi,
    freq
):
    """
    Return a dataframe with dates as index, items as dimensions and a kpi as records
    
    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        df: DataFrame
            It is the DataFrame with which want to work
        dateindex: str
            Is the column which contains dates
        item: str
            Is the column which contains the specific item
        kpi: str
            Is the column which contains values
        freq: str
            Is the frequency of the timeserie. Example: "D", "W", etc... 

    :return: Return a dataframe converted to a timeseries
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> datup = dt.Datup()
    >>> dt.format_timeseries(df,dateindex,item,kpi,freq)
    """
    try:
        df[item] = df[item].astype(str)        
        df_gp = df.groupby([item, dateindex], as_index=False).agg({kpi: sum})                
        df_pivot = df_gp.pivot_table(index=[dateindex], columns=item, values=kpi, fill_value=0).reset_index().rename_axis(None, axis='columns').set_index(dateindex).asfreq(freq)
        df_pivot = df_pivot.resample(freq).sum()        
    except IOError as error:
        print(f'Exception found: {error}')
        raise
    return df_pivot

def embedding_ts_delay(
    df_delay,
    lag,
    multi=False,
    sufix=None
):
    """
    Return a dataframe with its time delay embbeded
    
    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        df_delay: DataFrame
            It is the DataFrame with which want to work
        lag: int
            Is the number to create the dataframe delay as a LAG
        multi: bool, default False
            If multi is True, then a multiple timeseries in a single dataframe will be processed,
            the suffix name is required if multi is True
        sufix: str, default None
            Is the sufix to identify into the embbeded dataframe each timeserie. Just required if multi is True

    :return: Return a dataframe with the delay embbeded
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> datup = dt.Datup()
    >>> dt.embedding_ts_delay(df_delay,lag,multi=False,sufix=None)
    """
    try:
        df = pd.DataFrame()
        lag = lag-1
        for lag_ in range((lag-1),-1,-1):
            if lag_ == 0: df_temp = df_delay[(lag-1):]
            else: df_temp = df_delay[(lag-1)-lag_:-lag_]
            df = pd.concat([df_temp.reset_index(drop=True),df],axis=1)
            if multi: 
                if sufix is None: print(f"A suffix is needed to process the embbeded dataframe")
                else:
                    if df.shape[1] == lag: df = df.rename(columns={df.columns[0]:sufix+"_Xt"})
                    else: df = df.rename(columns={df.columns[0]:sufix+"_Xt-"+str(lag_)})
            else:
                if df.shape[1] == lag: df = df.rename(columns={df.columns[0]:"Xt"})
                else: df = df.rename(columns={df.columns[0]:"Xt-"+str(lag_)})
    except IOError as error:
        print(f'Exception found: {error}')
        raise
    return df

def autocorrelation_timeseries(
    timeseries,
    tau_lim
):
    """
    Return a dataframe with scores information about a timeserie autocorrelation
    
    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        timeseries: DataFrame
            It is the DataFrame with which want to work
        tau_lim: int
            Is the number until the autocorrelation would be calculated. Example: 365. The number could be
            refers to the 365 days in the year

    :return: Return a dataframe with the scores information about autocorrelation
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> datup = dt.Datup()
    >>> dt.autocorrelation_timeseries(timeseries,365)
    """
    try:
        corr = []
        for tau in range(1, tau_lim-1):
            unlagged = timeseries[:-tau]
            lagged = np.roll(timeseries, -tau)[:-tau]
            corr.append([pd.DataFrame(np.hstack((unlagged,lagged))).corr("pearson")[1][0],tau+1])
        df_scores = pd.DataFrame(corr,columns=["corr-score","lagperiods"])
        df_scores = df_scores.sort_values(by="corr-score",ascending=False).reset_index(drop=True)
    except IOError as error:
        print(f'Exception found: {error}')
        raise
    return df_scores

def causality_ts_granger(
    df,
    maxlag=8,
    method="ssr_chi2test"
):
    """
    Return a dataframe with the timeseries in cols and rows way where each row is the timeserie influenced by each column
    
    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        df: DataFrame
            It is the DataFrame with which want to work
        maxlag: int, default 8
            Is the LAG number to calculate the Granger Causality between timeseres
        method: str, default 'ssr_chi2test'
            The method to calculate the Granger Causality. Options avaiable are:
                *   params_ftest, based on F distribution
                *   ssr_ftest, based on F distribution
                *   ssr_chi2test, based on chi-square distribution
                *   lrtest, based on chi-square distribution

    :return: Return a dataframe with the scores information about Granger Causality
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> datup = dt.Datup()
    >>> dt.causality_ts_granger(df)
    """
    try:
        df_total_scores = pd.DataFrame()
        for cols_x in df.columns:
            x_list = [[round(grangercausalitytests(df[[cols_y,cols_x]], maxlag=maxlag, verbose=False)[1][0][method][1],4),cols_y+"_y"] for cols_y in df.columns]
            df_p_scores = pd.DataFrame(x_list, columns=[cols_x+"_x","pred"]).set_index("pred")
            df_total_scores = pd.concat([df_total_scores,df_p_scores],axis=1)
        df_total_scores
    except IOError as error:
        print(f'Exception found: {error}')
        raise
    return df_total_scores

def transform_log_plusone(
    timeseries
):
    """
    Return a timeserie with log(1+x) transformed
    
    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        timeseries: DataFrame
            It is the DataFrame with which want to work

    :return: Return a timeserie with log(1+x) transformed
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> datup = dt.Datup()
    >>> dt.transform_log_plusone(timeserie)
    """
    try:
        df = pd.DataFrame(np.log1p(timeseries.values),index=timeseries.index,columns=["values"])
        df.index = pd.to_datetime(df.index,format="%Y-%m-%d")
    except IOError as error:
        print(f'Exception found: {error}')
    return df

def inverse_log_plusone(
    timeseries
):
    """
    Return a timeserie with exp(x)-1 transformed
    
    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        timeseries: DataFrame
            It is the DataFrame with which want to work

    :return: Return a timeserie with exp(x)-1 transformed
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> datup = dt.Datup()
    >>> dt.inverse_log_plusone(timeserie)
    """
    try:
        df = pd.DataFrame(np.expm1(timeseries.values),index=timeseries.index,columns=["value"])
        df.index = pd.to_datetime(df.index,format="%Y-%m-%d")
    except IOError as error:
        print(f'Exception found: {error}')
    return df

def split_ts_train_test(
    timeseries,
    datemode=False,
    trainend=None,
    trainpsize=None
):
    """
    Return two DataFrames, for train and test.

    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        timeseries: DataFrame
            It is the DataFrame with which want to work
        datemode: Bool, default False
            If datemode is True, the train and test timeseries would be calculated in function of trainend parameter
            taking into account all timeserie. trainend parameter is required
        trainend: str, default None
            It is require if datemode is True. The format of the date is Y-m-d, example '2016-02-30'
        trainpsize: float, default None
            If datemode is False, trainpsize is require. Values accepted will be between 0-1

    :return: Return a timeserie with train values
    :rtype: DataFrame
    :return: Return a timeserie with test values
    :rtype: DataFrame 

    Examples
    --------
    >>> import datup as dt
    >>> datup = dt.Datup()
    >>> dt.split_ts_train_test(timeseries,trainpsize=0.7)
    """
    try:
        timeseries.index.name = "Date"
        timeseries_sorted = timeseries.sort_values(by="Date", ascending=True)
        if datemode and trainpsize is None and trainend is not None:
            if timeseries_sorted.index[0] > trainend or timeseries_sorted.shape[1] > 1 or timeseries_sorted.index[-1] < trainend:
                print("The last date of train couldn't be minor than the first date or major than the last date of the timeseries. The format of the date is Y-m-d") 
                print("The shape of the timeseries couldn't be major than one. Verify that the index contains dates and the single column contains values")
            else:      
                train_size = len(timeseries_sorted.loc[timeseries_sorted.index <= trainend])
                train_ts = timeseries_sorted.iloc[:train_size,:]
                test_ts = timeseries_sorted.iloc[train_size:,:]
        elif (datemode and trainpsize is not None and trainend is None) or (datemode and trainpsize is None and trainend is None) or (not datemode and trainpsize is None and trainend is not None):
            print("datemode only works with a valid trainend value and trainpsize in None mode")
        else:
            train_size = int(len(timeseries_sorted)*trainpsize)
            train_ts = timeseries_sorted.iloc[:train_size,:]
            test_ts = timeseries_sorted.iloc[train_size:,:]
    except IOError as error:
            print(f'Exception found: {error}')
    return train_ts, test_ts

def dickyfuller_ts_augmented(
    df,
    maxlag=None,
    regression="c",
    autolag="AIC",
    store=False,
    regresults=False,
    p_value=0.05
):
    """
    Return a DataFrame with Augmented Dicky Fuller's test to resolve if a timeserie is stationary or not

    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        df: DataFrame
            It is the DataFrame with which want to work
        maxlag: int, default None
            The maxlag parameter is the the maximum lag required for calculating stationality
        regression: str, default None
            Constant and trend order to include in regression.  
                *   'c': constant only (default).  
                *   'ct': constant and trend.  
                *   'ctt': constant, and linear and quadratic trend.  
                *   'nc': no constant, no trend.
        autolag: str, default 'AIC'
            Method to use when automatically determining the lag.
                *   if None, then maxlag lags are used.  
                *   if 'AIC' (default) or 'BIC', then the number of lags is chosen to minimize the corresponding information criterion.  
                *   't-stat' based choice of maxlag.  Starts with maxlag and drops a lag until the t-statistic on the last lag length is significant using a 5%-sized test.
        store: Bool, default False
            If True, then a result instance is returned additionally to the adf statistic. Default is False.  
        regresults: Bool, default False
            If True, the full regression results are returned. Default is False.
        p_value: float, default 0.05
            Is the significance value for rejecting or not the null hypothesis

    :return: Return a DataFrame with Augmented Dicky Fuller's test indicading if a timeseries is stationary or not
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> datup = dt.Datup()
    >>> dt.dickyfuller_ts_augmented(df)
    """
    try:
        stationary_list = []
        nostationary_list = []
        for column in df.columns:
            res = adfuller(df[column].values,maxlag=maxlag,regression=regression,autolag=autolag,store=store,regresults=regresults)
            if res[1] < p_value: stationary_list.append([column,res[1]])
            else: nostationary_list.append([column,res[1]])
        df_stationary = pd.concat([pd.DataFrame(stationary_list, columns=["timeseries","p-value"]),pd.DataFrame(nostationary_list, columns=["timeseries","p-value"])])
        df_stationary["stationality"] = df_stationary["p-value"].apply(lambda x: "Stationary" if x <= 0.05 else "Not stationary")
    except IOError as error:
        print(f"Exception found: {error}")
    return df_stationary

def pretrain_multi_rf(
    df,
    lags=8,
    timeserie_toforecast=None
):
    """
    Return a DataFrame with multivariate series time delay embbeded

    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        df: DataFrame
            It is the DataFrame with which want to work
        lags: int, default 8
            The number of lag to aggregate the delay matrix
        timeserie_toforecast: str, None
            Is the name of the timeserie to forecast. It orders the matrix DataFrame as required

    :return: Return a DataFrame with multivariate series time delay embbeded
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> datup = dt.Datup()
    >>> dt.pretrain_multi_rf(df)
    """
    try:
        df_total = pd.DataFrame()
        for column in df.columns:
            df_temp = embedding_ts_delay(pd.DataFrame(df[column]),lags,multi=True,sufix=str(column))
            if str(df[column].name) == timeserie_toforecast:
                df_main = df_temp.copy()
            df_total = pd.concat([df_temp,df_total],axis=1)
        df_prepared = pd.concat([df_main,df_total],axis=1)
    except IOError as error:
        print(f"Exception found: {error}")
    return df_prepared
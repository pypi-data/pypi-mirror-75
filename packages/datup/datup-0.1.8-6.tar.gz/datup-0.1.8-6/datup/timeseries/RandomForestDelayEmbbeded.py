from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import pandas as pd
import numpy as np
from datup.timeseries.timeseries_errors import (
    compute_mae,
    compute_maep,
    compute_mape,
    compute_mase,
    compute_rmse,
    compute_rmsep,
    compute_smape
)
from datup.timeseries.utils import (
    autocorrelation_timeseries,
    embedding_ts_delay,
    inverse_log_plusone
)

class RandomForestDelayEmbbeded:
    
    def __init__(self):
        self

    def pred_rf(
        self,
        df_embbeded,
        steps,
        model,
        lim_confidence=95      
    ):
        """
        Return a list with forecasted values using Random Forest Delay Embbeding
        
        THIS METHOD HAS BE TESTED

        Parameters
        ----------
            self: ExponentialSmoothing
                It is the object type ExponentialSmoothing
            df_embbeded: DataFrame
                It is the DataFrame provided by train_rf method necessary for create the steps ahead to forecast
            steps: int
                The steps ahead to forecast
            model: object
                Is the pickle model provided by train_rf method
            lim_confidence: int, default 95
                Is the percentile for to calculate the differents confidence limits 

        :return: Return a list with forecasted values using Random Forest Delay Embbeding
        :rtype: List
        :return: Return a list with forecasted values for the upper limit
        :rtype: List
        :return: Return a list with forecasted values for the lower limit
        :rtype: List

        Examples
        --------
        >>> import datup as dt
        >>> rf_u=dt.RandomForestDelayEmbbeded()
        >>> rf_u.pred_rf(df_embbeded,90,model)
        """
        try:
            pred_list = []
            lim_down = []
            lim_up = []
            for i in range(1,steps+1):
                if i == 1: pass  
                else:
                    df_embbeded = pd.concat([df_embbeded.iloc[1:,:1].reset_index(drop=True).rename(columns={"Xt"+str(i-1):"Xt+"+str(i)}),df_embbeded],axis=1)
                    df_embbeded = df_embbeded.iloc[:,:-1]  
                    X_test = df_embbeded.iloc[-1,1:]
                    print(f"Predicting {i} step ahead")
                X_test = df_embbeded.iloc[-1,1:]
                pred=model.predict(np.array([X_test]).reshape(1,-1))
                pred_list.append(pred[0])
                lim_down.append(np.percentile(pred_list, (100 - lim_confidence) / 2.))
                lim_up.append(np.percentile(pred_list,100 - (100 - lim_confidence) / 2.))
                df_embbeded.iloc[-1,:]=df_embbeded.iloc[-1,:].fillna(pred[0])
            lim_up = [pred_list[i] + lim_up[i] for i in range(steps)] 
            lim_down = [pred_list[i] - lim_up[i] for i in range(steps)]         
        except IOError as error:
            print(f"Exception found: {error}")
        return pred_list, lim_up, lim_down

    def train_rf(
        self,
        train_ts,
        test_ts,
        params,
        lags=8,
        autocorr=None,
        transform=None,
        autocorr_lag = False,
        multi=False
    ):
        """
        Return a pickle RandomForest model. The method doesn't need to be sepparated
        in X_train, X_test, y_train and y_test, the method suppose that the DataFrame
        incoming keeps Xt,Xt-1,Xt-n way provided by datup library's method, the embedding_ts_delay method
        
        THIS METHOD HAS BE TESTED

        Parameters
        ----------
            self: ExponentialSmoothing
                It is the object type ExponentialSmoothing
            train_ts: DataFrame
                Is the train DataFrame or timeserie
            test_ts: DataFrame
                Is the test DataFrame or timeserie
            params: dict
                The params parameter optimices the Randome Forest regressor performance
                The valid options are:
                    *   n_estimators: List, default [100,300,500,700,900,1200]
                    *   criterion: List, default ['mae','mse']
                    *   max_depth: List, default [None]
                    *   max_features: List, default ['auto']
            lags: int, default 8
                Is the number of lags if autocorr_lag flag is False, it creates from train_ts a DataFrame with lags-1 features
            autocorr: int, default None
                If autocorr flag is True, then, autocorr must be necessary. It calculates for timeserie the appropiate lag and create
                from train_ts the ideal lag calculated
            transform: str, default None
                Sometimes timeseries could be transformed, if transform is False the outcome timeserie keeps the its scale.
                The transforms availables are:
                    * 'inverse_log_plusone', This convert the income timeserie to a log(1+x) timeserie
            autocorr_lag: Bool, default False
                If autocorr is True, transform autocorr parameter is taken into account to calculate the embbeding delay
            multi: Bool, default False
                If multi is True, then, the train would be for a multivariate Random Forest Delay Time Embbedded DataFrame.

        :return: Return the embbeded DataFrame with the first step ahead Xt+1
        :rtype: DataFrame
        :return: Return a pickle object with a embbeded DataFrame trained by Random Forest
        :rtype: Object
        :return: Return a DataFrame with the calculated errors
        :rtype: DataFrame

        Examples
        --------
        >>> import datup as dt
        >>> rf_u=dt.RandomForestDelayEmbbeded()
        >>> rf_u.train_rf(df_train,df_test,params,8,transform="inverse_log_plusone")
        """
        try:    
            if autocorr_lag: 
                if multi: pass
                else: df = embedding_ts_delay(train_ts,autocorr)
                df_plusone = pd.concat([df.iloc[1:,:1].reset_index(drop=True).rename(columns={"Xt":"Xt+1"}),df],axis=1)
                df_scores = autocorrelation_timeseries(df_plusone,autocorr)      
            else: 
                if multi: pass
                else: df = embedding_ts_delay(train_ts,lags)
                df_plusone = pd.concat([df.iloc[1:,:1].reset_index(drop=True).rename(columns={"Xt":"Xt+1"}),df],axis=1)
                df_scores = autocorrelation_timeseries(df_plusone,lags)          
            y_train = df_plusone.iloc[:-1,:1]
            X_train = df_plusone.iloc[:-1,1:]
            rf = RandomForestRegressor(random_state=42)
            gs = GridSearchCV(rf, param_grid=params, n_jobs=-1)
            model = gs.fit(X_train,y_train)
            pred_list, lim_up, lim_down = self.pred_rf(df_plusone,len(test_ts),model)
            df_pred = pd.DataFrame(pred_list,index=test_ts.index, columns=["value"])
            if len(df_pred) == len(test_ts): 
                if transform is None: pass
                if transform == "inverse_log_plusone":
                    test_ts = inverse_log_plusone(test_ts)
                    df_pred = inverse_log_plusone(df_pred)
                mae = compute_mae(test_ts.reset_index(drop=True),df_pred.reset_index(drop=True))
                maep = compute_maep(test_ts.reset_index(drop=True),df_pred.reset_index(drop=True))
                mase = compute_mase(test_ts.reset_index(drop=True),df_pred.reset_index(drop=True))
                rmse = compute_rmse(test_ts.reset_index(drop=True),df_pred.reset_index(drop=True))
                rmsep = compute_rmsep(test_ts.reset_index(drop=True),df_pred.reset_index(drop=True))
                mape = compute_mape(test_ts.reset_index(drop=True),df_pred.reset_index(drop=True))
                smape = compute_smape(test_ts.reset_index(drop=True),df_pred.reset_index(drop=True))  
                print(f"MAE Error: {mae} - MAEP Error: {mape} - MASE Error: {mase} - RMSE Error: {rmse} - RMSEP Error: {rmsep} - MAPE Error: {mape} - sMAPE Error: {smape}")
                df_errors = pd.DataFrame([[df_scores["lagperiods"][0],df_scores["corr-score"][0],lags,mae,maep,mase,rmse,rmsep,mape,smape]],columns=["LAG-IDEAL","SCORE-LAG-IDEAL","LAG-CALCULADO","MAE","MAEP","MASE","RMSE","RMSEP","MAPE","sMAPE"])
            else: print(f"Test_ts and Forecast series must be to have the same shape test shape is {test_ts.shape} - forecast shape is {df_pred}") 
        except IOError as error:
            print(f'Exception found: {error}')
            raise
        return df_plusone, model, df_errors

  

    

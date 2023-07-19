#Import necessary libraries
import matplotlib.pyplot as plt
import seaborn as sn
import pandas as pd
import datetime as dt
import numpy as np
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

# Metrics
from sklearn.metrics import mean_absolute_error, mean_squared_error
# yfinance
import yfinance as yf

def get_dates(forecast):
    dates = []
    start_date = dt.date.today()
    for i in range(forecast):
        start_date += dt.timedelta(days=1)
        dates.append(start_date)
    return dates

def forecastPrices(days, code):
    # Previous 60 days data for training
    ndays = '60d'
    
    ticker = yf.Ticker(code)
    df = ticker.history(period=ndays) 
    df.reset_index(inplace=True)
    
    # Dataframe having Date and Closing price
    df = df[['Date', 'Close']]
    
    #Removing Timestamp from Date
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    
    forecast = days
    df['Prediction'] = df.Close.shift(-forecast)
    
    # Calculated dates of predicted prices
    idates = get_dates(forecast)
    
    #Closing price of with NaN predicted prices
    iclose = np.array(df['Close'][-forecast:]).reshape(-1,1)
    
    fdf = df.iloc[:-forecast]
    fdf = fdf.drop('Date', axis=1)
    
    # Barplot
    # plt.figure(figsize=(10,6))
    # sn.boxplot(fdf['Close'])
    # plt.show()
    # Q1 = fdf['Close'].quantile(.25)
    # Q3 = fdf['Close'].quantile(.75)
    # IQR = Q3 - Q1
    # fdf[(fdf['Close'] < Q1 - 1.5*IQR) | (fdf['Close'] > Q3 + IQR * 1.5)]
    
    x = np.array(fdf['Close'])
    x = x.reshape(-1,1)
    y = np.array(fdf['Prediction'])
    
    # Splitting dataset into training and testing
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.1)
    
    # Parmeter list of gridsearchCV
    parameter_list = {
        'C': [1, 10, 100, 1000, 10000],
        'gamma': [10, 1, .1, .01, .001, .0001]
    }
    
    # Hyperparameter tuning using GridSearchCV
    svrRbfModel = SVR(kernel='rbf')
    gridsvr = GridSearchCV(svrRbfModel, parameter_list, cv=None, scoring=['neg_mean_absolute_error', 'neg_mean_squared_error'], refit='neg_mean_absolute_error')
    gridsvr.fit(x_train, y_train)
    predictions = gridsvr.predict(iclose)
    predDict = {'Date': idates, 'Close': predictions}
    return pd.DataFrame(data=predDict)
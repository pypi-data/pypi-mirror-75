from Stock import *
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import datetime
import dateutil.relativedelta
import quandl
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np


def stockPredict(future: bool = False, companyName: str = 'AAPL', SVM: bool = True, LR: bool = True,
                 plot_getStock: bool = False, plot_stockPredict: bool = True, month: int = 12, test_size: int = 0.2,
                 svr_C: int = 1e3, svr_gamma: int = 0.1, confidence_test: bool = True):
    x = 0
    today = datetime.date.today()
    days = 30
    if not future:
        end = today - dateutil.relativedelta.relativedelta(days=x)
        df, mavg, start = getStock(companyName=companyName, month=month, plot=plot_getStock, end=end)
    elif future:
        end = today
        df, mavg, start = getStock(companyName=companyName, month=month, plot=plot_getStock)
    pred_num = days

    dayslist = []
    while x != pred_num:
        day = end + dateutil.relativedelta.relativedelta(days=x)
        dayslist.append(day)
        x += 1

    dates = np.array(dayslist)
    prediction_out = pred_num

    df['Prediction'] = df.shift(-prediction_out)
    print(df.tail())

    x = np.array(df.drop(['Prediction']))
    y = np.array(df["Prediction"])
    x = x[:-prediction_out]
    y = y[:-prediction_out]

    x = x.reshape(-1, 1)
    #y = y.reshape(-1, 1)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size)

    svr_rbf = SVR(kernel='rbf', C=svr_C, gamma=svr_gamma)
    svr_rbf.fit(x_train, y_train)

    x_forecast = np.array(df.drop(['Prediction']))[-prediction_out:]
    x_forecast = x_forecast.reshape(-1, 1)

    if not future:
        dfActual, mavgActual, startActual = getStock(companyName=companyName, month=month, plot=plot_getStock,
                                                     end=today, mavgPlot=False)
        print('ACTUAL: ')
        print(dfActual)

    if LR:
        lr = LinearRegression()
        lr.fit(x_train, y_train)

        lr_prediction = lr.predict(x_forecast)
        print('LR Prediction')
        print(lr_prediction)

        if plot_stockPredict:
            plt.plot(dates, lr_prediction)
            plt.title('Linear Regression')
            plt.show()

        if confidence_test:
            lr_confidence = lr.score(x_test, y_test)
            print("lr confidence: ", lr_confidence)
            dates = dates.tolist()
            lr_prediction = lr_prediction.tolist()
            return lr_confidence, lr_prediction, dates

        dates = dates.tolist()
        lr_prediction = lr_prediction.tolist()
        return lr_prediction, dates

    if SVM:
        svm_prediction = svr_rbf.predict(x_forecast)
        print('SVM Prediction')
        print(svm_prediction)


        if plot_stockPredict:
            plt.plot(dates, svm_prediction)
            plt.title('Support Vector Regression')
            plt.show()

        if confidence_test:
            svm_confidence = svr_rbf.score(x_test, y_test)
            print('SVM confidence is {}.'.format(svm_confidence))
            dates = dates.tolist()
            svm_prediction = svm_prediction.tolist()
            return svm_confidence, svm_prediction, dates

        dates = dates.tolist()
        svm_prediction = svm_prediction.tolist()
        return svm_prediction, dates

# TODO: Add iteration to find best settings with highest confidence rating

# import pandas
# from pandas import Series, DataFrame
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import datetime
import dateutil.relativedelta


def getStock(companyName: str, month: int = 1, plot: bool = False, end=datetime.date.today(), mavgPlot: bool = False):
    # set date for data retrieval
    window = 2 * month
    start = end - dateutil.relativedelta.relativedelta(months=int(month))

    # retrieve data from 'yahoo', type = 'Adj Close'
    df = web.DataReader(companyName, 'yahoo', start, end)['Adj Close']
    type(df)
    df.tail()
    mavg = df.rolling(window=window).mean()
    # label and plot chart
    df.plot(label=companyName)
    end -= dateutil.relativedelta.relativedelta(months=int(month))

    if plot:
        if mavgPlot:
            mavg.plot(label='mavg')
        plt.ylabel('Price')
        plt.xlabel('Year')
        plt.legend()
        plt.show()
    return df, mavg, start


#getStock(companyName='AAPL', plot=True, mavgPlot=False)

# Mean Reversions - Using that knowledge to recognise that if it is predicted to go up it will also go back down
# Unsupervised Learning
# PSO, LS-SVM, ANN LM,

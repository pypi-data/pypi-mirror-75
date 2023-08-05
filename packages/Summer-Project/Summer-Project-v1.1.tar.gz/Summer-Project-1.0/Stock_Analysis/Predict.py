from Stock import *
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import datetime
import dateutil.relativedelta
from sklearn import svm
import numpy as np

x = 0
df, mavg, start = getStock(companyName='AAPL', month=24, plot=True)
# print(df)

days = []
while x != 504:
    day = start + dateutil.relativedelta.relativedelta(days=x)
    days.append(int(day.strftime('%Y%m%d')))
    x += 1

dates = np.asarray(days)
dates = dates.reshape(252, 2)

clf = svm.SVC()
cDf = np.array(df)
# print(cDf)
cDf = cDf.reshape(252, 2, 1)

# carray = np.array([])
# while x != 1:
#    cDfTemp = cDf[x]
#    carray = cDfTemp.reshape(1, -1)
#    x -= 1
dates = dates.astype('int')
y = 0
while y != 251:
    clf.fit(cDf[y], dates[y])
    print('PREDICTION No. {}: '.format(y))
    print(clf.predict(cDf[y + 1]))
    yD2 = y / 2
    print('ACTUAL: ')
    if y % 2 == 0:
        print(cDf[int(yD2), 0])
    else:
        print(cDf[int(yD2), 1])
    print('')
    y += 1

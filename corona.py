import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
from CoronaParser import corona_parser
import pandas as pd



def sigmoid_and_delay(x, a, b, c):
    return b / (1.0 + np.exp(-a*(x+c)))

def sigmoid_without_delay(x, a, b):
    return b / (1.0 + np.exp(-a*x))

def fit_sigmoid_and_delay(xdata, ydata):
    starting_guesses = [0.2, 20000, -31]
    popt, pcov = curve_fit(sigmoid_and_delay, xdata, ydata, p0=starting_guesses)
    print(popt)
    plt.plot(xdata+int(popt[2]), ydata)
    plt.plot(xdata+int(popt[2]), sigmoid_and_delay(xdata, *popt))
    plt.title('Fitted sigmoid with 3 parameters')
    plt.xlabel('Days form tipping point')
    plt.show() 
    return popt

def fit_sigmoid_without_delay(xdata, ydata, delay):
    starting_guesses = [0.2, 20000]
    popt, pcov = curve_fit(sigmoid_without_delay, xdata+delay, ydata, p0=starting_guesses)
    #print(popt)
    plt.plot(xdata+delay, ydata)
    plt.plot(xdata+delay, sigmoid_without_delay(xdata+delay, *popt))
    plt.title('Fitted sigmoid with 2 parameters and delay= {delay}'.format(delay=delay))
    plt.xlabel('Days form tipping point')
    plt.show()
    return popt

country = 'Italy'
use_today = False
df = corona_parser(save_file=True, use_today=use_today)
#df = fix_duplicates(df)
italy = df[df['Country,Other']==country].sort_values(by='date')
italy_deaths = italy['deaths']
print(len(italy_deaths))
xdata = np.arange(len(italy_deaths))
xdata_pred = np.arange(len(italy_deaths)-1,len(italy_deaths)+30)
last_meassurement_day = italy['date'].max()
delay=-30

import pdb
pdb.set_trace()
fit_sigmoid_without_delay(xdata, italy_deaths, delay)
popt = fit_sigmoid_and_delay(xdata, italy_deaths)
print('Days to tipping point: {}'.format(-1*len(italy_deaths) - popt[2]))
daterange = [last_meassurement_day+datetime.timedelta(days=np.ceil(i)) for i in xdata+popt[2]]
daterange_pred = [last_meassurement_day+datetime.timedelta(days=np.ceil(i)) for i in xdata_pred+popt[2]]
fig, ax = plt.subplots()
ax.plot(daterange, italy_deaths)
ax.plot(daterange_pred, sigmoid_and_delay(xdata_pred, *popt), '--r')
fig.autofmt_xdate()
ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
plt.ylabel('cum deaths')
plt.title('Historical and prediction {country}'.format(country=country))
ax.legend(['Historical', 'Prediction'], loc='upper left')
plt.show()

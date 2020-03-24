import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
from CoronaParser import corona_parser
import pandas as pd

italy_deaths = [41,52,79,107,148,197,233,366,463,631,827,1016,1266,1441,1809,2158,2503,2978,3405,4032,4825,5476, 6077, 6820]
last_meassurement_day = datetime.date(2020,3,24)
xdata = np.arange(len(italy_deaths))
xdata_pred = np.arange(len(italy_deaths)-1,len(italy_deaths)+30)
delay=-30

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
    print(popt)
    plt.plot(xdata+delay, ydata)
    plt.plot(xdata+delay, sigmoid_without_delay(xdata+delay, *popt))
    plt.title('Fitted sigmoid with 2 parameters and delay= {delay}'.format(delay=delay))
    plt.xlabel('Days form tipping point')
    plt.show()
    return popt

df = corona_parser()
italy = df[df['Country,Other']=='Italy'].sort_values(by='date')
fit_sigmoid_without_delay(xdata, italy_deaths, delay)
popt = fit_sigmoid_and_delay(xdata, italy_deaths)

daterange = [last_meassurement_day+datetime.timedelta(days=np.ceil(i)) for i in xdata+popt[2]]
daterange_pred = [last_meassurement_day+datetime.timedelta(days=np.ceil(i)) for i in xdata_pred+popt[2]]
fig, ax = plt.subplots()
ax.plot(daterange, italy_deaths)
ax.plot(daterange_pred, sigmoid_and_delay(xdata_pred, *popt), '--r')
fig.autofmt_xdate()
ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
plt.ylabel('cum deaths')
plt.title('Historical and prediction italy')
ax.legend(['Historical', 'Prediction'], loc='upper left')
plt.show()

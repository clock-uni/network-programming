import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller

session1 = [89.2,
            133.6,
            146.2,
            143.8,
            141.4,
            162.1,
            167.5,
            168.1,
            162.4,
            171.7,
            195.1,
            208.3,
            190.6,
            207.1,
            222.4,
            205.9,
            229.3,
            241,
            270.7,
            304.3,
            346.9,
            368.5,
            385.6,
            479.8,
            421.6,
            ]
session2 = [123.4,
            143.2,
            140.8,
            149.5,
            163.6,
            163,
            158.5,
            167.8,
            181.6,
            196.3,
            205.9,
            203.8,
            200.2,
            216.7,
            222.7,
            226.6,
            250.9,
            271.3,
            307.9,
            347.8,
            370.6,
            387.4,
            413.5,
            420.7,
            419.6,
            ]

time = list(range(1997, 2022))


def logistic_increase_function(t, K, P0, r):
    t0 = 1997
    # t:time   t0:initial time    P0:initial_value    K:capacity  r:increase_rate
    exp_value = np.exp(r * (t - t0))
    return (K * exp_value * P0) / (K + (exp_value - 1) * P0)


fast_r = 0.40
slow_r = 0.64


def faster_logistic_increase_function(t, K, P0, ):
    return logistic_increase_function(t, K, P0, r=fast_r)


def slower_logistic_increase_function(t, K, P0, ):
    return logistic_increase_function(t, K, P0, r=slow_r)


def f(x, a, b):
    return a * np.exp(b * (x - 1997))


figure, axes = plt.subplots(nrows=1, ncols=2)
f_fit, f_conf = curve_fit(f, np.array(time), np.array(session1))
a, b = f_fit.tolist()
popt_fast, pcov_fast = curve_fit(faster_logistic_increase_function, time, session1)
popt_slow, pcov_slow = curve_fit(slower_logistic_increase_function, time, session1)
f_confirm = f(np.array(time), a, b)
fast_confirm = logistic_increase_function(np.array(time), popt_fast[0], popt_fast[1], r=slow_r)
slow_confirm = logistic_increase_function(np.array(time), popt_slow[0], popt_slow[1], r=slow_r)

model = AutoReg(session1, lags=1)
model_fit1 = model.fit()
yhat = model_fit1.predict(0, len(time) - 1)
model = ARIMA(session1, order=(0, 0, 1))
model_fit2 = model.fit()
yhat2 = model_fit2.predict(0, len(time) - 1)
model = ARIMA(session1, order=(1, 1, 1))
model_fit3 = model.fit()
yhat3 = model_fit3.predict(0, len(time) - 1)
axes[0].scatter(time, session1)
axes[0].plot(time, f_confirm, label='expmod')
axes[0].plot(time, fast_confirm, label='fast_logistic')
axes[0].plot(time, slow_confirm, label='slow_logistic')
axes[0].plot(time, yhat, label='AR')
axes[0].plot(time, yhat2, label='MA')
axes[0].plot(time, yhat3, label='ARIMA')
axes[0].set_title('Session1')
print('session1 exp predict:',f(2022, a, b))
print('session1 logistic predict:',logistic_increase_function(2022, popt_fast[0], popt_fast[1], r=slow_r))
print('session1 AR logistic predict:',model_fit1.predict(len(time),len(time)))
print('session1 MR logistic predict:',model_fit2.predict(len(time),len(time)))
print('session1 ARIMR logistic predict:',model_fit3.predict(len(time),len(time)))





f_fit, f_conf = curve_fit(f, np.array(time), np.array(session2))
a, b = f_fit.tolist()
popt_fast, pcov_fast = curve_fit(faster_logistic_increase_function, time, session2)
popt_slow, pcov_slow = curve_fit(slower_logistic_increase_function, time, session2)
f_confirm = f(np.array(time), a, b)
fast_confirm = logistic_increase_function(np.array(time), popt_fast[0], popt_fast[1], r=slow_r)
slow_confirm = logistic_increase_function(np.array(time), popt_slow[0], popt_slow[1], r=slow_r)

model = AutoReg(session2, lags=1)
model_fit = model.fit()
yhat = model_fit.predict(0, len(time) - 1)
model = ARIMA(session2, order=(0, 0, 1))
model_fit = model.fit()
yhat2 = model_fit.predict(0, len(time) - 1)
model = ARIMA(session2, order=(1, 1, 1))
model_fit = model.fit()
yhat3 = model_fit.predict(0, len(time) - 1)
axes[1].scatter(time, session2)
axes[1].plot(time, f_confirm, label='expmod')
axes[1].plot(time, fast_confirm, label='fast_logistic')
axes[1].plot(time, slow_confirm, label='slow_logistic')
axes[1].plot(time, yhat, label='AR')
axes[1].plot(time, yhat2, label='MA')
axes[1].plot(time, yhat3, label='ARIMA')
axes[1].set_title('Session2')
print('session2 exp predict:',f(2022, a, b))
print('session2 logistic predict:',logistic_increase_function(2022, popt_fast[0], popt_fast[1], r=slow_r))
print('session2 AR logistic predict:',model_fit1.predict(len(time),len(time)))
print('session2 MR logistic predict:',model_fit2.predict(len(time),len(time)))
print('session2 ARIMR logistic predict:',model_fit3.predict(len(time),len(time)))
axes[0].legend() #默认loc=Best
axes[1].legend()
plt.show()

figure, axes = plt.subplots(nrows=1, ncols=2)
model = ARIMA(session1, order=(1, 0, 1))
model_fit = model.fit()
yhat3 = model_fit.predict(0, len(time) - 1)
print('session1 ARMA logistic predict:',model_fit.predict(len(time),len(time)))
axes[0].scatter(time, session1)
axes[0].plot(time, yhat3, label='ARMA')
axes[0].legend() #默认loc=Best
model = ARIMA(session2, order=(1, 0, 1))
model_fit = model.fit()
yhat3 = model_fit.predict(0, len(time) - 1)
axes[1].scatter(time, session2)
axes[1].plot(time, yhat3, label='ARMA')
axes[1].legend() #默认loc=Best
axes[1].legend()
print('session2 ARMA logistic predict:',model_fit.predict(len(time),len(time)))
plt.show()
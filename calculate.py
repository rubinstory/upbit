import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly as py
import plotly.graph_objs as go
import requests
from keras.layers import *
from keras.models import *
from keras.callbacks import *
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
import pyupbit as upbit

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWeb\
            Kit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

access_key = 'UFcvGCeCy7NwwmIrDvxw0BCVxqqWbKiJgMHskv1C'
secret_key = '8rAk5yJao8waywxZztviffUbLkTd2LYWZs28Z5j7'
print(upbit.Upbit(access_key, secret_key).get_balances())

tickers = upbit.get_tickers()
coin_list = []



for comp in tickers :
    if (comp[:3] == 'KRW'):
        coin_list.append(comp)
print(coin_list)


coinName = "COSM"
url = 'https://crix-api-endpoint.upbit.com/v1/crix/candles/days?code=CRIX.UPBIT.KRW-' + coinName + '&count=500';

try:
    res = requests.get(url, headers=headers)
except requests.exceptions.HTTPError as err:
    print (err)
    exit(1)

data = reversed(res.json()) # json 구조로 변환

df = pd.DataFrame(data)
scaler = MinMaxScaler()
str_1 = 'tradePrice'

df[[str_1]] = scaler.fit_transform(df[[str_1]])
price = df[str_1].values.tolist()

window_size = 25

model = load_model('model.h5')
# model.h5 is a deep learning model, based on daily trade data.

new_value = []
new_value.append(price[-1])

for i in range(40) :
    new_array = [price[window_size * (-1) :]]
    new_array = np.asarray(new_array)
    new_array = new_array[window_size * (-1):, :]
    new_predict = new_array.reshape(new_array.shape[0], window_size, 1)
    new_predict = model.predict(new_predict)
    price.append(new_predict[-1][-1])

plt.figure(figsize=(10,10))
plt.plot(price[399:])
plt.savefig('graph.png', dpi=300)

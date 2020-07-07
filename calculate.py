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
import os

def get_prediction(coin_name) :
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWeb\
            Kit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    url = 'https://crix-api-endpoint.upbit.com/v1/crix/candles/days?code=CRIX.UPBIT.KRW-' + coin_name + '&count=400';
    
    try:
        res = requests.get(url, headers=headers)
    except requests.exceptions.HTTPError as err:
        print (err)
        exit(1)

    if(type(res.json()) is dict):
        return (0)
    data = reversed(res.json()) # json 구조로 변환
    df = pd.DataFrame(data)
    scaler = MinMaxScaler()
    str_1 = 'tradePrice'
    df[[str_1]] = scaler.fit_transform(df[[str_1]])
    price = df[str_1].values.tolist()
    #price = list(reversed(price))
    window_size = 10
    if(len(price) < 399):
        return (0)
    '''
    x = []
    y = []

    for i in range(len(price) - window_size) :
        x.append([price[i+j] for j in range(window_size)])
        y.append(price[window_size + i])

    x = np.asarray(x)
    y = np.asarray(y)

    train_test_split = int(len(price) * 0.75)

    x_train = x[:train_test_split, :]
    y_train = y[:train_test_split]

    x_test = x[train_test_split:, :]
    y_test = y[train_test_split :]

    x_train = x_train.reshape(x_train.shape[0], window_size, 1)
    x_test = x_test.reshape(x_test.shape[0], window_size, 1)
    
    model = Sequential()
    model.add(LSTM(128, input_shape = (10,1,)))
    model.add(Dropout(0.25))
    model.add(Dense(1, activation='linear'))
    model.compile(loss='mse', optimizer='adam')
    model.summary()

    model.fit(x_train, y_train, epochs = 500, verbose = 2)
    model.save('./model/' + coin_name + '.h5')
    '''
    
    model = load_model('./model/' + coin_name + '.h5')
    #model = load_model('./model/BTC.h5')
    # model.h5 is a deep learning model, based on daily trade data.
    #train_predict = model.predict(x_train)
    #test_predict = model.predict(x_test)
    
    new_value = []
    new_value.append(price[-1])

    prediction_num = 1
    for i in range(prediction_num) :
        new_array = [price[window_size * (-1) :]]
        new_array = np.asarray(new_array)
        new_array = new_array[window_size * (-1):, :]
        new_predict = new_array.reshape(new_array.shape[0], window_size, 1)
        new_predict = model.predict(new_predict)
        price.append(new_predict[-1][-1])

    price = [price]
    price = scaler.inverse_transform(price)
    price = price[0].tolist()

    '''
    plt.figure(figsize=(10,10))
    plt.plot(price[399:])
    
    split_pt = train_test_split + window_size
    plt.plot(np.arange(window_size, split_pt, ), train_predict, color='g')
    plt.plot(np.arange(split_pt, split_pt + len(test_predict), 1), test_predict, color='r')

    plt.savefig('./graph/' + coin_name + '.png', dpi=300)
    plt.close()
    '''
    
    tomorrow = len(price) - prediction_num
    today = tomorrow - 1
    #print((price[tomorrow] - price[today]) / price[tomorrow] * 100)
    return ((price[tomorrow] - price[today]) / price[tomorrow] * 100)

access_key = 'UFcvGCeCy7NwwmIrDvxw0BCVxqqWbKiJgMHskv1C'
secret_key = '8rAk5yJao8waywxZztviffUbLkTd2LYWZs28Z5j7'
#print(upbit.Upbit(access_key, secret_key).get_balances())

path = './model'
coin_list = os.listdir(path)
predict_list = []

for comp in coin_list:
    coin_name = comp[:-3]
    predict_list.append([coin_name, get_prediction(coin_name)])

predict_dict = dict(predict_list)
predict_dict = sorted(predict_dict.items(), key=lambda x: x[1], reverse=True)
print(predict_dict)
    
    



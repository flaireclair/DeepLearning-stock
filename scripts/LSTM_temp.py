# このまま実行してください
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error


# データセットの作成
def create_dataset(dataset, look_back):
    data_X, data_Y = [], []
    for i in range(look_back, len(dataset)):
        data_X.append(dataset[i-look_back:i, 0])
        data_Y.append(dataset[i, 0])
    return np.array(data_X), np.array(data_Y)

# データセットの読み込み
dataframe = pd.read_csv('./sales_forecast_data/monthly-champagne-sales-in-1000s.csv',usecols=[1], engine='python', skipfooter=3)
dataset = dataframe.values
dataset = dataset.astype('float32')

# トレーニングデータ、テストデータに分ける
train_size = int(len(dataset) * 0.67)
train, test = dataset[0:train_size, :], dataset[train_size:len(dataset), :]

# データのスケーリング
scaler = MinMaxScaler(feature_range=(0, 1))
scaler_train = scaler.fit(train)
train = scaler_train.transform(train)
test = scaler_train.transform(test)

# データの作成
look_back = 10
train_X, train_Y = create_dataset(train, look_back)
test_X, test_Y = create_dataset(test, look_back)

# データの整形
train_X = train_X.reshape(train_X.shape[0], train_X.shape[1], 1)
test_X = test_X.reshape(test_X.shape[0], test_X.shape[1], 1)

# LSTMモデルの作成と学習
model = Sequential()
model.add(LSTM(64, return_sequences=True, input_shape=(look_back, 1)))
model.add(LSTM(32))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(train_X, train_Y, epochs=15, batch_size=1, verbose=2)

# 予測データの作成
train_predict = model.predict(train_X)
test_predict = model.predict(test_X)

# スケールしたデータを元に戻す
train_predict = scaler_train.inverse_transform(train_predict)
train_Y = scaler_train.inverse_transform([train_Y])
test_predict = scaler_train.inverse_transform(test_predict)
test_Y = scaler_train.inverse_transform([test_Y])

# 予測精度の計算
train_score = math.sqrt(mean_squared_error(train_Y[0], train_predict[:, 0]))
print('Train Score: %.2f RMSE' % (train_score))
test_score = math.sqrt(mean_squared_error(test_Y[0], test_predict[:, 0]))
print('Test Score: %.2f RMSE' % (test_score))

# プロットのためのデータ整形
train_predict_plot = np.empty_like(dataset)
train_predict_plot[:, :] = np.nan
train_predict_plot[look_back:len(train_predict)+look_back, :] = train_predict
test_predict_plot = np.empty_like(dataset)
test_predict_plot[:, :] = np.nan
test_predict_plot[len(train_predict)+(look_back*2):len(dataset), :] = test_predict

# テストデータのプロット
plt.title("monthly-champagne-sales-in-1000s")
plt.xlabel("time(month)")
plt.ylabel("Earnings")
plt.plot(dataframe[round(len(dataset)*0.67):], label='train_data')
plt.plot(test_predict_plot, label='test_data')

plt.legend(loc='lower right')
plt.show()

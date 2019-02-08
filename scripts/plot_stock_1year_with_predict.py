# 1. パッケージインポート
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import newaxis
import math
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers.recurrent import SimpleRNN, LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
plt.style.use('ggplot')

while True :
    print('\n表示したい銘柄番号（東証一部）を入力してね！（終了は0）')
    brand_num = input('>> ')

    if brand_num == '0' :
        print('\n終了します')
        exit()
        
    # 2. ファイル読み込み
    index = [no for no in range(9)]
    is_already_index = False
    while index != []:
        try :
            if is_already_index :
                df_stock.append(pd.read_csv("../stock_data/201{0}_tousyou1bu_all/only_closing_stock_data_with_date/stock_data_with_date_{1}.csv".format(str(index[0]), brand_num)))
            else :
                df_stock = pd.read_csv("../stock_data/201{0}_tousyou1bu_all/only_closing_stock_data_with_date/stock_data_with_date_{1}.csv".format(str(index[0]), brand_num))
                is_already_index = True
        except :
            continue
        finally :
            del index[0]

    if is_already_index == False :
        print("\n正しい銘柄番号を入力してください")
        continue
    
    # 3. データの確認
    # sort_values メソッドで ソート
    df_stock['date'] = pd.to_datetime(df_stock['date'])
    df_stock.sort_values(by='date', inplace=True)
    
    # Date を indexに入れて可視化する
    df_stock.set_index('date', inplace=True)
    
    close_ts = df_stock['closing price']
    # 4. window_sizeに分けて時系列データのデータセットを作成
    
    
    def split_window_data(np_array, window_size, normalization=False, window_normalization=False):
        target_array = np_array.copy()
        # 全体に正規化をかける
        if normalization:
            scaler = MinMaxScaler(feature_range=(0, 1))
            target_array = scaler.fit_transform(target_array)
        # データを wowindow_sizeごとに分割
        sequence_length = window_size + 1
        window_data = []
        for index in range(len(target_array) - window_size):
            window = target_array[index: index + sequence_length]
            # windowごとに正規化をかける
            if window_normalization:
                window = [((float(p) / float(window[0])) - 1) for p in window]
            window_data.append(window)
        return window_data
    
    
    window_size = 60
    window_data = split_window_data(
        close_ts, window_size, normalization=False, window_normalization=True)
    # 5. トレーニングデータとテストデータに分ける
    print("window_data : {}".format(window_data))
    
    def split_train_test_window(np_array_window, window_size, train_rate, train_shuffle=False):
        window_data = np_array_window.copy()
        # (1218, 16)のデータの7割、つまり(852, 16)のデータをトレーニングデータにして分割
        row = round(train_rate * window_data.shape[0])
        # 0 ~ 852 番目までの、window　データを取り出す。
        train = window_data[0:row, :]
        # 16の時系列データのうち、最初の15個を説明変数 x とし、最後の16番目のデータを予測対象 y とする
        x_train = train[:, :-15]
        y_train = train[:, -15:]
        # 852 ~ 最後までの配列を取り出し、テストデータとする
        test = window_data[row:, ]
        x_test = test[:, :-15]
        y_test = test[:, -15]
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        return x_train, y_train, x_test, y_test
    
    train_rate = 0.7
    window_data = np.array(window_data)
    X_train, Y_train, X_test, Y_test = split_train_test_window(window_data, train_rate=train_rate, window_size=window_size, train_shuffle=True)
    #print("X_train : {0}\n Y_train : {1}\n X_test : {2}\n Y_test : {3}\n".format(X_train, Y_train, X_test, Y_test))
    # 6. モデルの作成
    # 入力サイズ
    inpiut_size = [X_train.shape[1], X_train.shape[2]]
    # レイヤーを定義
    model = Sequential()
    model.add(LSTM(input_shape=(inpiut_size[0], inpiut_size[1]),
                   units=60, return_sequences=False))
    model.add(Dense(units=15))
    model.add(Activation('linear'))
    model.compile(loss='mse', optimizer='adam')
    history = model.fit(X_train, Y_train, batch_size=200,
                        epochs=10, validation_split=0.1, verbose=2)
    
    # -------------------- 学習の過程を可視化する --------------------
    # 損失関数の推移図を出力
    plt.figure(figsize=(8, 5))
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    
    # -------------------- 未来の3ヶ月の消費者物価指数を予測してみる --------------------
    prediction_seqs = []
    prediction_len = 15
    
    for i in range(int(len(X_test)/prediction_len)):
        curr_frame = X_test[i*prediction_len]
        predicted = []
        
        for j in range(prediction_len):
            # 予測をしてください
            pred = model.predict(curr_frame[:,:,newaxis])
            #print(pred)
            for k in range(15) :
                predicted.append(pred[0, k])
            #print(predicted)
            curr_frame = curr_frame[1:, :]
            #print(predicted[-15])
            for l in range(15) :
                curr_frame = np.insert(curr_frame, window_size - 15 + l,
                                   predicted[-15 + l], axis=0)
        prediction_seqs.append(predicted)
    # 予測結果の出力
    plt.figure(figsize=(18, 10))
    plt.plot(Y_test, label='True Data')
    plt.plot(np.array(prediction_seqs).flatten().tolist(), label='Prediction')
    plt.title('predict')
    plt.legend()
    plt.show()
    

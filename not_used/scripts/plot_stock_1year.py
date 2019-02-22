# 1. パッケージインポート
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
plt.style.use('ggplot')

while True :
    print('表示したい銘柄番号（東証一部）を入力してね！（終了は0）')
    brand_num = input('>> ')

    if brand_num == '0' :
        print('終了します')
        exit()
    
    # 2. ファイル読み込み
    df_stock = pd.read_csv(
        "../stock_data/2018_tousyou1bu_all/stock_data_with_date_{}.csv".format(brand_num))

    # 3. データの確認
    # sort_values メソッドで ソート
    df_stock['date'] = pd.to_datetime(df_stock['date'])
    df_stock.sort_values(by='date', inplace=True)
    
    # Date を indexに入れて可視化する
    df_stock.set_index('date', inplace=True)
    
    close_ts = df_stock['closing price']
    close_ts.plot()
    plt.show()
    
    # 4. window_sizeに分けて時系列データのデータセットを作成
    
    
    def split_window_data(np_array, window_size, normalization=False, window_normalization=False):
        
        target_array = np_array.copy()
        
        # 全体に正規化をかける
        if normalization:
            # 正規化を行ってください
            scaler = MinMaxScalar(feature_range=(0,1))
            target_array = scaler.fit_transform(target_array)

        # データを window_sizeごとに分割
        sequence_length = window_size + 1
        window_data = []
        for index in range(len(target_array) - window_size):
            window = target_array[index: index + sequence_length]
            
            # windowごとに正規化をかける
            if window_normalization:
                window = [((float(p) / float(window[0])) - 1) for p in window]
                
            window_data.append(window)
            
        return window_data
    
    
    window_size = 15
    window_data = split_window_data(
        close_ts, window_size, normalization=False, window_normalization=True)

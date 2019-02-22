# サポートベクターマシーンのimport
from sklearn import svm
# train_test_splitのimport
from sklearn.model_selection import train_test_split
# accuracy_scoreのimport
from sklearn.metrics import accuracy_score
# Pandasのimport
import pandas as pd
# Numpyのimport
import numpy as np
# グリッドサーチのimport
from sklearn.model_selection import GridSearchCV

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import mutual_info_classif
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import RandomForestClassifier

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler

import get_last_working_day as lwd

def shapeCsv(brand_num,isTestdata):
    
    modified_data = np.zeros((0,6))
    if(isTestdata):
        # 株価の上昇率を算出、おおよそ-1.0～1.0の範囲に収まるように調整
        
        for i in range(1,4):
            stock_data = pd.read_csv("../stock_data/adopted_nikkeiheikin/"+ str(2015 + i) + "/all_stock_data_with_date/all_stock_data_with_date_"+ str(brand_num) +".csv", encoding="shift-jis")
            tmp_range = len(stock_data)

            for i in range(2,tmp_range):
                modified_data = np.append(
                modified_data,
                np.array([[(float(stock_data.iat[i,2]) - float(stock_data.iat[i-1,2]))/float(stock_data.iat[i-1,2]),
                            (float(stock_data.iat[i,3]) - float(stock_data.iat[i-1,3]))/float(stock_data.iat[i-1,3]),
                            (float(stock_data.iat[i,4]) - float(stock_data.iat[i-1,4]))/float(stock_data.iat[i-1,4]),
                            (float(stock_data.iat[i,5]) - float(stock_data.iat[i-1,5]))/float(stock_data.iat[i-1,5]),
                            (float(stock_data.iat[i,6]) - float(stock_data.iat[i-1,6]))/float(stock_data.iat[i-1,6]),
                            (float(stock_data.iat[i,7]) - float(stock_data.iat[i-1,7]))/float(stock_data.iat[i-1,7])]]),
                axis = 0)

        return modified_data

    else:
        stock_data = pd.read_csv("../stock_data/adopted_nikkeiheikin/2019/all_stock_data_with_date/all_stock_data_with_date_"+ str(brand_num) +".csv",encoding="shift-jis")
        tmp_range  = len(stock_data)

        for i in range(2,tmp_range):
            modified_data = np.append(
            modified_data, 
            np.array([[(float(stock_data.iat[i,2]) - float(stock_data.iat[i-1,2]))/float(stock_data.iat[i-1,2]),
                        (float(stock_data.iat[i,3]) - float(stock_data.iat[i-1,3]))/float(stock_data.iat[i-1,3]),
                        (float(stock_data.iat[i,4]) - float(stock_data.iat[i-1,4]))/float(stock_data.iat[i-1,4]),
                        (float(stock_data.iat[i,5]) - float(stock_data.iat[i-1,5]))/float(stock_data.iat[i-1,5]),
                        (float(stock_data.iat[i,6]) - float(stock_data.iat[i-1,6]))/float(stock_data.iat[i-1,6]),
                        (float(stock_data.iat[i,7]) - float(stock_data.iat[i-1,7]))/float(stock_data.iat[i-1,7])]]),
            axis = 0)
        return modified_data

def getData(brand_num):

    modified_data = shapeCsv(brand_num,True)

    # 要素数の設定
    count_m = len(modified_data)
    #print(modified_data[count_m-1])
    #print(modified_data) 

    # 最終日のデータを削除
    successive_data = np.delete(modified_data ,count_m - 1, axis=0)

    # データの正規化        
    ms = MinMaxScaler()
    ms.fit(successive_data)
    successive_data = ms.transform(successive_data)

    # データの標準化
    sc = StandardScaler()
    sc.fit(successive_data)
    successive_data = sc.transform(successive_data)

    # 正解値を格納するリスト　価格上昇: 1 価格低下:0
    answers = []

    # 正解値の格納
    for i in range(1, count_m):
        # 上昇率が0以上なら1、そうでないなら0を格納
        if modified_data[i,2] > 0:
            answers.append(1)
        else:
            answers.append(0)

    # データの分割（データの80%を訓練用に、20％をテスト用に分割する）
    X_train, X_test, y_train, y_test = train_test_split(successive_data, answers, test_size=0.2, random_state=1)

    parameters = {'C':[1, 3, 5],'loss':('hinge', 'squared_hinge')}

    # グリッドサーチを実行
    clf = GridSearchCV(svm.LinearSVC(), parameters)
    clf.fit(X_train, y_train) 
 
    # グリッドサーチ結果(最適パラメータ)を取得
    GS_C, GS_loss = clf.best_params_.values()
    #print ("最適パラメータ：{}".format(clf.best_params_))

    # 最適パラメータを指定して学習
    clf = svm.LinearSVC(loss=GS_loss, C=GS_C,random_state=1)
    clf.fit(X_train , y_train)

    # 学習後のモデルによるテスト
    # トレーニングデータを用いた予測
    y_train_pred = clf.predict(X_train)
    # テストデータを用いた予測
    y_val_pred = clf.predict(X_test)
    
    target_data = shapeCsv(brand_num,False)

    # データの正規化        
    ms = MinMaxScaler()
    ms.fit(target_data)
    target_data = ms.transform(target_data)

    # データの標準化
    sc = StandardScaler()
    sc.fit(successive_data)
    target_data = sc.transform(target_data)

    target_len = len(target_data)
    target_predict = clf.predict(target_data)
    return target_predict[target_len-1]

    # 正解率の計算
    train_score = accuracy_score(y_train, y_train_pred)
    test_score = accuracy_score(y_test, y_val_pred)
    # 正解率を表示
    print("トレーニングデータに対する正解率：" + str(train_score * 100) + "%")
    print("テストデータに対する正解率：" + str(test_score * 100) + "%")


f = open('get_brand_nikkei.txt')
file = open('data_to_predict_of_select2/target2.txt','a')
lines = f.readlines()
target_num = []
i = 0
for line in lines:
    #print(line)
    line = line.replace("\n","")
    tmp = getData(line)
    i += 1
    if(tmp == 1):
        target_num.append(line)
        file.write(line + '\n')


#print(target_num)
print("uped percent is  " + str(len(target_num)/i) + "  and  all  data  is  "+str(i) + "  and  uped  is  "+str(len(target_num)))
f.close()

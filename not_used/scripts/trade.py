# サポートベクターマシーンのimport
from sklearn import svm
# train_test_splitのimport
from sklearn.model_selection import train_test_split
# accuracy_scoreのimport
from sklearn.metrics import accuracy_score
# Pandasのimport
import pandas as pd
# グリッドサーチのimport
from sklearn.model_selection import GridSearchCV
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

def shapeCsv(brand_num,isTestdata):
    # 株価の上昇率を算出、おおよそ-1.0～1.0の範囲に収まるように調整
    modified_data = []
    if(isTestdata):
        for i in range(1,4):
            #tmp_data = pd.read_csv("6758_" + str(2015 + i) + ".csv", encoding="shift-jis")
            tmp_data = pd.read_csv("../stock_data/adopted_nikkeiheikin/"+ str(2015 + i) + "/all_stock_data_with_date/all_stock_data_with_date_"+ str(brand_num) +".csv", encoding="shift-jis")
            tmp_range = len(tmp_data)

            for i in range(2,tmp_range):
                modified_data.append((float(tmp_data.iat[i,3]) - float(tmp_data.iat[i-1,3]))/float(tmp_data.iat[i-1,3])*20)
    else:
        tmp_data = pd.read_csv("../stock_data/adopted_nikkeiheikin/2019/all_stock_data_with_date/all_stock_data_with_date_"+ str(brand_num) +".csv",encoding="shift-jis")
        tmp_range = len(tmp_data)
        
        for i in range(2,tmp_range):
            modified_data.append((float(tmp_data.iat[i,3]) - float(tmp_data.iat[i-1,3]))/float(tmp_data.iat[i-1,3])*20)

    return modified_data


def getData1(brand_num):
    
    modified_data = shapeCsv(brand_num,True)
    # 要素数の設定
    count_m = len(modified_data)
    #print(modified_data) 
    # 過去４日分の上昇率のデータを格納するリスト
    successive_data = []
 
    # 正解値を格納するリスト　価格上昇: 1 価格低下:0
    answers = []
 
    #  連続の上昇率のデータを格納していく
    for i in range(10, count_m):
        successive_data.append([modified_data[i-10]
            ,modified_data[i-9],modified_data[i-8],modified_data[i-7],modified_data[i-6],modified_data[i-5],modified_data[i-4]
            ,modified_data[i-3],modified_data[i-2],modified_data[i-1]])
        # 上昇率が0以上なら1、そうでないなら0を格納
        if modified_data[i] > 0:
            answers.append(1)
        else:
            answers.append(0)
    #print(successive_data) 
    # データの分割（データの80%を訓練用に、20％をテスト用に分割する）
    X_train, X_test, y_train, y_test =train_test_split(successive_data, answers, train_size=0.8,test_size=0.2,random_state=1)
 
    # サポートベクターマシーン
    clf = svm.LinearSVC()

    parameters = {'C':[1, 3, 5],'loss':('hinge', 'squared_hinge')}
 
    # グリッドサーチを実行
    clf = GridSearchCV(svm.LinearSVC(), parameters)
    clf.fit(X_train, y_train) 
 
    # グリッドサーチ結果(最適パラメータ)を取得
    GS_C, GS_loss = clf.best_params_.values()
    #print ("最適パラメータ：{}".format(clf.best_params_))

    # サポートベクターマシーンによる訓練
    #clf.fit(X_train , y_train)

    tmp_data = shapeCsv(brand_num,False)
    tmp_len = len(tmp_data)
    target_data = []

    for i in range(10, tmp_len):
        target_data.append([tmp_data[i-10]
            ,tmp_data[i-9],tmp_data[i-8],tmp_data[i-7],tmp_data[i-6],tmp_data[i-5],tmp_data[i-4]
            ,tmp_data[i-3],tmp_data[i-2],tmp_data[i-1]])
    target_len = len(target_data)
    target_predict = clf.predict(target_data)
    return target_predict[target_len-1]
 
    y_train_pred = clf.predict(X_train)
    # テストデータを用いた予測
    y_val_pred = clf.predict(X_test)
 
    # 正解率の計算
    train_score = accuracy_score(y_train, y_train_pred)
    test_score = accuracy_score(y_test, y_val_pred)
    # 正解率を表示
    print("トレーニングデータに対する正解率：" + str(train_score * 100) + "%")
    print("テストデータに対する正解率：" + str(test_score * 100) + "%")


    plt.figure(figsize=(8, 5))
    plt.plot(y_train_pred)
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')

    # 学習後のモデルによるテスト
    # トレーニングデータを用いた予測
    #y_train_pred = clf.predict(X_train)
    # テストデータを用いた予測
    #y_val_pred = clf.predict(X_test)
 
    # 正解率の計算
    #train_score = accuracy_score(y_train, y_train_pred)
    #test_score = accuracy_score(y_test, y_val_pred)
 
    # 正解率を表示
    #print("トレーニングデータに対する正解率：" + str(train_score * 100) + "%")
    #print("テストデータに対する正解率：" + str(test_score * 100) + "%")

f = open('get_brand_nikkei.txt')
fil = open('data_to_predict_of_select2/target1.txt','w')
lines = f.readlines()
target_num = []
i = 0
for line in lines:
    line = line.replace("\n","")
    tmp = getData1(line)
    #print(tmp)
    i += 1
    if(tmp == 1):
        target_num.append(line)
        fil.write(line + '\n')


#print(target_num)
print("uped percent is  " + str(len(target_num)/i) + "  and  all  data  is  "+str(i) + "  and  uped  is  "+str(len(target_num)))
f.close()

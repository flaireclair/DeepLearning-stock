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

import matplotlib.pyplot as plt
plt.style.use('ggplot')

def shapeCsv(brand_num,isTestdata):
    # 株価の上昇率を算出、おおよそ-1.0～1.0の範囲に収まるように調整
    modified_data = []
    if(isTestdata):
        for i in range(1,4):
            tmp_data = pd.read_csv("./adopted_nikkeiheikin/"+ str(2015 + i) + "/all_stock_data_with_date/all_stock_data_with_date_"+ str(brand_num) +".csv", encoding="shift-jis")
            tmp_range = len(tmp_data)

            for i in range(2,tmp_range):
                modified_data.append((float(tmp_data.iat[i,3]) - float(tmp_data.iat[i-1,3]))/float(tmp_data.iat[i-1,3])*20)
    else:
        tmp_data = pd.read_csv("./adopted_nikkeiheikin/2019/all_stock_data_with_date/all_stock_data_with_date_"+ str(brand_num) +".csv",encoding="shift-jis")
        tmp_range = len(tmp_data)
        
        for i in range(2,tmp_range):
            modified_data.append((float(tmp_data.iat[i,3]) - float(tmp_data.iat[i-1,3]))/float(tmp_data.iat[i-1,3])*20)

    return modified_data


def getData1(brand_num, array_num, plt_num, no):
    
    modified_data = shapeCsv(brand_num,True)
    # 要素数の設定
    count_m = len(modified_data)

    # 過去10日分の上昇率のデータを格納するリスト
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

    #2/7までのデータを予測させる
    tmp_data = shapeCsv(brand_num,False)
    tmp_len = len(tmp_data)
    target_data = []

    for i in range(10, tmp_len):
        target_data.append([tmp_data[i-10]
            ,tmp_data[i-9],tmp_data[i-8],tmp_data[i-7],tmp_data[i-6],tmp_data[i-5],tmp_data[i-4]
            ,tmp_data[i-3],tmp_data[i-2],tmp_data[i-1]])
    target_len = len(target_data)
    target_predict = clf.predict(target_data)

    if brand_num == "2531" or brand_num == "4507" or brand_num == "8035" or brand_num == "8766" or brand_num == "9022" or brand_num == "6098" or brand_num == "4021" or brand_num == "4506" or brand_num == "6367" :
        plt.subplot(2, 5, no)
        plt.plot(target_predict)
        plt.title('{}'.format(brand_num))
        plt.ylabel('varitation')
        plt.xlabel('date flow')
        no += 1
    else :
        pass

    #2/8以降の予想を返す
    return target_predict[target_len-1], no

def main():
    f = open('nikkei.txt')
    file = open('target1.txt','a')
    lines = f.readlines()
    target_num = []
    i = 0
    no = 1
    plot_num = range(len(lines))
    for line in lines:
        line = line.replace("\n","")
        tmp, no = getData1(line, i, len(plot_num), no)
        i += 1

        # 株価が上昇すると予想できた銘柄をtarget_numに格納
        if(tmp == 1):
            target_num.append(line)
            file.write(line + '\n')

    plt.show()
    # 株価が上昇すると判断した銘柄の割合を出力  
    print("uped percent is  " + str(len(target_num)/i) + "  and  all  data  is  "+str(i) + "  and  uped  is  "+str(len(target_num)))
    f.close()

# main関数呼び出し
if __name__ == "__main__":
    main() 

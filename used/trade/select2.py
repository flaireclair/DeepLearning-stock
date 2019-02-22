# coding: UTF-8
#
#-------------------------------------------------------------------------
# 引数
#
# searchData関数
# isUseContinuousData: 過去三年分の複数データを用いるか2018年の純利益を用いるかの変数
# 
# turnHighData関数
# target_array: 銘柄番号が格納された配列
#
# getparameter関数
# result_array: 銘柄番号が格納された配列
#
# 使用したファイル
# toushou.csv: 東証一部の業績が格納されているcsvファイル
# target1.txt: trade.pyで学習させた分類器によって株価が上昇すると判断された株の銘柄番号が格納されているtxtファイル
# target2.txt: trade2.pyで学習させた分類器によって株価が上昇すると判断された株の銘柄番号が格納されているtxtファイル
# 
# 変数
#
# searchData関数
# isColumndata: 読み込んだcsvファイルのデータがcolumnかどうかの変数
# l[1]: csvデータに格納されている銘柄番号
# l[3]: csvデータに格納されている決算が行われた時期と決算の種類
# l[7]: csvデータに格納されている純利益
# tmp: 決算が行われた時期
# tmp_flag: 16年,17年,18年の連続性が保証されているかどうか
# 
# turnHighData関数
# target_score: 条件にあった銘柄番号が入っている配列
# 
# machile_learning関数
# target_array: target1.txt,target2.txt両方に格納されている銘柄番号が格納された配列
#
# getparameter関数
# result_array: 購入する金額を格納した配列。並びはbest_scoreに対応している
# result_len: money_aryの配列の長さ
# num: best_scoreに格納されている銘柄の1株あたりの利益の合計
#
#---------------------------------------------------------------------------

import csv

# 受け取った銘柄番号の業績が一定条件を満たしている時Trueを、そうでない時はFalseを返す
def searchData(brand_num,isUseContinuousData):

    with open('toushou.csv','r',newline='',encoding='utf-8') as f:
        r = csv.reader(f)
        isColumndata = True
        tmp_flag = False
        tmp = 0
        n = 1

        for l in r:

            # column避け
            if(isColumndata):
                isColumndata = False
                continue
            
            # 引数と同じ銘柄番号の情報以外は除外
            if(int(l[1].replace('\n','')) != brand_num):
                continue
            # データがない場合は除外
            if(l[8] == "--"):
                continue
            # 連結決算もしくは単独決算でない情報は除外
            if(l[3][n-1] == "中" or l[3][n-1] == "四" or l[3][n-1] == "会"): 
                continue
            
            # 過去3年分の業績を対象とする
            if(isUseContinuousData):
                tmp = int(l[3][n+1])
                
                #持ってきた決算情報の時期が16年の時
                if(tmp == 6):
                    # データがないときは除外
                    if(l[7].replace(',','') == "--"):
                        continue
                    tmp_brand_num = int(l[1])
                    tmp_data1 = float(l[7].replace(',',''))
                    tmp_data2 = float(l[4].replace(',',''))
                    tmp_flag = True
                
                #持ってきた決算情報の時期が17年の時
                elif(tmp == 7):
                    if(l[7].replace(',','') == "--" or l[4].replace(',','') == "--"):
                        tmp_flag = False
                        continue
                    
                    if(tmp_flag and tmp_brand_num == int(l[1]) and tmp_data1 < float(l[7].replace(',','')) and tmp_data2 < float(l[4].replace(',',''))):
                        tmp_data1 = float(l[7].replace(',',''))
                        tmp_data2 = float(l[4].replace(',',''))
                    else:
                        tmp_flag = False

                #持ってきた決算情報の時期が18年の時
                elif(tmp == 8):
                    if(l[7].replace(',','') == "--" or l[4].replace(',','') == "--"):
                        tmp_flag = False
                        continue
                    if(tmp_flag and tmp_brand_num == int(l[1]) and tmp_data1 < float(l[7].replace(',','')) and tmp_data2 < float(l[4].replace(',',''))):
                        return True
                    else:
                        tmp_flag = False

            else:
                if(l[3][n+1] != "8"):
                    continue
                if(float(l[7].replace(',','')) > 0):
                    return True

        return False

# 受け取った銘柄番号の中から条件を満たす銘柄番号を格納した配列を返す
def turnHighData(target_array,isUseContinuousData):
    result_array = []
    
    for line in target_array:
        if(searchData(int(line.replace('\n','')),isUseContinuousData)):
            result_array.append(int(line.replace('\n','')))
    
    return result_array

# 別ファイルで学習させたモデルが選択した銘柄番号2種類のうち両方に含まれている銘柄番号を格納した配列を返す
def machile_learning():
    file1 = open('target1.txt')
    line1s = file1.readlines()
    file2 = open('target2.txt')
    line2s = file2.readlines()
    target_array = []

    for line1 in line1s:
        line1 = line1.replace("\n","")
        for line2 in line2s:
            line2 = line2.replace("\n","")
            if(line1 == line2):
                target_array.append(line2)
                break

    return target_array

# 受け取った銘柄番号の中から業績を使って条件を満たす銘柄番号が格納された配列を返す
def getparameter(target_array):
    with open('toushou.csv','r',newline='',encoding='utf-8') as f:
        r = csv.reader(f)
        result_array = []
        i = 0
        n = 2

        for l in r:
            if(len(result_array) == 9):
                break
            # column避け
            if(i == 0):
                i += 1
                continue

            for target_num in target_array:
                                
                # 必要なデータのみ抜き出し
                if(int(l[1].replace('\n','')) != target_num):
                    continue
                if(l[3][n] != "8"):
                    continue
                if(l[3][n-2] == "中"):    
                    continue
                result_array.append(float(l[8].replace(',','')))

        num = 0
        result_len = len(result_array)

        for i in result_array:
           num += i
        for j in range(0,result_len):
            result_array[int(j)] /= num
            result_array[int(j)] *= 1000
        for n in range(0,result_len):
            print("銘柄番号"+str(target_array[n])+"の株を大体"+str(result_array[n])+"万円\n")
        print("買うといいらしい")

# 各ファイルから銘柄番号を持ってきて条件を満たす銘柄番号を抽出し、購入金額の割合と一緒に出力を行う

def main():
    # 学習させたモデルが選んだ銘柄番号を格納した配列を受け取る
    target_array = machile_learning()

    # 業績を使って銘柄を絞る
    target_score = turnHighData(target_array,False)
    target_score2 = turnHighData(target_array,True)

    # ２つ両方に入っている銘柄番号を抜き出す
    target_array = []
    for tmp in target_score:
        for tmp2 in target_score2:
            if(tmp == tmp2):
                target_array.append(tmp2)
                break

    # 結果の出力
    getparameter(target_array)

# main関数呼び出し
if __name__ == "__main__":
    main() 

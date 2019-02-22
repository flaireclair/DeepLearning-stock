# coding: UTF-8
import csv
#from trade2 import getData
#from trade import getData1

def searchData(brand_num,isUseContinuousData):
    tmp = 0
    tmp_data = 0
    tmp_flag = False

    with open('data_to_predict_of_select2/toushou.csv','r',newline='',encoding='utf-8') as f:
        r = csv.reader(f)
        i = 0

        for l in r:
            n = 1
            # column避け
            if(i == 0):
                i += 1
                continue
            
            # 必要なデータのみ抜き出し
            if(int(l[1].replace('\n','')) != brand_num):
                continue

            if(l[8] == "--"):
                continue
            #if(l[3][n-1] != "連" and l[3][n-1] != "◎" and l[3][n-1] != "◇" and l[3][n-1] != "単" and l[3][n-1] != "□"):
            if(l[3][n-1] == "中" or l[3][n-1] == "四" or l[3][n-1] == "会"): 
                continue
            
            # 過去3年分の業績を対象とする
            if(isUseContinuousData):
                tmp = int(l[3][n+1])
                
                if(tmp == 6):
                    # データがないときは除外
                    if(l[7].replace(',','') == "--"):
                        continue
                    tmp_brand_num = int(l[1])
                    tmp_data1 = float(l[7].replace(',',''))
                    tmp_data2 = float(l[4].replace(',',''))
                    tmp_flag = True
                
                elif(tmp == 7):
                    if(l[7].replace(',','') == "--" or l[4].replace(',','') == "--"):
                        tmp_flag = False
                        continue
                    
                    if(tmp_flag and tmp_brand_num == int(l[1]) and tmp_data1 < float(l[7].replace(',','')) and tmp_data2 < float(l[4].replace(',',''))):
                        tmp_data1 = float(l[7].replace(',',''))
                        tmp_data2 = float(l[4].replace(',',''))
                    else:
                        tmp_flag = False

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
                    #return float(l[7].replace(',',''))
                    return True

        return False

def turnHighData(target_array,isUseContinuousData):
    target_score = []
    
    for line in target_array:
        if(searchData(int(line.replace('\n','')),isUseContinuousData)):
            target_score.append(int(line.replace('\n','')))
    
    return target_score

def machile_learning():
    file1 = open('data_to_predict_of_select2/target1.txt')
    line1s = file1.readlines()
    file2 = open('data_to_predict_of_select2/target2.txt')
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



    f = open('get_brand_nikkei.txt')
    lines = f.readlines()
    tmp_ary1 = []
    tmp_ary2 = []
    target_array = []

    for line in lines:
        line = line.replace("\n","")
        #tmp = getData(line)
        #tmp2 = getData1(line)

        if(tmp == 1):
            tmp_ary1.append(line)
        elif(tmp2 == 1):
            tmp_ary2.append(line)

    for i in tmp_ary1:
        for j in tmp_ary2:
            if(i == j):
                target_array.append(j)
                break
    print(tmp_ary1)
    print(tmp_ary2)
    #print(target_array)

    return target_array

def getparameter(best_score):
    with open('data_to_predict_of_select2/toushou.csv','r',newline='',encoding='utf-8') as f:
        r = csv.reader(f)
        money_ary = []
        i = 0
        n = 2
        for l in r:
            if(len(money_ary) == 9):
                break
            # column避け
            if(i == 0):
                i += 1
                continue

            for target_num in best_score:
                                
                # 必要なデータのみ抜き出し
                if(int(l[1].replace('\n','')) != target_num):
                    continue
                if(l[3][n] != "8"):
                    continue
                print(str(target_num) +"   and   "+ str(l[3]))
                #if(l[3][n-2] != "連" and l[3][n-1] != "◎" and l[3][n-1] != "◇" and l[3][n-1] != "単" and l[3][n-1] != "□" and l[3][n-1] != "◇"):
                if(l[3][n-2] == "中"):    
                    continue

                money_ary.append(float(l[8].replace(',','')))
        num = 0
        money_len = len(money_ary)
        for i in money_ary:
           num += i
        for j in range(0,money_len):
            money_ary[int(j)] /= num
            money_ary[int(j)] *= 1000
        for n in range(0,money_len):
            print("銘柄番号"+str(best_score[n])+"の株を大体"+str(money_ary[n])+"万円\n")
        print("買うといいらしい")




tmp_array = machile_learning()
tmp_score = turnHighData(tmp_array,False)
tmp_score2 = turnHighData(tmp_array,True)
best_score = []
print(tmp_score)
print(tmp_score2)
for tmp in tmp_score:
    for tmp2 in tmp_score2:
        if(tmp == tmp2):
            best_score.append(tmp2)
            break
print(best_score)
getparameter(best_score)


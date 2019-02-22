#1つ目

# scikit-learnのLinearRegressionというモデルをインポートします。詳細は1.2で説明します
from sklearn.linear_model import LinearRegression

# scikit-learnに標準で搭載されている、ボストン市の住宅価格のデータセットをインポートします
from sklearn.datasets import load_boston

# scikit-learnに搭載されているデータセットを学習用と予測結果照合用に分けるツールをインポートします
from sklearn.model_selection import train_test_split


# データの読み込みです
data = load_boston()

# データを教師用とテスト用に分けます
train_X, test_X, train_y, test_y = train_test_split(
    data.data, data.target, random_state=42)

# 学習器の構築です
model = LinearRegression()

# 教師データを用いて学習器に学習させてください
model.fit(train_X,train_y)

# テスト用データを用いて学習結果をpred_yに格納してください
pred_y = model.predict(test_x)

# 予測結果を出力します
print(pred_y)


#2つ目

# 必要なモジュールのインポートします。
import request
from sklearn.linear_model import LinearRegression

# 次に学習させたいデータの読み込みを行います。詳しいコードはこの問題にあるコードを参照ください。
# 以下のようにtrain_X, test_X, train_y, test_yという4つのファイルに分けてデータがロードします。
train_X, test_X, train_y, test_y = (データの情報)

# 学習器の構築を行います。
# 学習器とは、学習モデル(学習方法)に沿って学習を行うように設計されたオブジェクトのことです。
# scikit-learnのLinearRegressionが学習して予測データを返してくれるのです。
# このLinearRegressionの詳細は次以降のセッションで扱います。
model = LinearRegression()

# 教師データ(学習を行うための既存データ)を用いて学習器に学習させます。
model.fit(train_X, train_y)

# 教師データとは別に用意したテスト用データを用いて学習器に予測させます。
pred_y = model.predict(test_X)

# 学習器の性能を確認するため決定係数という評価値を算出します。
score = model.score(test_X, test_y)

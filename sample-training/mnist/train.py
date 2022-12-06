# ライブラリのインポート
import numpy as np
from keras.datasets import mnist
from keras.models import Model
from keras.layers import Input, Dense

# MNISTのトレーニングデータを用意
(x_train, _), (_, _) = mnist.load_data()
x_train = x_train.astype('float32') / 255.  # 正規化
x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))  # 28x28の画像を784次元のベクトルに変換

# オートエンコーダーのモデルを定義
# 入力層から中間層へのエンコーダー部分
input_img = Input(shape=(784,))
encoded = Dense(32, activation='relu')(input_img)

# 中間層から出力層へのデコーダー部分
decoded = Dense(784, activation='sigmoid')(encoded)

# エンコーダーとデコーダーをモデルとしてまとめる
autoencoder = Model(input_img, decoded)

# モデルをコンパイルして学習させる
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')
autoencoder.fit(x_train, x_train, epochs=50, batch_size=256, shuffle=True)

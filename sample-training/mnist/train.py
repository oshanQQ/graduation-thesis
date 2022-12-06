# ライブラリのインポート
import wandb
from wandb.keras import WandbCallback
import numpy as np
from keras.datasets import mnist
from keras.models import Model
from keras.layers import Input, Dense

# wandbの初期化
wandb.init(project="my-test-project")
wandb.config = {
  "learning_rate": 0.001,
  "epochs": 100,
  "batch_size": 128
}

# MNISTのトレーニングデータとテストデータを用意
(x_train, _), (x_test, _) = mnist.load_data()
x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.
x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
x_test = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))

# オートエンコーダーのモデルを定義
input_img = Input(shape=(784,))
encoded = Dense(32, activation='relu')(input_img)
decoded = Dense(784, activation='sigmoid')(encoded)
autoencoder = Model(input_img, decoded)

# モデルをコンパイルして学習させる
# wandbコールバック関数を指定して、学習中のGPUの状態を記録していく
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')
autoencoder.fit(x_train, x_train, epochs=50, batch_size=256, shuffle=True, callbacks=[WandbCallback()])

# 学習済みのモデルを使って、テストデータを検証する
decoded_imgs = autoencoder.predict(x_test)

# 検証結果をプロットする
import matplotlib.pyplot as plt

# オリジナルの画像とデコード後の画像のペアを10組表示する
n = 10
plt.figure(figsize=(20, 4))
for i in range(n):
    # オリジナルの画像を表示
    ax = plt.subplot(2, n, i + 1)
    plt.imshow(x_test[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # デコード後の画像を表示
    ax = plt.subplot(2, n, i + 1 + n)
    plt.imshow(decoded_imgs[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
plt.savefig("mnist_result.png")

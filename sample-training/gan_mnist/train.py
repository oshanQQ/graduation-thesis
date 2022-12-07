import keras
from keras.datasets import mnist
from keras.layers import Input, Dense, Reshape, Flatten, Dropout
from keras.layers import BatchNormalization, Activation, ZeroPadding2D
from keras.layers.advanced_activations import LeakyReLU
from keras.layers.convolutional import UpSampling2D, Conv2D
from keras.models import Sequential, Model
from tensorflow.keras.optimizers import Adam
import numpy as np

# MNISTデータセットを読み込む
(X_train, _), (_, _) = mnist.load_data()

# 入力ノイズの次元
noise_dim = 100

# 生成モデルを定義する
generator = Sequential()
generator.add(Dense(128 * 7 * 7, activation="relu", input_dim=noise_dim))
generator.add(Reshape((7, 7, 128)))
generator.add(UpSampling2D())
generator.add(Conv2D(128, kernel_size=3, padding="same"))
generator.add(BatchNormalization(momentum=0.8))
generator.add(Activation("relu"))
generator.add(UpSampling2D())
generator.add(Conv2D(64, kernel_size=3, padding="same"))
generator.add(BatchNormalization(momentum=0.8))
generator.add(Activation("relu"))
generator.add(Conv2D(1, kernel_size=3, padding="same"))
generator.add(Activation("tanh"))

# 識別モデルを定義する
discriminator = Sequential()
discriminator.add(Conv2D(32, kernel_size=3, strides=2, input_shape=(28, 28, 1), padding="same"))
discriminator.add(LeakyReLU(alpha=0.01))
discriminator.add(Dropout(0.25))
discriminator.add(Conv2D(64, kernel_size=3, strides=2, padding="same"))
discriminator.add(ZeroPadding2D(padding=((0,1),(0,1))))
discriminator.add(BatchNormalization(momentum=0.8))
discriminator.add(LeakyReLU(alpha=0.01))
discriminator.add(Dropout(0.25))
discriminator.add(Conv2D(128, kernel_size=3, strides=2, padding="same"))
discriminator.add(BatchNormalization(momentum=0.8))
discriminator.add(LeakyReLU(alpha=0.01))
discriminator.add(Dropout(0.25))
discriminator.add(Conv2D(256, kernel_size=3, strides=1, padding="same"))
discriminator.add(BatchNormalization(momentum=0.8))
discriminator.add(LeakyReLU(alpha=0.01))
discriminator.add(Dropout(0.25))
discriminator.add(Flatten())
discriminator.add(Dense(1, activation='sigmoid'))

# 識別モデルをコンパイル
discriminator.compile(loss='binary_crossentropy', optimizer=Adam(), metrics=['accuracy'])

# 生成モデルと識別モデルからGANを構成
gan = Sequential()
gan.add(generator)
gan.add(discriminator)
gan.compile(loss='binary_crossentropy', optimizer=Adam())

# MNISTデータセットを入力データとして使用
X_train = (X_train.astype(np.float32) - 127.5) / 127.5
X_train = np.expand_dims(X_train, axis=3)

# バッチサイズ
batch_size = 64

# 無限ループで学習
for epoch in range(10000):
    # ランダムなノイズを生成
    noise = np.random.normal(0, 1, (batch_size, noise_dim))
    
    # 生成モデルから画像を生成
    generated_images = generator.predict(noise)

    # MNISTデータセットからランダムに画像を選択
    image_batch = X_train[np.random.randint(0, X_train.shape[0], size=batch_size)]

    # 生成モデルの画像と本物のMNIST画像を結合
    X = np.concatenate([image_batch, generated_images])

    # 本物のMNIST画像と生成モデルの画像のラベルを作成
    y = np.concatenate([np.ones((batch_size, 1)), np.zeros((batch_size, 1))])

    # 識別モデルを学習
    discriminator.trainable = True
    d_loss = discriminator.train_on_batch(X, y)

    # ランダムなノイズを生成
    noise = np.random.normal(0, 1, (batch_size, noise_dim))

    # 識別モデルを無効化して、生成モデルを学習
    discriminator.trainable = False
    g_loss = gan.train_on_batch(noise, np.ones((batch_size, 1)))

    # 進捗を出力
    if epoch % 100 == 0:
        print("epoch: {}, g_loss: {}, d_loss: {}".format(epoch, g_loss, d_loss))

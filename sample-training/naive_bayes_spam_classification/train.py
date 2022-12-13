import pandas as pd
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import LSTM, Dense, Embedding
from sklearn.metrics import confusion_matrix

epoch = 10

pd.set_option("display.max_colwidth", 100)

dataset_df = pd.read_csv('./SMSSpamCollection', sep='\t', header=None)
dataset_df.rename({0: 'label', 1: 'text'}, axis=1, inplace=True)
dataset_df['category'] = dataset_df.apply(lambda r: 1 if r['label'] == 'spam' else 0, axis=1)
dataset_df.head()

X_train, X_test, Y_train, Y_test = train_test_split(
    dataset_df[['text']], dataset_df[['category']], 
    test_size=0.2, random_state=0
)

max_len = 100  # 1メッセージの最大単語数 (不足分はパディング)

tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_train['text'])
x_train = tokenizer.texts_to_sequences(X_train['text'])
x_test = tokenizer.texts_to_sequences(X_test['text'])

for text, vector in zip(X_train['text'].head(3), x_train[0:3]):
    print(text)
    print(vector)

x_train = pad_sequences(x_train, maxlen=max_len)
x_test = pad_sequences(x_test, maxlen=max_len)

print(x_train[0])

vocabulary_size = len(tokenizer.word_index) + 1

model = Sequential()
model.add(Embedding(input_dim=vocabulary_size, output_dim=32))
model.add(LSTM(16, return_sequences=False))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

# テストデータの設定
y_train = Y_train['category'].values
y_test = Y_test['category'].values

# 学習
history = model.fit(
    x_train, y_train, batch_size=32, epochs=epoch,
    validation_data=(x_test, y_test)
)

y_pred = model.predict(x_test)

# 非スパムと誤判定したメッセージ
print(X_test[y_test > y_pred.reshape(-1)]['text'])

# スパムと誤判定したメッセージ
print(X_test[y_test < y_pred.reshape(-1)]['text'])

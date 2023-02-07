import csv
import time
import pandas as pd
import numpy as np
from tensorflow import keras
from tensorflow.keras.datasets import mnist


def Classify(batch_size, epochs):
    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()

    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    model.summary()

    print("\n◆Train:")
    start_time = time.time()
    model.fit(train_images, train_labels, epochs=epochs, batch_size=batch_size)
    end_time = time.time()
    learning_time = end_time - start_time
    print("Done")

    print("\n◆Predict:")
    predictions = model.predict(test_images, verbose=1)
    num = 2
    result = np.argmax(predictions[num])
    print(f"The result of image {num} is [{result}].")

    print("\n◆Evaluate:")
    test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=1)
    print(f"Test accuracy:{100 * test_acc:5.2f}%")
    
    with open('data.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([batch_size, epochs, learning_time, test_loss, test_acc])


for batch in range(10, 101, 10):
    for epoch in range(10, 101, 10):
        Classify(batch, epoch)


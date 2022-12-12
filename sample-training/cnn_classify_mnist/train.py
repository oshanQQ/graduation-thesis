import numpy as np
from tensorflow import keras
from tensorflow.keras.datasets import mnist

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
model.fit(train_images, train_labels, epochs=10)
print("Done")

print("\n◆Predict:")
predictions = model.predict(test_images, verbose=1)
num = 2
result = np.argmax(predictions[num])
print(f"The result of image {num} is [{result}].")

print("\n◆Evaluate:")
test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=1)
print(f"Test accuracy:{100 * test_acc:5.2f}%")

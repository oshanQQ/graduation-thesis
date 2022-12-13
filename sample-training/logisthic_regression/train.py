import wandb
from wandb.keras import WandbCallback
import numpy as np
from keras.datasets import mnist
from keras.models import Sequential 
from keras.layers import Dense, Activation 
from keras.utils import np_utils

nb_epoch = 40

# wandbの初期化
wandb.init(project="logistic-regression-mnist")
wandb.config = {
  "epochs": nb_epoch,
}

(X_train, y_train), (X_test, y_test) = mnist.load_data()

# Split the training set into a training set and a validation set
X_val = X_train[0:10000,:,:]
X_train = X_train[10000:,:,:]
y_val = y_train[0:10000]
y_train = y_train[10000:]

# Reshape the training data tensors so that each image is a vector
input_dim = 784 #28*28 
X_train_flat = X_train.reshape(50000, input_dim) 
X_test_flat = X_test.reshape(10000, input_dim)
X_val_flat = X_val.reshape(10000, input_dim)

# Convert flattned training data to
# tensors of floating point numbers rather than integers
X_train_flat = X_train_flat.astype('float32') 
X_test_flat = X_test_flat.astype('float32') 
X_val_flat = X_val_flat.astype('float32') 

# Scale the training data so that pixel intensity lies in [0,1]
X_train_flat = X_train_flat / 255
X_test_flat = X_test_flat / 255
X_val_flat = X_val_flat / 255

# Convert the labels to the one hot encoding

nb_classes = 10
y_train_one_hot = np_utils.to_categorical(y_train, nb_classes) 
y_val_one_hot = np_utils.to_categorical(y_val, nb_classes)
y_test_one_hot = np_utils.to_categorical(y_test, nb_classes)

# Build a Keras model for logistic regression

output_dim = nb_classes
model = Sequential()
# Add a single layer with 28*28 inputs and 10 ouputs with a softmax activation (i.e. logistic regression)
model.add(Dense(output_dim, input_dim=input_dim, activation='softmax'))

# Compile the model, specifying that SGD should be used to train and the cross entropy 
# loss function should be used. Also keep track of accuracy throughout training.
model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy']) 

# Train the model for 40 epochs, displaying progress (verbose=1) and
# recording performance on the validation. Store record of training
# in variable "history".
history = model.fit(X_train_flat, y_train_one_hot, epochs=nb_epoch, verbose=1, validation_data=(X_val_flat, y_val_one_hot), callbacks=[WandbCallback()])

# Test the trained model on the test set
score = model.evaluate(X_test_flat, y_test_one_hot, verbose=0) 
print('Test loss:', score[0]) 
print('Test accuracy:', score[1])


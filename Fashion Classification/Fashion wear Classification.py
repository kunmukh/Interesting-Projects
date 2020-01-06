import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

# DATA LOADING AND PROCESSING
# load the data set
data = keras.datasets.fashion_mnist

# separate the data into training and testing data set
(train_images, train_labels), (test_images, test_labels) = data.load_data()

# get the label for the classfier
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# change the data range from 0-255 to 0-1
train_images = train_images/255.0
test_images = test_images/255.0

# print(train_images[7])

# show the image  in grey scale
# plt.imshow(train_images[7], cmap=plt.cm.binary)
# plt.show()

# TRAINING OF THE NEURAL NETWORK

# declaring the layers
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28,28)),
    keras.layers.Dense(128, activation="relu"), # rectified linear unit
    keras.layers.Dense(10, activation="softmax") # get a value from 0-1
])

model.compile(optimizer="adam",
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])

# training the model
model.fit(train_images, train_labels, epochs=5)

# testing the model
test_loss, test_acc = model.evaluate(test_images, test_labels)

print("Tested Acc: ", test_acc)

# PREDICTION FROM THE NEURAL NETWORK

# predictions = model.predict(test_images[7])
predictions = model.predict(test_images)

for i in range(5):
    plt.grid(False)
    plt.imshow(test_images[i], cmap=plt.cm.binary)
    plt.xlabel("Actual: " + class_names[test_labels[i]])
    plt.title("Prediction: " + class_names[np.argmax(predictions[i])])
    plt.show()

# print(class_names[np.argmax(predictions[0])])



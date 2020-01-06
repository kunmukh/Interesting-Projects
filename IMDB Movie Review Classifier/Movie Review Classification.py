import tensorflow as tf
from tensorflow import keras
import numpy as np

data = keras.datasets.imdb

# separate the data into training and testing data set
(train_data, train_labels), (test_data, test_labels) = data.load_data(num_words=88000)

# print(train_data[0])

# returns tuple of key and value
word_index = data.get_word_index()

# separate the tuples in key and value
word_index = {k:(v+3) for k, v in word_index.items()}

word_index["<PAD>"] = 0
word_index["<START>"] = 1
word_index["<UNK>"] = 2
word_index["<UNUSED>"] = 3

# change integer to point to a word
reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])

# converting the data into a form that the model can take in
train_data = keras.preprocessing.sequence.pad_sequences(train_data,
                                                        value=word_index["<PAD>"],
                                                        padding="post",
                                                        maxlen=250)
test_data = keras.preprocessing.sequence.pad_sequences(test_data,
                                                        value=word_index["<PAD>"],
                                                        padding="post",
                                                        maxlen=250)

def decode_review(text):
    return " ".join([reverse_word_index.get(i, "?") for i in text])

# print(decode_review(test_data[0]))

# declaring the layers for the model
'''model = keras.Sequential()
model.add(keras.layers.Embedding(88000, 16)) # input vector = 1000, output dim = 16
model.add(keras.layers.GlobalAveragePooling1D()) # brings down the dimension
model.add(keras.layers.Dense(16, activation="relu"))
model.add(keras.layers.Dense(1, activation="sigmoid"))

model.summary()

model.compile(optimizer="adam",
              loss="binary_crossentropy",
              metrics=["accuracy"])

# VALIDATION: how well our model is working
x_val = train_data[:10000]
x_train = train_data[10000:]

y_val = train_labels[:10000]
y_train = train_labels[10000:]

# training the model
fitModel = model.fit(x_train,
                     y_train,
                     epochs=40,
                     batch_size=512,
                     validation_data=(x_val, y_val),
                     verbose=1)
                     
# Saving the model
model.save("word_model.h5")'''

# Loading a saved model
model = keras.models.load_model("word_model.h5")

# getting the accuracy
acc = model.evaluate(test_data, test_labels)

print("Accuracy of model: ", acc[1])

# predictions from a test model
test_review = test_data[0]
predict = model.predict([test_review])
print("Review: ", decode_review(test_review))
print("Predictions: " + str(predict[0]))
print("Actual: " + str(test_labels[0]))
print("Accuracy: ", acc[1])

# predictions from an outside data
def review_encode(s):
    encoded = [1]

    for word in s:
        if word.lower() in word_index:
            encoded.append(word_index[word.lower()])
        else:
            encoded.append(2)

    return encoded

with open("text.txt", encoding="utf-8") as f:
    for line in f.readlines():
        nline = line.replace(",", "").replace(".", "").replace("(", "").\
            replace(")", "").replace(":", "").replace("\"", "").strip().split(" ")
        encode = review_encode(nline)
        encode = keras.preprocessing.sequence.pad_sequences([encode],
                                                            value=word_index["<PAD>"],
                                                            padding="post",
                                                            maxlen=250)
        predict = model.predict(encode)
        print("Line: ", line)
        print("encoded test: ", encode)
        print("Predictions: " + str(predict[0]))
import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy
import tflearn
import tensorflow
import random
import json
import pickle

stemmer = LancasterStemmer()
nltk.download('punkt')

# opening the json file that contains the data
with open("intents.json") as file:
    data = json.load(file)

try:
    with open("data.pickle", "rb") as f: #rb: read byte
        words, labels, training, output = pickle.load(f)
except:
    # pre-processing the data
    words = [] # all the words in our patter the model has seen
    labels = [] # all the labels
    docs_x = [] # list of all the patterns
    docs_y = [] # list of all the tags for the pattern

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    # one hot encoded( a list of all the words that contains
    # how many times each word has occurred in the list
    training = [] # pattern
    output = [] # distinct label for the bag of word

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = [] # numerical conversion for pattern

        wrds = [stemmer.stem(w) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)

    with open("data.pickle", "wb") as f: #rb: read byte
        pickle.dump((words, labels, training, output), f)

# creating a model
tensorflow.reset_default_graph() # reset the data graph

# input neurons with same number of words as seen in pattern
net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8) # hidden layer of 8 neurons
net = tflearn.fully_connected(net, 8) # hidden layer of 8 neurons
# output neurons with each of the classes, predict which tag to give response from
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

# train the model
model = tflearn.DNN(net) # type of neural network

try:
    model.load("chatbot.tflearn")
except:
    # fitting the model
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("chatbot.tflearn")

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))] # store all the words, 0

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)

def chat():
    print("Start talking with the bot! Type quit to stop")

    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            print("Bot: Good bye!")
            break

        results = model.predict([bag_of_words(inp, words)])[0]
        results_index = numpy.argmax(results)
        tag = labels[results_index]
        # print("Tag: ", tag)

        if results[results_index] > 0.7:
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']

            print("Bot :", random.choice(responses))
        else:
            print("Bot: I did not get that, try again!")

# main runner file
chat()
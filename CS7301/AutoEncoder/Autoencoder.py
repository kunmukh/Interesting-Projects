# Name: Kunal Mukherjee
# Personal email: kunmukh@GMAIL.COM
# Date: 8/30/21
# File name: 
# Project name:

from keras.layers import Input, Dense
from keras import regularizers
from keras.models import Model, load_model
import os
import logging
import sys
import datetime
from AutoencoderUtils import AutoencoderUtils
import time


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s | %(levelname)s\t| %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

# base directory for models
base = "C:\\Users\\kunmu\\Documents\\Kunal\\gitlab\\autoencoder\\"
modelsBase = base+"models\\autoencoder\\"
logBase = base+"logs\\"

class Autoencoder():

    def __init__(self, trainFilename, anomolyFilename):
        print("DEBUG: Autoencoder init")
        self.trainFilename = trainFilename
        self.anomolyFilename = anomolyFilename
        self.autoencoderUtils = AutoencoderUtils()
        self.uniqueName = self.generateUniqueName(trainFilename, anomolyFilename)
        self.modelFilename = modelsBase + self.uniqueName + ".h5"
        self.logFile = logBase + self.uniqueName + ".log"

    def generateUniqueName(self, benignFilename, anomolyFilename):
        uniquestr = self.genUniqueStr()

        anomalyTag = (anomolyFilename.split("\\nd")[0].split("data\\")[1]).replace("\\", "_")

        return uniquestr + "_" + anomalyTag

    def genUniqueStr(self):
        now = datetime.datetime.now()
        uniquestr = str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.second)
        return uniquestr.replace("\\", "_")

    def run(self):
        print("DEBUG: Autoencoder Running")
        self.startLog()
        print("DEBUG: Running Autoencoder And Generating Model")
        print("DEBUG: UNIQUE RUN NAME" + str(self.uniqueName))
        print("DEBUG: TRAIN FILEPATH:" + self.trainFilename)
        print("DEBUG: ANOMALY FILEPATH:" + self.anomolyFilename)
        print("DEBUG: MODEL FILEPATH:" + self.modelFilename)
        print("DEBUG: LOG FILEPATH:" + self.logFile)

        x_train, x_test, _ = self.autoencoderUtils.getData(False,
                                                           self.trainFilename,
                                                           self.anomolyFilename)
        model = self.getAutoencoderModel(x_train, x_test)

        self.autoencoderUtils.driver(model, '', False,
                                     self.trainFilename,
                                     self.anomolyFilename)
        self.endLog()
        time.sleep(10)

    def runWithModel(self, modelFilename):
        self.startLog()
        x_train, x_test, _ = self.autoencoderUtils.getData(False, self.trainFilename, self.testFilename, self.anomolyFilename)
        model = load_model(modelFilename)
        self.autoencoderUtils.driver(model, 'Non-Federated', False, self.trainFilename, self.testFilename, self.anomolyFilename)
        self.endLog()

    def getAutoencoderModel(self, x_train, x_test, numberEpochs=100,
                            batchSize=128):
        print("DEBUG: Getting Autoencoder Model")

        # number of features
        input_dim = x_train.shape[1]
        # bottle necking the feature
        encoding_dim = int(input_dim / 2)
        hidden_dim = int(encoding_dim / 4)
        input_layer = Input(shape=(input_dim,))

        # NN shape
        encoder = Dense(encoding_dim, activation="tanh",
                        activity_regularizer=regularizers.l1(10e-5))(input_layer)
        encoder = Dense(hidden_dim, activation="relu")(encoder)
        decoder = Dense(encoding_dim, activation='relu')(encoder)
        decoder = Dense(input_dim, activation='tanh')(decoder)

        autoencoder = Model(inputs=input_layer, outputs=decoder)
        autoencoder.compile(optimizer='adam',
                            loss='mean_squared_error',
                            metrics=['accuracy'])

        autoencoder.fit(x_train, x_train, epochs=numberEpochs, batch_size=batchSize, shuffle=True,
                        validation_data=(x_test, x_test), verbose=1)

        # save the auto encoder and then run from it
        autoencoder.save(self.modelFilename)
        autoencoder = load_model(self.modelFilename)
        return autoencoder

    def startLog(self):
        self.old_stdout = sys.stdout
        self.log_file = open(self.logFile, "w")
        # sys.stdout = self.log_file

    def endLog(self):
        sys.stdout = self.old_stdout
        self.log_file.close()
# Name: Kunal Mukherjee
# Personal email: kunmukh@GMAIL.COM
# Date: 8/30/21
# File name: 
# Project name:

from keras.datasets import mnist, fashion_mnist
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from PIL import Image
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from random import shuffle
from sklearn.model_selection import train_test_split
from sklearn.neighbors import LocalOutlierFactor

# Number of samples to show
SAMPLES = 900

class AutoencoderUtils():

    # constructor
    def __init__(self):
        print("DEBUG: AutoencoderUtils init")

    def removeOutliers(self, dataset, percentage, benign):
        print("DEBUG: Removing Outliers")
        print("DEBUG: Dataset Size:" + str(len(dataset)))

        # calculate centerpoint
        centerpoint = []
        for i in range(len(dataset[0])):
            average = 0
            for vector in dataset:
                average += vector[i]
            average = average / len(dataset)
            centerpoint.append(average)
        # print(centerpoint)

        # calculate distances from centerpoint for all vectors in dataset
        distancesFromCenterPoint = []
        for vector in dataset:
            distance = np.linalg.norm(centerpoint - vector)
            distancesFromCenterPoint.append(distance)

        # find 20th percentile cutoff
        sortedDistances = distancesFromCenterPoint.copy()
        sortedDistances.sort()
        cutoffIndex = int(len(dataset) * percentage)
        cutoffLimit = sortedDistances[cutoffIndex]
        print("DEBUG: Distance Cutoff Limit:" + str(cutoffLimit))

        # extract all values below the cutoff limit
        denoisedValues = []
        for vector in dataset:
            distance = np.linalg.norm(centerpoint - vector)
            if distance < cutoffLimit:
                denoisedValues.append(vector)

        # convert list back into numpy form
        finalDenoisedDataset = np.vstack(denoisedValues)
        print("DEBUG: Length of Denoised Data" + str(len(finalDenoisedDataset)))

        return finalDenoisedDataset

    def getData(self, needMINST, fileNameTrain=None, fileNameAbnormal=None):

        if needMINST:
            print("DEBUG: Need MINST")

            # prepare normal dataset (Mnist)
            (x_train, _), (x_test, _) = mnist.load_data()
            x_train = x_train / 255.  # normalize into [0,1]
            x_test = x_test / 255.

            # prapare abnormal dataset (Fashion Mnist)
            (_, _), (x_abnormal, _) = fashion_mnist.load_data()
            x_abnormal = x_abnormal / 255.

            # # reshape input data according to the model's input tensor
            x_train = x_train.reshape(-1, 28 * 28)
            x_test = x_test.reshape(-1, 28 * 28)
            x_abnormal = x_abnormal.reshape(-1, 28 * 28)
        else:
            print("DEBUG: No MINST")

            x_train_df = pd.read_csv(fileNameTrain)
            x_abnormal_df = pd.read_csv(fileNameAbnormal, header=None)

            global SAMPLES

            # x stuff, this gets denoised
            x_train = x_train_df.values

            # x_abnormal stuff
            x_abnormal = x_abnormal_df.values
            # x_abnormal = self.removeOutliers(x_abnormal, 0.5, False)

            SAMPLES = len(x_abnormal)

            print("DEBUG:x_train:" + str(len(x_train)))
            print("DEBUG:x_abnormal:" + str(len(x_abnormal)))

            # combine train and test
            # x = MinMaxScaler().fit_transform(x_train)
            x_train, x_test = train_test_split(x_train, test_size=0.2)

            # denoise x_train here
            x_train = self.removeOutliers(x_train, 0.8, True)
            x_test = self.removeOutliers(x_test, 0.8, True)

        return x_train, x_test, x_abnormal

    # helper function to plot the loss
    # https://www.linkedin.com/pulse/anomaly-detection-autoencoder-neural-network-applied-urls-daboubi/
    def showloss(self, x_test, x_abnormal, model):

        # the entire x set: normal image + abnormal image
        x_concat = np.concatenate([x_test, x_abnormal], axis=0)
        losses = []
        for x in x_concat:
            # compute loss for each test sample
            x = np.expand_dims(x, axis=0)
            loss = model.test_on_batch(x, x)
            losses.append(loss[0])

        # plot
        fig, ax = plt.subplots()

        # plot both the loss
        plt.plot(range(len(losses[:SAMPLES])), losses[:SAMPLES], linestyle='-', linewidth=1, label="normal data",
                 color='blue')
        plt.plot(range(SAMPLES, len(losses)), losses[SAMPLES:], linestyle='-', linewidth=1, label="anomaly data",
                 color='red')

        # create graph
        plt.legend(loc='best')
        plt.grid()
        plt.title("Reconstruction error for different classes")
        plt.ylabel("Reconstruction error")
        plt.xlabel("Data point index")

    def plotLoss(self, autoencoder, X_test, y_test, threshold, modelName):

        tn, fp, fn, tp = 0, 0, 0, 0
        error_df = None

        predictions = autoencoder.predict(X_test)
        mse = np.mean(np.power(X_test - predictions, 2), axis=1)

        '''print(mse)
        print(f"threshold: {threshold}")
        print(f"1st sentence: {threshold - mse[3]} ")
        print(f"2nd sentence: {threshold - mse[4]} ")
        print(f"3rd sentence: {threshold - mse[5]}")'''

        # showImage(X_test.values[101], predictions[101])
        error_df = pd.DataFrame(list(zip(list(mse.values.reshape(1, len(mse))[0]),
                                         list(y_test.values.reshape(1, len(y_test))[0]))),
                                columns=['reconstruction_error', 'true_class'])

        print('\nLoss Test **************************')
        print('threshold', threshold)
        y_pred = [1 if e > threshold else 0 for e in error_df.reconstruction_error.values]
        conf_matrix = confusion_matrix(error_df.true_class, y_pred)


        '''#-----
        path='C:\\Users\\kunmu\\Documents\\Kunal\\gitlab\\autoencoder\\data\\gadget_2021_11_24\\'
        ano_path = path+'all_data_preprocessing_clean.csv'
        ano_path_det = path+'all_data_preprocessing_clean_det.csv'
        ano_path_not_det = path+'all_data_preprocessing_clean_not_det.csv'

        ana_file = open(ano_path, 'r')
        ana_file_det = open(ano_path_det, 'a')
        ana_file_not_det = open(ano_path_not_det, 'a')

        for i, line in enumerate(ana_file):
            if y_pred[i] == 1:
                print(f"DET: {line}")
                ana_file_det.write(line)
            else:
                print(f"NOT DET: {line}")
                ana_file_not_det.write(line)
        #-------'''

        result = conf_matrix.ravel()
        if len(result) == 4:
            tn, fp, fn, tp = result
        else:
            tp = result

        print('TP:' + str(tp))
        print('FP:' + str(fp))
        print('TN:' + str(tn))
        print('FN:' + str(fn))

        precision = 1. * tp / (tp + fp)
        recall = 1. * tp / (tp + fn)
        f1 = (2 * recall * precision) / (recall + precision)

        accuracy = 1. * (tp + tn) / (tp + tn + fp + fn)

        print('Accuracy:' + str(accuracy))
        print('Precision:' + str(precision))
        print('Recall:' + str(recall))
        print('F1:' + str(f1))

        print("DEBUG:x_test plot loss:" + str(len(X_test)))

        groups = error_df.groupby('true_class')

        # plot the loss
        fig, ax = plt.subplots()

        for name, group in groups:
            ax.plot(group.index, group.reconstruction_error, marker='o', ms=2, linestyle='',
                    label="Abnormal data" if name == 1 else "Normal data", color='red' if name == 1 else 'orange')
        ax.hlines(threshold, ax.get_xlim()[0], ax.get_xlim()[1], colors="green",
                  zorder=100, label='Threshold=' + str(np.round(threshold, 3)))
        ax.legend()
        plt.title(modelName + " Reconstruction error| Accuracy= " + str(accuracy))
        plt.ylabel("Reconstruction error")
        plt.xlabel("Data point index")

    def getThreasholdTrain(self, autoencoder, X, y_test, modelName):

        predictions = autoencoder.predict(X)
        mse = np.mean(np.power(X - predictions, 2), axis=1)

        PERCENTILE = 0.99  # 0.9900
        threshold = np.quantile(mse, PERCENTILE)

        # showImage(X_test.values[101], predictions[101])
        error_df = pd.DataFrame(list(zip(list(mse.values.reshape(1, len(X))[0]),
                                         list(y_test.values.reshape(1,len(X))[0]))),
                                columns=['reconstruction_error', 'true_class'])

        y_pred = [1 if e > threshold else 0 for e in error_df.reconstruction_error.values]

        conf_matrix = confusion_matrix(error_df.true_class, y_pred)

        result = conf_matrix.ravel()
        if len(result) == 4:
            tn, fp, fn, tp = result
        else:
            tp = result

        print('\nLoss Train **************************')
        print('TP:' + str(tp))
        print('FP:' + str(fp))
        print('TN:' + str(tn))
        print('FN:' + str(fn))
        accuracy = 1. * (tp + tn) / (tp + tn + fp + fn)

        groups = error_df.groupby('true_class')

        # plot the image
        fig, ax = plt.subplots()

        for name, group in groups:
            ax.plot(group.index, group.reconstruction_error, marker='o', ms=2, linestyle='',
                    label="Abnormal data" if name == 1 else "Normal data", color='red' if name == 1 else 'orange')
        ax.hlines(threshold, ax.get_xlim()[0], ax.get_xlim()[1], colors="green",
                  zorder=100, label='Threshold=' + str(np.round(threshold, 3)))
        ax.legend()
        plt.title(modelName + " Reconstruction error| Accuracy= " + str(accuracy))
        plt.ylabel("Reconstruction error")
        plt.xlabel("Data point index")

        return threshold

    def driver(self, model, modelName, MINSTData, train, ano):

        if MINSTData:
            X_train, x_test, x_abnormal = self.getData(True)
        else:
            X_train, x_test, x_abnormal = self.getData(False, train, ano)

        #x_test = x_test[:len(x_abnormal)]

        # get the 80th percentile of the train threshold
        # get the threshold that will give 80% training accuracy
        threshold = self.getThreasholdTrain(model,
                                       pd.DataFrame(X_train),
                                       pd.DataFrame([0 for _ in range(len(X_train))]),
                                       modelName)

        X_test = pd.DataFrame(np.concatenate([x_test, x_abnormal], axis=0))
        Y_test = pd.DataFrame([0 for _ in range(len(x_test))]+[1 for _ in range(len(x_abnormal))])


        # plot the mse loss of X test using the given mse threshold
        self.plotLoss(model, X_test, Y_test, threshold, modelName)

        print('\n\nThreshold', threshold)

        plt.show()
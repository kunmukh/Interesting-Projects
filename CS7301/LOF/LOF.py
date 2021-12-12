# Name: Kunal Mukherjee
# Email: kunmukh@gmail.com
# Date: 11/23/2021
# Project: 

import logging

# help: https://towardsdatascience.com/anomaly-detection-with-local-outlier-factor-lof-d91e41df10f2
# data preparation
import pandas as pd
import numpy as np

# data visualzation
import matplotlib.pyplot as plt

# outlier/anomaly detection
from sklearn.neighbors import LocalOutlierFactor
from sklearn.metrics import confusion_matrix

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s | %(levelname)s\t| %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

# base file location
base = "C:\\Users\\kunmu\\Documents\\Kunal\\prov-ng-proj\\eval-result\\data-backup\\"
benign_path = base+"anomaly\\benign-fv-attack.csv"
anomaly_path = base+"anomaly\\anomaly-fv-attack.csv"
gadget_path = base+"gadget1-data-exfil\\anomaly-gadget-fv.csv"


def printStat(CONFUSION_MATRIX):

    result = CONFUSION_MATRIX.ravel()
    if len(result) == 4:
        tn, fp, fn, tp = result
    else:
        tp = result

    precision = 1. * tp / (tp + fp)
    recall = 1. * tp / (tp + fn)
    f1 = (2 * recall * precision) / (recall + precision)
    accuracy = 1. * (tp + tn) / (tp + tn + fp + fn)

    log.info('TP:' + str(tp))
    log.info('FP:' + str(fp))
    log.info('TN:' + str(tn))
    log.info('FN:' + str(fn))
    log.info('Accuracy:' + str(accuracy))
    log.info('Precision:' + str(precision))
    log.info('Recall:' + str(recall))
    log.info('F1:' + str(f1))
    log.info("\n\n")


def filter_outlier(DF_BENIGN_DATA):
    outlier_frac = 0.001
    model = LocalOutlierFactor(contamination=outlier_frac)
    pred = model.fit_predict(DF_BENIGN_DATA)

    inlier_ind = np.where(pred==1)
    inlier_val = DF_BENIGN_DATA.iloc[inlier_ind]

    return pd.DataFrame(inlier_val)


def main():
    log.info(f"benign path: {benign_path}")
    log.info(f"anomaly path: {anomaly_path}")
    log.info(f"gadget path: {gadget_path}")

    df_ben = pd.read_csv(benign_path, header=None)
    df_ana = pd.read_csv(anomaly_path, header=None)
    df_gat = pd.read_csv(gadget_path, header=None)

    # benign data
    df_ben_processed = filter_outlier(df_ben)

    # model specification
    model1 = LocalOutlierFactor(novelty=True, contamination=0.04) 
    model1.fit(df_ben_processed)

    pred1 = model1.predict(df_ben_processed)
    pred2 = model1.predict(df_ana)
    pred3 = model1.predict(df_gat)

    ret1 = (pred1 == 1).sum() / len(pred1)
    ret2 = (pred2 == 1).sum() / len(pred2)
    ret3 = (pred3 == 1).sum() / len(pred3)

    # log.info(outlier_index)
    log.info(f"ret1: {ret1} ret2: {ret2} ret3: {ret3}")

    # for anomaly
    y_pred_ana = (pred2 == 1)
    y_true_ana = [1 for i in range(len(y_pred_ana))]
    printStat(confusion_matrix(y_true_ana, y_pred_ana))

    # for gadget
    y_pred_gad = (pred3 == 1)
    y_true_gad = [1 for i in range(len(y_pred_gad))]
    printStat(confusion_matrix(y_true_gad, y_pred_gad))


if __name__ == '__main__':
    main()

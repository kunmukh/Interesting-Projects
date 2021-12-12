# Name: Kunal Mukherjee
# Personal email: kunmukh@GMAIL.COM
# Date: 8/30/21
# File name: 
# Project name:

import os
from Autoencoder import Autoencoder
import logging

# base file location
base = "C:\\Users\\kunmu\\Documents\\Kunal\\gitlab\\autoencoder\\data\\"

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s | %(levelname)s\t| %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


def main():

    log.info("DEBUG: PID:", os.getpid())
    log.info("DEBUG: DIRECTORY:" + str(os.listdir()))

    benign = base+"benign\\benign_WIN\\benign-fv.csv"
    anomaly = base + "anomaly_2021_11_11\\anomaly-fv.csv"

    autoencoder_a = Autoencoder(benign, anomaly)
    autoencoder_a.run()

    benign = base+"benign\\benign_WIN\\benign-fv.csv"
    gadget = base + "anomaly_2021_11_11\\gadget-fv.csv"

    autoencoder_g = Autoencoder(benign, anomaly)
    autoencoder_g.run()


if __name__ == '__main__':
    main()

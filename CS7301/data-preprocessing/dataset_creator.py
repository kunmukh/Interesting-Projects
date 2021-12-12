# Name: Kunal Mukherjee
# Email: kunmukh@gmail.com
# Date: 11/17/2021
# Project:

# import
import glob
import logging
import pandas as pd
import re
from ntpath import basename

# logging set up
# set up logging variables
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s | %(levelname)s\t| %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

# import path
ROOT = "C:\\Users\\kunmu\\Documents\\Kunal\\gitlab\\autoencoder\\data\\"
GADGET_PATH = "gadget_2021_11_24\\"

APPS = ['EXCEL.EXE', 'EXPLORER.EXE', 'ACRORD32', 'ADOBE', '445', '443', 'OSQL.EXE', 'NETSH.EXE']

def getCSVfile(PATH, PATTERN):
    csvFiles = []

    for filename in glob.iglob(f"{PATH}**/*.*", recursive=True):
        # todo: replace crimson_test
        if filename.__contains__(PATTERN):
            # log.info(f"mapdb path: {filename}")
            csvFiles.append(filename)

    return csvFiles


def processLine(LINE):
    try:
        line = LINE.strip('\n')
        line = line.replace("<--", "&").replace("[InetChannel]", "").replace("[Process]", "").replace("[File]", "")
        line = re.sub(r'\([^()]*\)', '', line)

        # split the line based on '&'
        line = re.split('&', line)
        line = [l.strip() for l in line]
        line = [basename(l) for l in line]

        line = " ".join(line)

        return line
    except AttributeError:
        return ""


def writeFile(LINE, FILE):

    new_line = processLine(LINE)

    try:
        csvfile = open(FILE, 'r')
        loglist = csvfile.readlines()
        csvfile.close()

        for line in loglist:
            if new_line in line:
                return False

        logfile = open(FILE, 'a')
        logfile.write(new_line + "\n")
        logfile.close()

        return True
    except FileNotFoundError:
        logfile = open(FILE, 'a')
        logfile.write(new_line + "\n")
        logfile.close()

        return True
    except UnicodeEncodeError:
        return False


def getLines(CSV_FILE, OUTPUT_FILE, isBENIGN):

    log.info(f"WORKING ON {CSV_FILE}")
    log.info(f"OUTPUT ON {OUTPUT_FILE}")

    df = pd.read_csv(CSV_FILE, index_col=False, error_bad_lines=False)

    # get the path
    log.info(f"Len of Paths:{len(df[' Actual Path'].values[:-1])}")
    actual_paths = df[' Actual Path'].values[:-1]

    # if benign dataset
    if isBENIGN:
        actual_paths = actual_paths[::-1]

    if len(actual_paths) < 500:
        _val_20_perccent = 0.2 * len(actual_paths)
    elif len(actual_paths) < 1000:
        _val_20_perccent = 0.1 * len(actual_paths)
    elif len(actual_paths) < 10000:
        _val_20_perccent = 0.01 * len(actual_paths)
    else:
        _val_20_perccent = 500

    lin_cnt = 0
    indx = 0

    while lin_cnt < _val_20_perccent and indx < len(actual_paths):

        if writeFile(actual_paths[indx], OUTPUT_FILE):
            lin_cnt += 1

        indx += 1


def makeAllCSV(PATH):
    csvFiles = getCSVfile(f"{PATH}", "data_preprocessing_clean.csv")
    for csvFile in csvFiles:
        log.info(f"WORKING ON: {csvFile}")
        outPath = f"{PATH}all_data_preprocessing_clean.csv"

        f = open(csvFile, 'r')
        loglist = f.readlines()
        f.close()

        for line in loglist:
            writeFile(line, outPath)


def main():

    for app in APPS:
        path = f"{ROOT}{GADGET_PATH}{app}\\"
        csvFiles = getCSVfile(path, "path_score.csv")

        for csvFile in csvFiles:
            outPath = f"{ROOT}{GADGET_PATH}{app}\\data_preprocessing_clean.csv"
            getLines(csvFile, outPath, False)

    makeAllCSV(f"{ROOT}{GADGET_PATH}")


if __name__ == '__main__':
    main()
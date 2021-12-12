# Name: Kunal Mukherjee
# Personal email: kunmukh@GMAIL.COM
# Date: 11/12/21
# File name:
# Project name:

import logging
import glob
import pandas as pd
import numpy as np
from ntpath import basename


# set up logging variables
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s | %(levelname)s\t| %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

# GLOBAL PATHS
root = "C:\\Users\\kunmu\\Documents\\Kunal\\gitlab\\prov-ng-kunal\\scripts\\find-gadget\\"
DB_PATH = root + "data\\mapdbs_txt\\"
P2P_REL_PATH = root + "data\\tmp\\p2p_rel.csv"
TRANS_MAT_PATH = root + "data\\tmp\\trans_mat.csv"
ORG_PATH = root + "data\\org_path.txt"

EDGE_THRESHOLD = 0.3
GADGET_SELECT_THRES = 0.4
MAX_GADGET_LEN = 20


# get the list of mapdbs
def getListMapDBs(DB_PATH, PATTERN):

    mapdb_path = []

    for filename in glob.iglob(f"{DB_PATH}**/*.*", recursive=True):
        # todo: replace crimson_test
        if filename.__contains__(PATTERN): # crimson_test # csv.sort.csv
            # log.info(f"mapdb path: {filename}")
            mapdb_path.append(filename)

    return mapdb_path


# get the process2process matrix
def process2processRelMatrix(MAPDB_PATH_ARR):

    p2p_df = pd.DataFrame(columns=['src', 'dst', 'rel', 'cnt'])

    # for every mapdb path make this relationship matrix
    for mapdb_path in MAPDB_PATH_ARR:
        log.info(f"WORKING ON: {mapdb_path}")
        df = pd.read_csv(mapdb_path)

        for index, row in df.iterrows():

            # only consider process
            if 'Start_Processlet' in row['relationship']:
                # log.info(f"relationship: {row['relationship']}")
                # log.info(f"relationship: {row['count']}")

                _rel = str(row['relationship']).split("Start_Processlet")

                check_row = p2p_df.loc[(p2p_df['src'] == basename(_rel[0])) &
                                      (p2p_df['dst'] == basename(_rel[1])) &
                                      (p2p_df['rel'] == 'Start_Processlet')]

                # check if a row exist
                # if not exist append the row
                # else increase the count
                if check_row.empty:
                    p2p_df = p2p_df.append({'src': basename(_rel[0]),
                                            'dst': basename(_rel[1]),
                                            'rel': 'Start_Processlet',
                                            'cnt': row['count']}, ignore_index=True)
                else:
                    p2p_df.loc[(p2p_df['src'] == basename(_rel[0])) & (p2p_df['dst'] == basename(_rel[1])) & (
                                p2p_df['rel'] == 'Start_Processlet'), ['cnt']] = check_row['cnt'] + row['count']


    p2p_df.to_csv(P2P_REL_PATH, index=False)

    return p2p_df


# get the frequency
def getFreq(p2p_rel_df, src, rel, dst=None):

    if dst is not None:
        check_row = p2p_rel_df.loc[(p2p_rel_df['src'] == src) &
                                   (p2p_rel_df['dst'] == dst) &
                                   (p2p_rel_df['rel'] == rel)]

        return float(check_row['cnt'].sum())
    else:
        check_rows = p2p_rel_df.loc[(p2p_rel_df['src'] == src) &
                                   (p2p_rel_df['rel'] == rel)]

        return float(check_rows['cnt'].sum())


# get the transitional matrix
def transitionMatrix():
    p2p_rel_df = pd.read_csv(P2P_REL_PATH)

    # get all the src and dst process
    proc_src = p2p_rel_df['src'].unique()
    proc_dst = p2p_rel_df['dst'].unique()

    # get the lst of all unique processes
    procs = [x for x in list({*proc_src, *proc_dst}) if x == x]
    procs = sorted(procs)

    log.info(f"PROC IN SYS: {len(procs)}")

    # create the transition matrix
    trans_mat_df = pd.DataFrame(columns=procs)
    p2p_rel_df = pd.read_csv(P2P_REL_PATH)

    for i, src_proc in enumerate(procs):
        log.info(f"WORKING ON PROCESS: {src_proc}: {i}/{len(procs)}")
        row = []

        for dst_proc in procs:
            # id src and st same then prob is 1.0
            if src_proc is dst_proc:
                prob = 1.0
            else:
                freq_src_rel = getFreq(p2p_rel_df, src_proc, 'Start_Processlet')
                freq_src_dst_rel = getFreq(p2p_rel_df, src_proc, 'Start_Processlet', dst_proc)

                # if src is not creating proc
                # the freq is 0 but making that would make
                # the regulatory score calculation to be 0
                # which we dont want, it should be low but not 0
                if freq_src_rel == 0 or freq_src_dst_rel == 0:
                    prob = 0.002
                else:
                    prob = freq_src_dst_rel / freq_src_rel
            row.append(prob)

        # log.info(f"prob:{i}:{src_proc}:{row}")
        trans_mat_df.loc[len(trans_mat_df)] = row

    trans_mat_df.to_csv(TRANS_MAT_PATH, index=False)

    return trans_mat_df


# get the transition probability
def getTransProb(src, dst, all=None):
    trans_mat_df = pd.read_csv(TRANS_MAT_PATH)
    procs = list(trans_mat_df.columns)

    if all is None:
        # get the source process index
        src_indx = procs.index(src)

        # get the transition probability
        # select the col dst and then chose the src index
        trans_prob = trans_mat_df[dst][src_indx]

        return trans_prob

        # log.info(f"{src}:{dst}:{trans_prob}")
    else:
        trans_probs = trans_mat_df[dst]

        return procs, trans_probs


# get the score of the path
def getScorePath(PROC_ARR):

    # regulatory score
    rs = 1.0

    for i, p in enumerate(PROC_ARR[:-1]):
        src_p = p
        dst_p = PROC_ARR[i + 1]

        rs *= getTransProb(src_p, dst_p)

    # anomaly score is 1 - rs
    return 1 - rs


# get the rare relation
def findRareRel(PROC_ARR):

    ral_rel =[]

    for i, p in enumerate(PROC_ARR[:-1]):
        src_p = p
        dst_p = PROC_ARR[i + 1]

        prob = getTransProb(src_p, dst_p)

        if prob < EDGE_THRESHOLD:
            log.info(f"RARE EDGE: src:{src_p}:dst:{dst_p}:prob:{prob}")
            ral_rel.append([src_p, dst_p])

    return ral_rel


# send gadget seq from nested list path
_gadget_helper_list = []
def getGadgetSeqPrint(path):
    global _gadget_helper_list

    if type(path) == list:
        for p in path:
            if type(p) == list:
                getGadgetSeqPrint(p)
            else:
                _gadget_helper_list.append(p)
    else:
        _gadget_helper_list.append(path)


# get gadget
def getGadget(OLD_SRC, DST_PROC):

    gadgets = []

    # get the process and their transition probability
    procs, tran_prob = getTransProb(None, DST_PROC, 'all')

    # get the process that has higher trans probability
    for idx, p in enumerate(procs):
        if (p != DST_PROC) and (p != OLD_SRC):
            if tran_prob[idx] > GADGET_SELECT_THRES:
                gadgets.append(p)

    return gadgets


# recursively find gadget
def recFindGadget(gadget, INTRO_GADGET, len):

    # length
    if len == MAX_GADGET_LEN:
        return []
    # base case
    if gadget == INTRO_GADGET:
        return [gadget]
    # recursive case
    else:
        gadgets = getGadget(gadget, gadget)

        poss_path = []
        # if gadget found
        # for all gadget append the new gadget
        if gadgets:
            for g in gadgets:
                try:
                    poss_path.append([gadget, recFindGadget(g, INTRO_GADGET, len+1)[0]])
                except IndexError:
                    return []
            return poss_path
        else:
            return poss_path


# replace the rare edge with gadget
# the gadget replace algorithm
def replaceGADGET(PROCS, RARE_RELS):
    global _gadget_helper_list
    gadget_rep_path = {}

    # for each rare rel
    for rel in RARE_RELS:
        intro = PROCS[:PROCS.index(rel[1])]
        payload = PROCS[PROCS.index(rel[1]):]

        log.info(f"INTRO GADGET:{intro} PAYLOAD GADGET:{payload}")

        # find the first gadget
        if len(payload) > 1:
            gadgets = getGadget(payload[0], payload[1])
        else:
            gadgets = getGadget(payload[0], payload[0])

        # if first gadget found
        if gadgets:
            # for the gadgets in gadget
            for i, gadget in enumerate(gadgets):
                log.info(f"TRYING TO FIND PATH FROM PAYLOAD GADGET {rel[0]} ->...-> {gadget} -> {payload[-1]}: {i+1}/{len(gadgets)}")

                poss_gadget_path = recFindGadget(gadget, intro[-1], 0)

                if poss_gadget_path:
                    for path in poss_gadget_path:

                        # log.info(f"RAW GADGET PATH: {path}")
                        _gadget_helper_list = []

                        getGadgetSeqPrint(path)

                        _gadget_helper_list.reverse()
                        gadget_seq = _gadget_helper_list

                        # add the rel and gadget sequence
                        gadget_path = intro + gadget_seq[1:] + payload[1:]
                        gadget_rep_path[rel[0]] = gadget_path
                        log.info(f"GADGET PATH: FOUND for RARE EDGE: src:{rel[0]}:dst:{rel[1]} --> {gadget_seq}")
                        log.info(f"GADGET PATH: score: {getScorePath(gadget_path)}: {' PROC_CREATE '.join(gadget_path)}")
                else:
                    gadget_rep_path[rel[0]] = []
                    log.info(f"GADGET PATH: NOT FOUND for RARE EDGE: src:{rel[0]}:dst:{rel[1]}")

        else: # if not found
            gadget_rep_path[rel[0]] = []
            log.info(f"GADGET PATH: NOT FOUND for RARE EDGE: src:{rel[0]}:dst:{rel[1]}")

    return gadget_rep_path


# function to start the replace
def replacePath(PATH):
    file = open(PATH, 'r')

    for path in file:
        # get the processes from the path
        proc_arr = [basename(p.strip()) for p in path.split("PROC_CREATE")]
        proc_arr.reverse()

        # original score of the path
        log.info(f"ORG PATH: score: {getScorePath(proc_arr)}: {' PROC_CREATE '.join(proc_arr)}")

        # get the edges that are rare relation
        attack_edges = findRareRel(proc_arr)

        # replace the rare edge with common edge
        gadget_procs = replaceGADGET(proc_arr, attack_edges)

        for gadget_proc in gadget_procs:

            if not gadget_proc:
                # new score of the gadget replaced path
                log.info(f"GADGET PATH: score: {getScorePath(gadget_proc)}: {' PROC_CREATE '.join(gadget_proc)}")


def main():
    mapdbs = getListMapDBs(DB_PATH, "crimson_test") # "csv.sort.csv" # crimson_test

    # create process to process relation matrix
    process2processRelMatrix(mapdbs)

    # create a transition matrix for the processes
    transitionMatrix()

    # call the func to replace the path
    replacePath(ORG_PATH)
    




if __name__ == '__main__':
    main()
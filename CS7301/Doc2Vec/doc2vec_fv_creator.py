# Name: Kunal Mukherjee
# Personal email: kunmukh@GMAIL.COM
# Date: 6/28/21
# File name: 
# Project name:

# help:
# https://radimrehurek.com/gensim/auto_examples/tutorials/run_doc2vec_lee.html

import logging
import gensim
import smart_open
import csv

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# base file location
base = "C:\\Users\\kunmu\\Documents\\Kunal\\gitlab\\autoencoder\\data\\"

# training input and output file location
train_file= base+"benign\\benign_WIN\\all_data_preprocessing_clean.csv"
output_beng_train= base+"benign\\benign_WIN\\benign-fv.csv"

# anomalous input and output file location
anomolus_file= base+"gadget_2021_11_24\\all_data_preprocessing_clean.csv"
output_ana=base+"gadget_2021_11_24\\anomaly-gadget-fv.csv"


# model store/load location
model_out_f= "C:\\Users\\kunmu\\Documents\\Kunal\\gitlab\\autoencoder\\models\\doc2vec\\doc2vec.bin"

HEADER = [i for i in range(50)]


# preprocessing the data
def read_corpus(fname, tokens_only=False):
    with smart_open.open(fname, encoding="iso-8859-1") as f:
        for i, line in enumerate(f):
            tokens = gensim.utils.simple_preprocess(line)
            if tokens_only:
                yield tokens
            else:
                # For training data, add tags
                yield gensim.models.doc2vec.TaggedDocument(tokens, [i])


def main():

    # training, testing, anomalous corpus
    train_corpus = list(read_corpus(train_file))
    train_corpus_token = list(read_corpus(train_file, tokens_only=True))
    ano_corpus_token = list(read_corpus(anomolus_file, tokens_only=True))

    # load a model - I
    # model = gensim.models.doc2vec.Doc2Vec.load(model_out_f)

    # or build a model
    # model initialization - I
    model = gensim.models.doc2vec.Doc2Vec(vector_size=50, min_count=1,
                                          epochs=10, dm=1, workers=1)
    model.build_vocab(train_corpus)

    # model train - II
    model.train(train_corpus, total_examples=model.corpus_count,
                epochs=model.epochs)

    # save the model - III
    model.save(model_out_f)

    # infer the feature vector and write to file
    with open(output_beng_train, "w", newline='') as file1:
        employee_writer = csv.writer(file1, delimiter=',',
                                     quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # employee_writer.writerow(HEADER)
        for t in train_corpus_token:
            fv = model.infer_vector(t)
            employee_writer.writerow(fv)

    with open(output_ana, "w", newline='') as file3:
        employee_writer = csv.writer(file3, delimiter=',',
                                     quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # employee_writer.writerow(HEADER)
        for t in ano_corpus_token:
            fv = model.infer_vector(t)
            employee_writer.writerow(fv)


if __name__ == '__main__':
    main()
#!/usr/bin/python

import cPickle, pickle
import numpy
import re
import sys

from time import time

# from sklearn import cross_validation
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectPercentile, f_classif

from sklearn.feature_extraction.text import CountVectorizer



def preprocess(words_file='../word_data.pkl', context_file='../context_data.pkl'):

    context_file_handler = open(context_file, "r")
    context_data = cPickle.load(context_file_handler)
    context_file_handler.close()

    words_file_handler = open(words_file, "r")
    word_data = cPickle.load(words_file_handler)
    words_file_handler.close()


    features_train, features_test, labels_train, labels_test = train_test_split(word_data, context_data, test_size=0.1, random_state=42)

    vectorizer = CountVectorizer(ngram_range=(1, 2), min_df=1)
    # vectorizer = TfidfVectorizer(sublinear_tf=True, ngram_range=(1, 2), max_df=0.3)

    features_train_transformed = vectorizer.fit_transform(features_train)
    features_test_transformed  = vectorizer.transform(features_test)

    # selector = SelectPercentile(f_classif, percentile=100)
    # selector.fit(features_train_transformed, labels_train)
    # features_train_transformed = selector.transform(features_train_transformed).toarray()
    # features_test_transformed  = selector.transform(features_test_transformed).toarray()


    return features_train_transformed, features_test_transformed, labels_train, labels_test



# from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.metrics import accuracy_score
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC

features_train, features_test, labels_train, labels_test = preprocess()



def One_Vs_Rest_Clf(features_train, labels_train, features_test, labels_test):


    clf = OneVsRestClassifier(LinearSVC(random_state=0))

    t0 = time()
    clf.fit(features_train, labels_train)
    print "training time:", round(time()-t0, 3), "s"


    pred = clf.predict(features_test)

    accuracy = accuracy_score(pred, labels_test)

    return accuracy



print One_Vs_Rest_Clf(features_train, labels_train, features_test, labels_test)











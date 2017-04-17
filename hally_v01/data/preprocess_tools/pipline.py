import cPickle, sys
from sklearn.externals import joblib
from sklearn.pipeline import make_pipeline

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier


def create_pipeline(word_data_file='../word_data.pkl', label_data_file='../context_data.pkl'):

    context_file_handler = open(label_data_file, "r")
    label_data = cPickle.load(context_file_handler)
    context_file_handler.close()

    words_file_handler = open(word_data_file, "r")
    word_data = cPickle.load(words_file_handler)
    words_file_handler.close()

    vec = TfidfVectorizer(ngram_range=(1, 3), min_df=1)
    clf = OneVsRestClassifier(LinearSVC(random_state=0))

    clf_pipe = make_pipeline(vec, clf)

    clf_pipe.fit(word_data, label_data)

    joblib.dump({'class1': clf_pipe}, '../data_models', compress=9)


if __name__ == '__main__':
    if sys.argv:
        if sys.argv[1] == "makenew":
            from time import time
            t0 = time()
            create_pipeline()
            print "time to complete", round(time()-t0, 8), "s"
            print "~" * 40
            print "\nnew data model made\n"
            print "~" * 40
    else:
        print "~" * 40
        print "\nNeed args\n"
        print "~" * 40


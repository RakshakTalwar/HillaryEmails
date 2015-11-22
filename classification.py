"""
Copyright (c) 2015
Authors: Majid Latif and Rakshak Talwar

Cluster Hillary's emails
"""

import csv
import json
import pandas as pd
import sys, getopt, pprint
import sys
import sklearn
import nltk.stem
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn.datasets import load_files
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from pymongo import MongoClient

if __name__ == "__main__":

  movie_reviews_data_folder = 'txt_sentoken'
  dataset = load_files(movie_reviews_data_folder, shuffle=False)


  # split the dataset in training and test set:
  docs_train, docs_test, y_train, y_test = train_test_split(dataset.data, dataset.target, test_size=0.25, random_state=None)

  english_stemmer = nltk.stem.SnowballStemmer('english')
  # create a class for the TfidfVectorizer to incorporate stemming
  class StemmedTfidfVectorizer(TfidfVectorizer):
    def build_analyzer(self):
      analyzer = super(StemmedTfidfVectorizer, self).build_analyzer()
      return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))


  pipeline = Pipeline([('vect', StemmedTfidfVectorizer(min_df=1)),('clf', LinearSVC(C=1000)),])

  # TASK: Build a grid search to find out whether unigrams or bigrams are
  # more useful.
  # Fit the pipeline on the training set using grid search for the parameters
  parameters = { 'vect__ngram_range': [(1, 1), (1, 2)],}
  grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1)
  grid_search.fit(docs_train, y_train)

  # TASK: print the cross-validated scores for the each parameters set
  # explored by the grid search
  print(grid_search.grid_scores_)
  print 'here'

  # TASK: Predict the outcome on the testing set and store it in a variable
  # named y_predicted
  y_predicted = grid_search.predict(docs_test)

  # Print the classification report
  print(metrics.classification_report(y_test, y_predicted,
                                        target_names=dataset.target_names))

  # Print and plot the confusion matrix
  cm = metrics.confusion_matrix(y_test, y_predicted)
  print(cm)



#mon_client = MongoClient('sabre_webserver.cloudapp.net', 27017)
#
#csvfile = open('Emails.csv')
#reader = csv.DictReader( csvfile )
#mongo_client=MongoClient()
#db=mongo_client.october_mug_talk
#db.segment.drop()
#header = ["Id", "DocNumber", "MetadataSubject", "MetadataTo", "MetadataFrom", "SenderPersonId", "MetadataDateSent", "MetadataDateReleased", "MetadataPdfLink", "MetadataCaseNumber", "MetadataDocumentClass", "ExtractedSubject", "ExtractedTo", "ExtractedFrom", "ExtractedCc", "ExtractedDateSent", "ExtractedCaseNumber", "ExtractedDocNumber", "ExtractedDateReleased", "ExtractedReleaseInPartOrFull", "ExtractedBodyText", "RawText"];

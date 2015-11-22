"""
Copyright (c) 2015
Authors: Majid Latif and Rakshak Talwar

Cluster Hillary's emails
"""

import csv, json, sys, getopt, pdb, pprint
import pandas as pd
import nltk.stem
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn.datasets import load_files
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from pymongo import MongoClient

### global instantiations
english_stemmer = nltk.stem.SnowballStemmer('english')
# create a class for the TfidfVectorizer to incorporate stemming
class StemmedTfidfVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedTfidfVectorizer, self).build_analyzer()
        return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))

# create the mongo connection
mon_con = MongoClient('localhost', 27017) # NOTE: change to localhost when running on server
mon_col = mon_con['hillary']['emails']

### load in training data
movie_reviews_data_folder = 'txt_sentoken'
rev_dataset = load_files(movie_reviews_data_folder, shuffle=False)

# split the movie reviews dataset into a train and test set
rev_X_train, rev_X_test, rev_y_train, rev_y_test = train_test_split(rev_dataset.data, rev_dataset.target, test_size=0.25, random_state=None)

pipeline = Pipeline( [ ('vect', StemmedTfidfVectorizer(min_df=1, stop_words = 'english')), ('clf', LinearSVC(C=1000)) ] )

# TASK: Build a grid search to find out whether unigrams or bigrams are
# more useful.
# Fit the pipeline on the training set using grid search for the parameters
parameters = { 'vect__ngram_range': [(1, 1), (1, 2)] }
grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1)
grid_search.fit(rev_X_train, rev_y_train)

# TASK: print the cross-validated scores for the each parameters set
# explored by the grid search
#print(grid_search.grid_scores_)

### load in Hillary's emails, run predictions, store classifications to mongo

emails = [] # a list of dicts, each contains an email string, Mongo ObjectId, and predicted classification score
for email in mon_col.find({}, {'RawText' : 1, '_id' : 1}):
    pdb.set_trace()
    classification = grid_search.predict([email['RawText']])
    emails.append( { 'text' : email['RawText'], '_id' : email['_id'], 'classification' : classification } )

# update the mongo collection
for email_dict in emails:
    pdb.set_trace()
    mon_col.update({"_id" : email_dict['_id']}, {"$set" : {"classification" : email_dict['classification']}})

# TASK: Predict the outcome on the testing set and store it in a variable
# named y_predicted

# Print the classification report
#print(metrics.classification_report(rev_y_test, y_predicted, target_names=dataset.target_names))
# Print and plot the confusion matrix
#cm = metrics.confusion_matrix(y_test, y_predicted)
#print(cm)


#csvfile = open('Emails.csv')
#reader = csv.DictReader( csvfile )
#mongo_client=MongoClient()
#db=mongo_client.october_mug_talk
#db.segment.drop()
#header = ["Id", "DocNumber", "MetadataSubject", "MetadataTo", "MetadataFrom", "SenderPersonId", "MetadataDateSent", "MetadataDateReleased", "MetadataPdfLink", "MetadataCaseNumber", "MetadataDocumentClass", "ExtractedSubject", "ExtractedTo", "ExtractedFrom", "ExtractedCc", "ExtractedDateSent", "ExtractedCaseNumber", "ExtractedDocNumber", "ExtractedDateReleased", "ExtractedReleaseInPartOrFull", "ExtractedBodyText", "RawText"];

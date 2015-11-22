"""
Copyright (c) 2015 Rakshak Talwar
Author: Rakshak Talwar

Cluster Hillary's emails
"""

import pymongo
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import nltk.stem
import pdb

### begin global instantiations

# create a class for the TfidfVectorizer to incorporate stemming
class StemmedTfidfVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedTfidfVectorizer, self).build_analyzer()
        return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))

vectorizer = StemmedTfidfVectorizer(min_df=1, stop_words='english', decode_error='ignore', strip_accents='ascii') # the vectorizer used to product the bag of words

def get_word_bag(text_dicts):
    """Pass it a list of dictionaries. Each dictionary contains the email's text and Mongo ObjectId.Receive a bag-of-words"""
    """We return both bag_of_words and ObjectIds list together as a dict to help preserve indices, otherwise any
    issues with the original urls may cause misaligned indices."""

    # generate the bag of words
    corpus = [item['text'] for item in text_dicts] # create a list of purely text
    bag_of_words = vectorizer.fit_transform(corpus) # fits the model and then transforms to bag of words

    # return the bag_of_words and urls
    return {'bag_of_words' : bag_of_words, 'ids' : [item['_id'] for item in text_dicts]}

# capture emails from Mongo
mon_col = pymongo.MongoClient('localhost', 27017)['hillary']['emails']

### end global instantiations

# grab data from Mongo
all_emails = [] # list will contain dicts with each dict containing the raw text and the Mongo ObjectId
for email in mon_col.find({}, {'RawText' : 1, '_id' : 1}):
    all_emails.append({'text' : email['RawText'], '_id' : email['_id']})

# create a bag of words
word_bag = get_word_bag(all_emails)

# create the model
n_clusters = 3
km = KMeans(n_clusters=n_clusters, init='k-means++', n_init=1, verbose=1)
# fit the model
km.fit(word_bag)

# store the clusters in a way which is relatable with the original database
clusters = defaultdict(list)
pdb.set_trace()
for o,i in enumerate(km.labels_):
    clusters[i].append(' ')

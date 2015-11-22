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
import pdb, re

### begin global instantiations
english_stemmer = nltk.stem.SnowballStemmer('english')
# create a class for the TfidfVectorizer to incorporate stemming
class StemmedTfidfVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedTfidfVectorizer, self).build_analyzer()
        return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))

vectorizer = StemmedTfidfVectorizer(min_df=1, stop_words='english', decode_error='ignore', strip_accents='ascii') # the vectorizer used to product the bag of words

whitespace_pattern = re.compile(r'(\\\w{1}|( ){2,})') # regex pattern used to remove whitespace characters (e.g. \n) snd any whitespace consisting of more than one space (e.g. '   ')
non_alpha_num_pattern = re.compile(r'[^0-9a-zA-Z( )]+') # regex pattern used to remove non-alphanumeric characters and spaces

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
    # clean the text
    clean_text = re.sub(whitespace_pattern, ' ', email['RawText'])
    clean_text = re.sub(non_alpha_num_pattern, ' ', clean_text)
    # add the text
    all_emails.append({'text' : clean_text, '_id' : email['_id']})

# create a bag of words
word_bag_with_ids = get_word_bag(all_emails)
word_bag, ids = word_bag_with_ids['bag_of_words'], word_bag_with_ids['ids']

# create the model
n_clusters = 8
km = KMeans(n_clusters=n_clusters, init='k-means++', n_init=1, verbose=1)
# fit the model
km.fit(word_bag)

# store the clusters in a way which is relatable with the original database
clusters = defaultdict(list)
for o,i in enumerate(km.labels_):
    clusters[i].append(ids[o])

# store the cluster names in the mongo documents
for cluster in clusters:
    for _id in clusters[cluster]:
        mon_col.update({'_id' : _id}, {'$set' : {'cluster' : int(cluster)}})

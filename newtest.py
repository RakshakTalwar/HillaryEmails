import pdb
import nltk.stem
from sklearn.feature_extraction.text import TfidfVectorizer

### global instantiations
english_stemmer = nltk.stem.SnowballStemmer('english')
# create a class for the TfidfVectorizer to incorporate stemming
class StemmedTfidfVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedTfidfVectorizer, self).build_analyzer()
        return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))

corpus = ['hello mate', 'hello']
targets = [0, 1]

vectorizer = StemmedTfidfVectorizer()

vectorizer.fit(corpus)

word_bag = vectorizer.transform(['yolo hello'])

pdb.set_trace()

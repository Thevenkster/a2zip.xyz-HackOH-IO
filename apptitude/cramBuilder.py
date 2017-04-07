#CREDIT: TextRank (http://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf)
#
import numpy as np, scipy
import networkx as nx
from nltk.tokenize.punkt import PunktSentenceTokenizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


#general explanation (TEXTRANK):
#1. separate text into sentences based on trained model;
#2. (BAG OF WORDS) : Build sparse matrix of words and the count it appears;
#3  Normalize each word using scikit learn library (the term is called:
#      "term frequency–inverse document frequency",)
#4.
def relevance(input):
    #setup the nltk tokenizer,
    stringtoken = PunktSentenceTokenizer()
    sentences = stringtoken.tokenize(input)
    #we use the count vectorizer to fit and transform our data,
    #creating a sparse bag of word matrix
    bagowmtrx = CountVectorizer().fit_transform(sentences)
    #using term frequency-inverse document frequency, we can normalize our
    #
    normalized = TfidfTransformer().fit_transform(bagowmtrx)

    similarity_graph = normalized * normalized.T

    nx_graph = nx.from_scipy_sparse_matrix(similarity_graph)

    results = nx.pagerank(nx_graph)
    data = sorted(((results[i],s) for i,s in enumerate(sentences)),
                  reverse=True)
    return data



# class cramBerry(object):
#     def __init__(self, topic='', data=None):
#         self.data = data
#         self.topic = topic
#
#     def bagOfWords(self):
#

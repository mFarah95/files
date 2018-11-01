import random
import codecs
import re
import string
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
import io
import copy
import sys
from nltk.stem.porter import PorterStemmer


def get_lsi(tfidf_corpus, dictionary):

    # Build LSI
    lsi_model = gensim.models.LsiModel(
        tfidf_corpus, id2word=dictionary, num_topics=100)

    # Map bow into LSI weights
    lsi_corpus = lsi_model[tfidf_corpus]

    # MatrixSimilarity object
    index = gensim.similarities.MatrixSimilarity(
        lsi_corpus, num_features=len(dictionary))

    return lsi_model, index


def main():

    ################ PART 1 - Data loading and preprocessing #################

    random.seed(123)

    # Open text
    f = io.open("nlp/pg3300.txt", 'r', encoding="utf-8")
    # Remove text punctuation and lower case
    text = f.read().translate(str.maketrans('', '', string.punctuation)).lower()
    # Split text into paragraphs
    split_paragraph = re.split(r"\n\s*\n", str(text))

    # Filter out paragraphs that contain "gutenberg"
    filtered_word = filter(
        lambda prgh: 'gutenberg' not in prgh, split_paragraph)

    # Tokenize paragraphs (split them into words) and remove whitespaces
    tokenized = [prgh.split() for prgh in filtered_word]

    # Stemmeing
    stemmer = PorterStemmer()
    stemmed = [[stemmer.stem(word) for word in parh] for parh in tokenized]

    ################ PART 2 - Dictionary building #############################

    # Load "common english words" text file
    cm_w = io.open("nlp/common-english-words.txt", "r", encoding="utf-8")
    stopwords = cm_w.read().split(",")

    # Init Corpora dictionary
    dictionary = gensim.corpora.Dictionary(stemmed)

    # Filter stopwords that are not in dictinoary
    stopwords = list(filter(
        lambda word: word in dictionary.token2id, stopwords))

    # Get stopword IDs
    stopwords_ids = list(
        map(lambda w: dictionary.token2id[w], stopwords))

    # Filter stopwords
    dictionary.filter_tokens(stopwords_ids)

    # Map paragraphs into Bags-of-Words using the dictionary
    corpus = [dictionary.doc2bow(prgh) for prgh in stemmed]

    ################ PART 3 - Retrieval Models ###############################

    # Build TF-IDF
    tfidf_model = gensim.models.TfidfModel(corpus)

    # Map bow into TF-IDF weights
    tfidf_corpus = tfidf_model[corpus]

    # MatrixSimilarity object
    tfidf_index = gensim.similarities.MatrixSimilarity(
        tfidf_corpus, num_features=len(dictionary))

    # Repeating steps above for LSI
    lsi_model, lsi_index = get_lsi(tfidf_corpus, dictionary)

    # Report and interpret first 3 LSI topics
    lsi_model.show_topics(num_topics=3)

    ################ PART 4 - Querying #######################################

    print("done")


if __name__ == '__main__':
    main()

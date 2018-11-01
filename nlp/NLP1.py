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

    testt = f.read()

    # Split text into paragraphs
    split_paragraph = re.split(r"\n\s*\n", testt)

    # Filter out paragraphs that contain "gutenberg"
    filtered_word = list(filter(
        lambda prgh: not re.search(r"gutenberg", prgh, re.IGNORECASE), split_paragraph))

    # Tokenize paragraphs (split them into words) and remove whitespaces
    tokenized = [prgh.split() for prgh in filtered_word]

    # Remove text punctuation and lower case
    text = [[word.translate(
        str.maketrans('', '', string.punctuation+"\n\r\t")).lower()
        for word in parh] for parh in tokenized]

    # Stemmeing
    stemmer = PorterStemmer()
    stemmed = [[stemmer.stem(word) for word in parh] for parh in text]

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
    print("[First 3 LSI topics] \n",
          lsi_model.show_topics(num_topics=3), "\n\n")

    ################ PART 4 - Querying #######################################

    # Query
    preprocessed_query = "What is the function of money?"

    # Apply transformations part 1 (remove punctuations, tokenize and lowercase)
    transformations = preprocessed_query.translate(
        str.maketrans('', '', string.punctuation)).lower().split()

    # Apply transformations part 2 (stem and convert to BOW)
    query = dictionary.doc2bow([stemmer.stem(word)
                                for word in transformations])

    # Convert BOW to TF-IDF ----------------------------- PRINT THIS
    tfidf_query = tfidf_model[query]

    # Report
    print("[TF-IDF weights]")
    for weights in tfidf_query:
        print(str(dictionary[weights[0]]) + ":", weights[1], end=' ')
    print("\n\n")

    # Sort top 3 most relevant paragraphs
    doc2similarity_tfidf = enumerate(tfidf_index[tfidf_query])
    sorted_sim_tfidf = sorted(doc2similarity_tfidf, key=lambda kv: -kv[1])[:3]

    # non utf-8 of the text
    f = io.open("nlp/pg3300.txt", 'r')

    # Split into paragraphs and remove header and footer
    orginal = re.split(r"\n\s*\n", f.read())

    orginal = list(filter(
        lambda prgh: not re.search(r"gutenberg", prgh, re.IGNORECASE), orginal))

    # Report
    print("TF-IDF: TOP 3 MOST RELVANT PARAGRAPHS:", "\n")

    for prgh in sorted_sim_tfidf:
        print("[paragraph " + str(prgh[0]) + "]", "\n",
              orginal[prgh[0]].split("\n")[:5], "\n\n")

    # Top 3 topics with the most significant (with the largest absolute values) weights
    lsi_query = lsi_model[tfidf_query]

    sorted_abs = sorted(lsi_query, key=lambda kv: -abs(kv[1]))[:3]

    # Report
    print("TOP 3 MOST SIGNIFICANT WEIGHTS:", "\n")
    for topic in sorted_abs:
        print("[topic " + str(topic[0]) + "]", "\n",
              lsi_model.show_topics()[topic[0]][1], "\n\n")

    # Top 3 the most relevant paragraphs (LSI model)
    doc2similarity_lsi = enumerate(lsi_index[lsi_query])
    sorted_sim_lsi = sorted(doc2similarity_lsi, key=lambda kv: -kv[1])[:3]

    # Report
    print("LSI MODEL: TOP 3 MOST RELVANT PARAGRAPHS:", "\n")
    for prgh in sorted_sim_lsi:
        print("[paragraph " + str(prgh[0]) + "]", "\n",
              orginal[prgh[0]].split("\n")[:5], "\n\n")


if __name__ == '__main__':
    main()

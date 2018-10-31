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
bow = [dictionary.doc2bow(prgh) for prgh in stemmed]


################ PART 3 - Retrieval Models ###############################

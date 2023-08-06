from __future__ import print_function, unicode_literals

from functools import reduce

import numpy as np
from gensim.models import Word2Vec
from sklearn.preprocessing import StandardScaler

from kolibri.settings import EMBEDDING_SIZE, WORD2VEC_WORKERS, MIN_WORD_COUNT, WORD2VEC_CONTEXT
from kolibri.utils import chunks
from kolibri.utils import flatten
from kolibri.utils.file import save_to_disk


def train_word2vec_in_memory(docs, vec_dim=EMBEDDING_SIZE):
    """
    Builds word embeddings from documents and return a model
    :param docs: list of Document objects
    :param vec_dim: the dimensionality of the vector that's being built

    :return: trained gensim object with word embeddings
    """
    doc_sentences = map(lambda d: d.read_sentences(), docs)
    all_sentences = reduce(lambda d1, d2: d1 + d2, doc_sentences)

    # Initialize and train the model
    model = Word2Vec(
        all_sentences,
        workers=WORD2VEC_WORKERS,
        size=vec_dim,
        min_count=MIN_WORD_COUNT,
        window=WORD2VEC_CONTEXT,
    )

    # If you don't plan to train the model any further, calling
    # init_sims will make the model much more memory-efficient.
    model.init_sims(replace=True)

    return model


def compute_word2vec_for_phrase(phrase, model):
    """
    Compute (add) word embedding for a multiword phrase using a given model
    :param phrase: unicode, parsed label of a keyphrase
    :param model: gensim word2vec object

    :return: numpy array
    """
    result = np.zeros(model.vector_size, dtype='float32')
    for word in phrase.split():
        if word in model.wv:
            result += model.wv[word]

    return result


def fit_scaler(datastream, word2vec_model, batch_size=1024, persist_to_path=None):
    """ Get all the word2vec vectors in a 2D matrix and fit the scaler on it.
     This scaler can be used afterwards for normalizing feature matrices. """
    if type(word2vec_model) == str:
        word2vec_model = Word2Vec.load(word2vec_model)

    scaler = StandardScaler(copy=False)

    for batch in chunks([d.sentences for d in datastream], batch_size):
        vectors = []
        for doc in flatten(batch):
            for word in doc:
                if word in word2vec_model.wv:
                    vectors.append(word2vec_model.wv[word])

        matrix = np.array(vectors)
        print("Fitted to {} vectors".format(matrix.shape[0]))

        scaler.partial_fit(matrix)

    if persist_to_path:
        save_to_disk(persist_to_path, scaler)

    return scaler


def train_word2vec(training_data, vec_dim=EMBEDDING_SIZE):
    """
    Train the Word2Vec object iteratively, loading stuff to memory one by one.
    :param doc_directory: directory with the documents
    :param vec_dim: the dimensionality of the vector that's being built

    :return: Word2Vec object
    """

    class SentenceIterator(object):
        def __init__(self, data):
            self.training_data = data

        def __iter__(self):

            for document in self.training_data:
                for sentence in document.sentences:
                    yield sentence

    # Initialize and train the model
    model = Word2Vec(
        SentenceIterator(training_data),
        workers=WORD2VEC_WORKERS,
        size=vec_dim,
        min_count=MIN_WORD_COUNT,
        window=WORD2VEC_CONTEXT,
    )

    # If you don't plan to train the model any further, calling
    # init_sims will make the model much more memory-efficient.
    model.init_sims(replace=True)

    return model

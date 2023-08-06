import logging
import os
from typing import Any, Dict, Text

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

from kolibri.features.features import Features
from kolibri.stopwords import get_stop_words

logger = logging.getLogger(__name__)


class TFIDFFeaturizer(Features):
    """Bag of words featurizer

    Creates bag-of-words representation of intent features
    using sklearn's `CountVectorizer`.
    All tokens which consist only of digits (e.g. 123 and 99
    but not ab12d) will be represented by a single feature."""

    name = "tf_idf_featurizer"

    provides = ["text_features"]

    requires = ["tokens"]

    defaults = {
        # the parameters are taken from
        # sklearn's CountVectorizer

        # regular expression for tokens
        "token_pattern": r'(?u)\b\w\w+\b',

        # remove accents during the preprocessing step
        "strip_accents": None,  # {'ascii', 'unicode', None}

        "lower-case": True,
        # list of stop words
        "stop_words": None,  # string {'en'}, list, or None (default)

        # min document frequency of a word to add to vocabulary
        # float - the parameter represents a proportion of documents
        # integer - absolute counts
        "min_df": 7,  # float in range [0.0, 1.0] or int

        # max document frequency of a word to add to vocabulary
        # float - the parameter represents a proportion of documents
        # integer - absolute counts
        "max_df": 0.7,  # float in range [0.0, 1.0] or int

        # set range of ngrams to be extracted
        "min_ngram": 1,  # int
        "max_ngram": 1,  # int

        # limit vocabulary size
        "max_features": 5000,  # int or None

        # if convert all characters to lowercase
        "case_sensitive": True,  # bool
        "use_bigram_model": False

    }

    @classmethod
    def required_packages(cls):
        return ["sklearn"]

    def _load_count_vect_params(self):
        # regular expression for tokens
        self.token_pattern = self.component_config['token_pattern']

        # remove accents during the preprocessing step
        self.strip_accents = self.component_config['strip_accents']

        # list of stop words
        self.stop_words = self.component_config['stop_words']

        # min number of word occurancies in the document to add to vocabulary
        self.min_df = self.component_config['min_df']

        # max number (fraction if float) of word occurancies
        # in the document to add to vocabulary
        self.max_df = self.component_config['max_df']

        # set ngram range
        self.min_ngram = self.component_config['min_ngram']
        self.max_ngram = self.component_config['max_ngram']

        # limit vocabulary size
        self.max_features = self.component_config['max_features']

        # if convert all characters to lowercase
        self.lowercase = self.component_config['lower-case']

    def __init__(self, component_config=None):
        """Construct a new count vectorizer using the sklearn framework."""

        super(TFIDFFeaturizer, self).__init__(component_config)

        # parameters for sklearn's CountVectorizer
        self._load_count_vect_params()
        self.use_bigram_model = self.component_config["use_bigram_model"]
        # declare class instance for CountVectorizer
        self.stop_words = get_stop_words('en')

        self.vectorizer = TfidfVectorizer(min_df=self.min_df, sublinear_tf=True, max_df=self.max_df,
                                          tokenizer=self._identity_tokenizer, lowercase=False,
                                          stop_words=self.stop_words)

    def _identity_tokenizer(self, text):
        return text

    def fit(self, X, y):
        self.vectorizer.fit(X, y)

        return self

    def transform(self, X):

        if self.vectorizer is None:
            logger.error("There is no trained CountVectorizer: "
                         "component is either not trained or "
                         "didn't receive enough training texts")
        else:
            return self.vectorizer.transform(raw_documents=X)

    def train(self, training_data, **kwargs):
        """Take parameters from config and
                construct a new tfidf vectorizer using the sklearn framework."""

        self.vectorizer.fit([doc.tokens for doc in training_data])
        [self.process(doc) for doc in training_data]

    def process(self, document, **kwargs):

        document.vector = self.vectorizer.transform([document.tokens])[0]

    def persist(self, model_dir):
        # type: (Text) -> Dict[Text, Any]
        """Persist this model into the passed directory.
        Returns the metadata necessary to load the model again."""

        featurizer_file = os.path.join(model_dir, self.name + ".pkl")
        joblib.dump(self, featurizer_file)
        return {"featurizer_file": self.name + ".pkl"}

    @classmethod
    def load(cls,
             model_dir=None, model_metadata=None, cached_component=None, **kwargs):

        meta = model_metadata.for_component(cls.name)

        if model_dir and meta.get("featurizer_file"):
            file_name = meta.get("featurizer_file")
            featurizer_file = os.path.join(model_dir, file_name)
            return joblib.load(featurizer_file)
        else:
            logger.warning("Failed to load featurizer. Maybe path {} "
                           "doesn't exist".format(os.path.abspath(model_dir)))
            return TFIDFFeaturizer(meta)

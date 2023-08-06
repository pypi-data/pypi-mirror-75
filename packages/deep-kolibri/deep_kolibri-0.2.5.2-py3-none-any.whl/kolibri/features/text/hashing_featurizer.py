from sklearn.feature_extraction.text import HashingVectorizer

from kolibri.features.features import Features
from kolibri.stopwords import get_stop_words


class HashingFeaturizer(Features):
    """Bag of words featurizer

    Creates bag-of-words representation of intent features
    using sklearn's `HashingVectorizer`.
    All tokens which consist only of digits (e.g. 123 and 99
    but not ab12d) will be represented by a single feature."""

    name = "hashing_featurizer"

    provides = ["text_features"]

    requires = ["tokens"]

    defaults = {
        # the parameters are taken from
        # sklearn's CountVectorizer

        # regular expression for tokens
        "token_pattern": r'(?u)\b\w\w+\b',

        # remove accents during the preprocessing step
        "strip_accents": None,  # {'ascii', 'unicode', None}

        # list of stop words
        "stop_words": None,  # string {'en'}, list, or None (default)

        # if convert all characters to lowercase
        "lower-case": False,  # bool
        "use_bigram_model": False
    }

    @classmethod
    def required_packages(cls):
        return ["sklearn"]

    def __init__(self, component_config={}):
        """Construct a new count vectorizer using the sklearn framework."""

        super(HashingFeaturizer, self).__init__(component_config)

        self.use_bigram_model = self.component_config["use_bigram_model"]
        # declare class instance for CountVectorizer
        self.stop_words = get_stop_words('en')

        self.vectorizer = HashingVectorizer(decode_error='ignore', n_features=2 ** 18,
                                            alternate_sign=False, tokenizer=self._identity_tokenizer, lowercase=False,
                                            stop_words=self.stop_words)

    def _identity_tokenizer(self, text):
        return text

    def fit(self, X, y):
        return self

    def transform(self, X):
        return self.vectorizer.transform(X)

    def train(self, training_data, **kwargs):
        [self.process(document) for document in training_data]

    def process(self, document, **kwargs):
        document.vector = self.vectorizer.transform([document.tokens])

    def get_info(self):
        return 'hasing vectorizer'

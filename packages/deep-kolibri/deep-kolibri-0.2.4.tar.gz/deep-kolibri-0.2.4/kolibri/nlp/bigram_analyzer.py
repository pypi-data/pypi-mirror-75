import logging
import os
from typing import List
from typing import Text

import joblib
from gensim.models import Phrases

from kolibri.kolibri_component import Component
from kolibri.utils.file import save_to_disk, load_from_disk

logger = logging.getLogger(__name__)

BIGRAM_FILENAME = "kolibri-bigram.model"


class BigramAnalyzer(Component):

    _estimator_type = 'estimator'

    name = 'bigram_analyzer'

    provides = ["ngram"]

    requires = ["text_features"]

    defaults = {
        # We try to find a good number of cross folds to use during
        # class training, this specifies the max number of folds
        "min-count": 5,

        "threshold": 10,

        "retrain-bigram": False
    }

    def __init__(self, component_config=None):
        """Construct a new class classifier using the sklearn framework."""
        super().__init__(component_config=component_config)
        self.bigram_model = None

    @classmethod
    def required_packages(cls):
        # type: () -> List[Text]
        return ["gensim"]

    def train(self, training_data, **kwargs):
        retrain = self.component_config['retrain-bigram']
        if retrain:
            self.train_bigram(training_data)
            self.save_bigram_model()
        elif self.bigram_model:
            [self.process(d) for d in training_data]
        else:
            self.bigram_model = self.load_bigram_model()
            [self.process(d) for d in training_data]

    def fit(self, X, y):
        retrain = self.component_config['retrain-bigram']
        if retrain:
            self.train_bigram(X)
            self.save_bigram_model()
        else:
            self.bigram_model = self.load_bigram_model()
        return self

    def transform(self, data, **kwargs):
        return [self.bigram_model[d] for d in data]

    def process(self, document, **kwargs):
        return self.bigram_model[document.sentences]

    def train_bigram(self, trainingdata):
        """
        Train the word2vec model on a directory with text files.
        :param train_dir: directory with '.txt' files
        :param vec_dim: dimensionality of the word vectors

        :return: trained gensim model
        """

        class SentenceIterator(object):
            def __init__(self, data):
                self.training_data = data

            def __iter__(self):
                for document in self.training_data:
                    for sentence in document.sentences:
                        yield sentence

        self.bigram_model = Phrases(SentenceIterator(trainingdata), min_count=self.component_config['min-count'],
                                    threshold=self.component_config['threshold'])

        return self.bigram_model

    def save_bigram_model(self, overwrite=True):
        """ Save the word2vec model to a file """
        if not self.bigram_model:
            raise ValueError("Can't save the word2vec model, " + \
                             "it has not been trained yet")
        save_to_disk(os.path.join(self.component_config["output-folder"], BIGRAM_FILENAME), self.bigram_model,
                     overwrite=overwrite)

    def load_bigram_model(self):
        """ Load the word2vec model from a file """
        self.bigram_model = load_from_disk(os.path.join(self.component_config["output-folder"], BIGRAM_FILENAME))
        return self.bigram_model

    @classmethod
    def load(cls, model_dir=None, model_metadata=None, cached_component=None, **kwargs):

        meta = model_metadata.for_component(cls.name)
        file_name = meta.get("bigram_file", BIGRAM_FILENAME)
        classifier_file = os.path.join(model_dir, file_name)

        if os.path.exists(classifier_file):
            model = joblib.load(classifier_file)

            return model
        else:
            return cls(meta)

    def persist(self, model_dir):
        """Persist this model into the passed directory."""

        bigram_file = os.path.join(model_dir, BIGRAM_FILENAME)
        joblib.dump(self, bigram_file)

        return {
            "bigram_file": BIGRAM_FILENAME
        }

    def get_info(self):
        return "brigram analyzer"

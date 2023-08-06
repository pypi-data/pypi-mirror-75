import logging
import os

import joblib
import numpy as np
from scipy.sparse import vstack
from sklearn.utils import class_weight

from kolibri.indexers.label_indexer import LabelIndexer
from kolibri.kolibri_component import Component

logger = logging.getLogger(__name__)

KOLIBRI_MODEL_FILE_NAME = "classifier_kolibri.pkl"
DNN_MODEL_FILE_NAME = "classifier_dnn"


class DnnEstimator(Component):
    """classifier using the sklearn framework"""

    _estimator_type = 'estimator'

    name = ''

    provides = []

    requires = []

    defaults = {

        # the models used in the classifier if several models are given they will be combined
        "embeddings": None,
        "multi-label": False,
        "sequence_length": 'auto',
        "epochs": 1,
        "loss": 'categorical_crossentropy',
        "class-weight": False,
    }

    def __init__(self, component_config=None):

        """Construct a new class classifier using the sklearn framework."""
        super().__init__(component_config=component_config)

        self.indexer = LabelIndexer(multi_label=self.component_config["multi-label"])

    @classmethod
    def required_packages(cls):
        return ["tensorflow"]

    def fit(self, X, y, X_val=None, y_val=None):
        fit_kwargs = {}
        if self.component_config['class-weight']:
            class_weights = class_weight.compute_class_weight('balanced',
                                                              np.unique(y),
                                                              y)
            fit_kwargs = {"class_weight": class_weights}

        self.clf.fit(X, y, x_validate=X_val, y_validate=y_val, epochs=self.component_config["epochs"],
                     fit_kwargs=fit_kwargs)

    def transform(self, document):

        return self.clf.transform(document, )

    def predict(self, X):
        """Given a bow vector of an input text, predict most probable label.

        Return only the most likely label.

        :param X: bow of input text
        :return: tuple of first, the most probable label and second,
                 its probability."""

        return self.clf.predict(X)

    def train(self, training_data, **kwargs):

        y = [document.label for document in training_data]
        X = vstack([document.vector for document in training_data])
        self.fit(X, y)

    def process(self, document, **kwargs):
        raise NotImplementedError

    def __getstate__(self):
        """Return state values to be pickled."""
        return (self.component_config, self.classifier_type, self.indexer)

    def __setstate__(self, state):
        """Restore state from the unpickled state values."""
        self.component_config, self.classifier_type, self.indexer = state

    @classmethod
    def load(cls, model_dir=None, model_metadata=None, cached_component=None, **kwargs):

        meta = model_metadata.for_component(cls.name)
        classifier_file_name = meta.get("classifier_file", KOLIBRI_MODEL_FILE_NAME)
        dnn_file_name = meta.get("dnn_file", DNN_MODEL_FILE_NAME)
        classifier_file = os.path.join(model_dir, classifier_file_name)
        if os.path.exists(classifier_file):
            # Load saved model
            model = joblib.load(classifier_file)

            clf = model.classifier_type.load_model(os.path.join(model_dir, dnn_file_name))

            model.clf = clf
            return model
        else:
            return cls(meta)

    def persist(self, model_dir):
        """Persist this model into the passed directory.

        Returns the metadata necessary to load the model again."""
        classifier_file = os.path.join(model_dir, KOLIBRI_MODEL_FILE_NAME)
        joblib.dump(self, classifier_file)
        dnn_file = os.path.join(model_dir, DNN_MODEL_FILE_NAME)
        if self.clf:
            self.clf.save(dnn_file)

        return {"classifier_file": KOLIBRI_MODEL_FILE_NAME, "dnn_file": DNN_MODEL_FILE_NAME}

    #
    # @classmethod
    # def load(cls, model_dir=None, model_metadata=None,  cached_component=None,  **kwargs):
    #
    #
    #     meta = model_metadata.for_component(cls.name)
    #     classifier_file_name = meta.get("classifier_file", KOLIBRI_MODEL_FILE_NAME)
    #     dnn_file_name = meta.get("dnn_file", DNN_MODEL_FILE_NAME)
    #     classifier_file = os.path.join(model_dir, classifier_file_name)
    #
    #     if os.path.exists(classifier_file):
    #         # Load saved model
    #         model = joblib.load(classifier_file)
    #         clf = kolibri.dnn.utils.load_model(dnn_file_name)
    #         model.clf=clf
    #         return model
    #     else:
    #         return cls(meta)
    #
    # def persist(self, model_dir):
    #     """Persist this model into the passed directory."""
    #
    #
    #
    #     classifier_file = os.path.join(model_dir, KOLIBRI_MODEL_FILE_NAME)
    #     joblib.dump(self, classifier_file)
    #     dnn_file = os.path.join(model_dir, DNN_MODEL_FILE_NAME)
    #     self.clf.save(dnn_file)
    #
    #     return {"classifier_file": DNN_MODEL_FILE_NAME, "dnn_file":DNN_MODEL_FILE_NAME}

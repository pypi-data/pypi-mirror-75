import logging

from kolibri import settings
from kolibri.config import TaskType
from kolibri.dnn.embeddings import DefaultEmbedding, WordEmbedding
from kolibri.dnn.tasks.dnn_estimator import DnnEstimator
from kolibri.dnn.tasks.text.classification.models import get_model

logger = logging.getLogger(__name__)

KOLIBRI_MODEL_FILE_NAME = "classifier_kolibri.pkl"
DNN_MODEL_FILE_NAME = "classifier_dnn"


class DnnTextClassEstimator(DnnEstimator):
    """classifier using the sklearn framework"""

    name = 'dnn_classifier'

    provides = ["classification", "target_ranking"]

    requires = ["text_features"]

    defaults = {

        # the models used in the classifier if several models are given they will be combined
        "models": "bilstm",
        "embeddings": "default",
        "multi-label": False,
        "sequence_length": 'auto',
        "epochs": 1,
        "loss": 'categorical_crossentropy',
        "class-weight": False,

    }

    def __init__(self, component_config=None):

        """Construct a new class classifier using the sklearn framework."""
        super().__init__(component_config)

        if self.component_config['embeddings'] == 'default':
            self.embeddings = DefaultEmbedding(task=TaskType.CLASSIFICATION,
                                               sequence_length=self.component_config["sequence_length"],
                                               indexer=self.indexer)
        elif self.component_config['embeddings'] == 'word':
            self.embeddings = WordEmbedding(w2v_path=self.component_config["embedding_path"],
                                            task=TaskType.CLASSIFICATION,
                                            sequence_length=self.component_config["sequence_length"],
                                            indexer=self.indexer)
        elif self.component_config['embeddings'] == None:
            self.embeddings = None

        self.clf = get_model(self.component_config['models'], embedding=self.embeddings,
                             hyper_parameters=self.component_config)
        self.classifier_type = type(self.clf)

    @classmethod
    def required_packages(cls):
        return ["tensorflow"]

    def process(self, document, **kwargs):
        """Return the most likely class and its probability for a document."""
        raw_results = None
        if not self.clf:
            # component is either not trained or didn't
            # receive enough training texts
            target = None
            target_ranking = []
        else:
            X = document.tokens
            raw_results = self.clf.predict([X], top_k=settings.modeling['TARGET_RANKING_LENGTH'])

            if len(raw_results) > 0:

                target = {"name": raw_results[0]['label'], "confidence": raw_results[0]['confidence']}

                target_ranking = raw_results[0]['confidence']
            else:
                target = {"name": None, "confidence": 0.0}
                target_ranking = []

        document.label = target
        document.raw_prediction_results = raw_results
        document.set_output_property("raw_prediction_results")
        document.set_output_property("label")
        document.target_ranking = target_ranking
        document.set_output_property("target_ranking")

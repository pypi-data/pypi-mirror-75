from kolibri.tasks.classification.models import get_online_model
from kolibri.tasks.classification.sklearn_estimator import SklearnEstimator


class StreamedClassifier(SklearnEstimator):
    name = 'streamed_classifier'

    def __init__(self, component_config, classifier='MultinomialNB'):
        super().__init__(component_config=component_config, classifier=classifier)

        self.clf = get_online_model(classifier)

    def partial_fit(self, X, y, classes):
        self.indexer.build_label_dict(y)
        y = self.indexer.numerize_label_sequences(y)

        return self.clf.partial_fit(X, y, classes)

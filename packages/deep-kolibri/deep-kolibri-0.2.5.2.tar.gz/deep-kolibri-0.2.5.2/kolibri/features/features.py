import numpy as np

from kolibri.kolibri_component import Component


class Features(Component):

    def __init__(self, config):
        super().__init__(config)
        self.vectorizer = None

    @staticmethod
    def _combine_with_existing_features(document,
                                        additional_features):
        if document.get("text_features") is not None:
            return np.hstack((document.get("text_features"),
                              additional_features))
        else:
            return additional_features

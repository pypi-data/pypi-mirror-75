import json
import os
import pathlib
from abc import abstractmethod
from typing import Dict, Any

import tensorflow as tf

import kolibri
from kolibri.indexers import LabelIndexer
from kolibri.logger import logger


class TaskBaseModel(object):

    def __init__(self, sequence_length=None, hyper_parameters=None, multi_label=False, label_indexer=None):

        self.hyper_parameters = self.get_default_hyper_parameters()

        if hyper_parameters:
            self.update_hyper_parameters(hyper_parameters)

        self.tf_model: tf.keras.Model = None

        self.sequence_length: int
        self.sequence_length = sequence_length
        self.multi_label = multi_label
        if label_indexer is None:
            self.label_indexer = LabelIndexer(multi_label=multi_label)

    def to_dict(self) -> Dict[str, Any]:
        model_json_str = self.tf_model.to_json()

        return {
            'tf_version': tf.__version__,  # type: ignore
            'kolibri_version': kolibri.__version__,
            'label_indexer': self.label_indexer.to_dict(),
            '__class_name__': self.__class__.__name__,
            '__module__': self.__class__.__module__,
            'config': {
                'hyper_parameters': self.hyper_parameters,  # type: ignore
            },
            'tf_model': json.loads(model_json_str)
        }

    def update_hyper_parameters(self, parameters):
        if self.hyper_parameters is None:
            return

        for k, v in parameters.items():
            if k in self.hyper_parameters:
                self.hyper_parameters[k] = v

    @classmethod
    def get_default_hyper_parameters(cls) -> Dict[str, Dict[str, Any]]:
        raise NotImplementedError

    def save(self, model_path: str) -> str:
        """
        Save model
        Args:
            model_path:
        """
        pathlib.Path(model_path).mkdir(exist_ok=True, parents=True)
        model_path = os.path.abspath(model_path)
        with open(os.path.join(model_path, 'model_config.json'), 'w') as f:
            f.write(json.dumps(self.to_dict(), indent=2, default=str, ensure_ascii=False))
            f.close()

        self.tf_model.save_weights(os.path.join(model_path, 'model_weights.h5'))  # type: ignore
        logger.info('model saved to {}'.format(os.path.abspath(model_path)))
        return model_path

    @classmethod
    def load_model(cls, model_path):
        raise NotImplementedError

    @abstractmethod
    def build_model(self,
                    x_data: Any,
                    y_data: Any) -> None:
        raise NotImplementedError


if __name__ == "__main__":
    path = ''
    m = TaskBaseModel.load_model(path)
    m.tf_model.summary()

import json
import os
import tempfile
import time
from abc import abstractmethod
from pathlib import Path
from typing import Dict, Any

import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

from kolibri.data.corpus.generators import DataGenerator
from kolibri.dnn.embeddings import DefaultEmbedding
from kolibri.dnn.tasks.base_model import TaskBaseModel
from kolibri.dnn.utils import load_data_object
from kolibri.indexers.text_indexer import TextIndexer
from kolibri.logger import logger


class TextBaseModel(TaskBaseModel):

    def __init__(self, embedding=None, sequence_length=None, hyper_parameters=None, multi_label=False,
                 content_indexer=None, label_indexer=None):

        super().__init__(sequence_length, hyper_parameters, multi_label, label_indexer)

        if embedding is None:
            embedding = DefaultEmbedding()  # type: ignore
        if content_indexer is None:
            content_indexer = TextIndexer()

        self.content_indexer = content_indexer
        self.embedding = embedding

    def to_dict(self):
        model_json_str = self.tf_model.to_json()
        base_dict = super(TextBaseModel, self).to_dict()
        base_dict.update({
            'embedding': self.embedding.to_dict(),  # type: ignore
            'content_indexer': self.content_indexer.to_dict(),
            'label_indexer': self.label_indexer.to_dict(),
            'tf_model': json.loads(model_json_str)
        })
        return base_dict

    def update_hyper_parameters(self, parameters):
        if self.hyper_parameters is None:
            return

        for k, v in parameters.items():
            if k in self.hyper_parameters:
                self.hyper_parameters[k] = v

    @classmethod
    def get_default_hyper_parameters(cls) -> Dict[str, Dict[str, Any]]:
        raise NotImplementedError

    def fit(self, x_train, y_train, x_validate=None, y_validate=None,
            *,
            batch_size: int = 64,
            epochs: int = 5,
            early_stopping_patience=3,
            callbacks=None,
            fit_kwargs: Dict = None):
        """
        Trains the model for a given number of epochs with given texts set list.
        """
        self.checkpoint_model_path = ""
        if x_validate:
            if callbacks is None:
                callbacks = []
            self.checkpoint_model_path = os.path.join(tempfile.gettempdir(), str(time.time()))
            Path(self.checkpoint_model_path).mkdir(parents=True, exist_ok=True)
            self.checkpoint_model_path = os.path.join(self.checkpoint_model_path, 'best_weights.h5')
            callbacks.append([EarlyStopping(monitor='val_accuracy', patience=early_stopping_patience),
                              ModelCheckpoint(filepath=self.checkpoint_model_path, monitor='val_accuracy',
                                              save_best_only=True, verbose=1, mode='max')])

        train_gen = DataGenerator(x_train, y_train)
        if x_validate is not None:
            valid_gen = DataGenerator(x_validate, y_validate)
        else:
            valid_gen = None
        return self.fit_generator(train_sample_gen=train_gen,
                                  valid_sample_gen=valid_gen,
                                  batch_size=batch_size,
                                  epochs=epochs,
                                  callbacks=callbacks,
                                  fit_kwargs=fit_kwargs)

    def build_model_generator(self, generators):
        raise NotImplementedError

    def fit_generator(self, train_sample_gen, valid_sample_gen=None,
                      *,
                      batch_size: int = 64,
                      epochs: int = 5,
                      callbacks=None,
                      fit_kwargs):

        self.build_model_generator([g for g in [train_sample_gen, valid_sample_gen] if g])

        model_summary = []
        self.tf_model.summary(print_fn=lambda x: model_summary.append(x))
        logger.debug('\n'.join(model_summary))

        train_set = train_sample_gen
        train_set.set_batch_size(batch_size)
        train_set.label_indexer = self.label_indexer
        train_set.content_indexer = self.content_indexer

        if fit_kwargs is None:
            fit_kwargs = {}

        if valid_sample_gen:
            valid_gen = train_sample_gen
            valid_gen.set_batch_size(batch_size)
            valid_gen.label_indexer = self.label_indexer
            valid_gen.content_indexer = self.content_indexer

            fit_kwargs['validation_data'] = valid_gen
            fit_kwargs['validation_steps'] = len(valid_gen)

        history = self.tf_model.fit(train_set,
                                    steps_per_epoch=len(train_set),
                                    epochs=epochs,
                                    callbacks=callbacks,
                                    **fit_kwargs)
        if os.path.exists(self.checkpoint_model_path):
            self.tf_model.load_weights(self.checkpoint_model_path)

        return self.tf_model

    @classmethod
    def load_model(cls, model_path):
        from kolibri.dnn.layers.crf import ConditionalRandomField
        model_config_path = os.path.join(model_path, 'model_config.json')
        with open(model_config_path, 'r') as f:
            model_config = json.loads(f.read())
        model = load_data_object(model_config)

        model.embedding = load_data_object(model_config['embedding'])
        model.content_indexer = load_data_object(model_config['content_indexer'])
        model.label_indexer = load_data_object(model_config['label_indexer'])

        tf_model_str = json.dumps(model_config['tf_model'])
        model.tf_model = tf.keras.models.model_from_json(tf_model_str,
                                                         {'ConditionalRandomField': ConditionalRandomField})

        if isinstance(model.tf_model.layers[-1], ConditionalRandomField):
            model.layer_crf = model.tf_model.layers[-1]

        model.tf_model.load_weights(os.path.join(model_path, 'model_weights.h5'))
        model.embedding.embed_model.load_weights(os.path.join(model_path, 'embed_model_weights.h5'))
        return model

    @abstractmethod
    def build_model(self,
                    x_data: Any,
                    y_data: Any) -> None:
        raise NotImplementedError

    def save(self, model_path: str) -> str:
        """
        Save model
        Args:
            model_path:
        """

        super(TextBaseModel, self).save(model_path)
        self.embedding.embed_model.save_weights(os.path.join(model_path, 'embed_model_weights.h5'))
        logger.info('embedding file saved to {}'.format(os.path.abspath(model_path)))
        return model_path


if __name__ == "__main__":
    path = '/var/folders/x3/_dg9_drj42l_cc70tsqkpqrw0000gn/T/1590915853.4571211'
    m = TextBaseModel.load_model(path)
    m.tf_model.summary()

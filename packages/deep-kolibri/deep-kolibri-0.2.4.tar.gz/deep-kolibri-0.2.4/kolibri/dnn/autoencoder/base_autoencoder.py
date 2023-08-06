import json
import logging
import os
import pathlib
from typing import Dict, Any, List, Optional, Union, Tuple

import numpy as np
import tensorflow as tf
from tensorflow import keras

from kolibri.dnn import __version__
from kolibri.dnn.utils import custom_object_scope

L = keras.layers


class BaseAutoencoder(object):
    """Base Sequence Labeling Model"""

    @classmethod
    def get_default_hyper_parameters(cls) -> Dict[str, Dict[str, Any]]:
        raise NotImplementedError

    def info(self):
        model_json_str = self.tf_model.to_json()

        return {
            'config': {
                'hyper_parameters': self.hyper_parameters,
            },
            'tf_model': json.loads(model_json_str),
            'class_name': self.__class__.__name__,
            'module': self.__class__.__module__,
            'tf_version': tf.__version__,
            'kolibri.version': __version__
        }

    def __init__(self, hyper_parameters: Optional[Dict[str, Dict[str, Any]]] = None):
        """

        """

        self.hyper_parameters = self.get_default_hyper_parameters()
        self.model_info = {}

        self.autoencoder=None
        if hyper_parameters:
            self.hyper_parameters.update(hyper_parameters)

    def build_model(self, x_train):
        """
        Build model with corpus

        Args:
            x_train: Array of train feature texts (if the model has a single input),
                or tuple of train feature texts array (if the model has multiple inputs)
            y_train: Array of train label texts
            x_validate: Array of validation feature texts (if the model has a single input),
                or tuple of validation feature texts array (if the model has multiple inputs)
            y_validate: Array of validation label texts

        Returns:

        """
        self.input_dim=x_train[0].size


        if self.autoencoder is None:
            self.build_model_arc()
            self.compile_model(**self.hyper_parameters)


    def build_multi_gpu_model(self,
                              gpus: int,
                              x_train: Union[Tuple[List[List[str]], ...], List[List[str]]],
                              y_train: Union[List[List[str]], List[str]],
                              cpu_merge: bool = True,
                              cpu_relocation: bool = False,
                              x_validate: Union[Tuple[List[List[str]], ...], List[List[str]]] = None,
                              y_validate: Union[List[List[str]], List[str]] = None):
        """
        Build multi-GPU model with corpus

        Args:
            gpus: Integer >= 2, number of on GPUs on which to create model replicas.
            cpu_merge: A boolean value to identify whether to force merging model weights
                under the scope of the CPU or not.
            cpu_relocation: A boolean value to identify whether to create the model's weights
                under the scope of the CPU. If the model is not defined under any preceding device
                scope, you can still rescue it by activating this option.
            x_train: Array of train feature texts (if the model has a single input),
                or tuple of train feature texts array (if the model has multiple inputs)
            y_train: Array of train label texts
            x_validate: Array of validation feature texts (if the model has a single input),
                or tuple of validation feature texts array (if the model has multiple inputs)
            y_validate: Array of validation label texts

        Returns:

        """
        if x_validate is not None and not isinstance(x_validate, tuple):
            self.embedding.analyze_corpus(x_train + x_validate, y_train + y_validate)
        else:
            self.embedding.analyze_corpus(x_train, y_train)

        if self.tf_model is None:
            with custom_object_scope():
                self.build_model_arc()
                self.tf_model = tf.keras.utils.multi_gpu_model(self.tf_model,
                                                               gpus,
                                                               cpu_merge=cpu_merge,
                                                               cpu_relocation=cpu_relocation)
                self.compile_model()

    def get_data_generator(self,
                           x_data,
                           y_data,
                           batch_size: int = 64,
                           shuffle: bool = True):
        """
        texts generator for fit_generator

        Args:
            x_data: Array of feature texts (if the model has a single input),
                or tuple of feature texts array (if the model has multiple inputs)
            y_data: Array of label texts
            batch_size: Number of samples per gradient update, default to 64.
            shuffle:

        Returns:
            texts generator
        """
        index_list = np.arange(len(x_data))
        page_count = len(x_data) // batch_size + 1

        while True:
            if shuffle:
                np.random.shuffle(index_list)
            for page in range(page_count):
                start_index = page * batch_size
                end_index = start_index + batch_size
                target_index = index_list[start_index: end_index]

                if len(target_index) == 0:
                    target_index = index_list[0: batch_size]

                yield (x_data, x_data)

    def fit(self,
            x_train: Union[Tuple[List[List[str]], ...], List[List[str]]],
            x_validate: Union[Tuple[List[List[str]], ...], List[List[str]]] = None,
            batch_size: int = 64,
            epochs: int = 5,
            validation_split=0.2,
            callbacks: List[keras.callbacks.Callback] = None,
            fit_kwargs: Dict = None,
            shuffle: bool = True):
        """
        Trains the model for a given number of epochs with fit_generator (iterations on a dataset).

        Args:
            x_train: Array of train feature texts (if the model has a single input),
                or tuple of train feature texts array (if the model has multiple inputs)
            y_train: Array of train label texts
            x_validate: Array of validation feature texts (if the model has a single input),
                or tuple of validation feature texts array (if the model has multiple inputs)
            y_validate: Array of validation label texts
            batch_size: Number of samples per gradient update, default to 64.
            epochs: Integer. Number of epochs to train the model. default 5.
            callbacks:
            fit_kwargs: fit_kwargs: additional arguments passed to ``fit_generator()`` function from
                ``tensorflow.keras.Model``
                - https://www.tensorflow.org/api_docs/python/tf/keras/models/Model#fit_generator
            shuffle:

        Returns:

        """
        self.build_model(x_train)

        with custom_object_scope():

            return self.autoencoder.fit(x_train, x_train, epochs=epochs,
                                        batch_size=batch_size,
                                        shuffle=shuffle, validation_split=validation_split
                                        )

    def compile_model(self, **kwargs):
        """Configures the model for training.

        Using ``compile()`` function of ``tf.keras.Model`` -
        https://www.tensorflow.org/api_docs/python/tf/keras/models/Model#compile

        Args:
            **kwargs: arguments passed to ``compile()`` function of ``tf.keras.Model``

        Defaults:
            - loss: ``categorical_crossentropy``
            - optimizer: ``adam``
            - metrics: ``['accuracy']``
        """
        configs={}
        configs['loss']=kwargs.get('loss', 'mean_squared_error')
        configs['optimizer']=kwargs.get('optimizer', 'adam')
#        configs['metrics']=kwargs.get('metrics', ['loss'])


        self.autoencoder.compile(**configs)

    def encode(self,
                x_data,
                batch_size=32,
                debug_info=False,
                predict_kwargs: Dict = None):
        """
        Generates output predictions for the encoder.
        """
        if predict_kwargs is None:
            predict_kwargs = {}
        with custom_object_scope():
#            tensor = self.process_x_dataset(x_data)
            pred = self.encoder.predict(x_data, batch_size=batch_size, **predict_kwargs)



            if debug_info:
                print('input: {}'.format(x_data))
                print('output: {}'.format(pred))

        return pred

    def decode(self,
               x_data,
               batch_size=32,
               debug_info=False,
               predict_kwargs: Dict = None):
        """
        Generates output predictions for the encoder.
        """
        if predict_kwargs is None:
            predict_kwargs = {}
        with custom_object_scope():
            tensor = self.process_x_dataset(x_data)
            pred = self.decoder.predict(tensor, batch_size=batch_size, **predict_kwargs)

            if debug_info:
                print('input: {}'.format(tensor))
                print('output: {}'.format(pred))

        return pred

    def predict(self,
               x_data,
               batch_size=32,
               debug_info=False,
               predict_kwargs: Dict = None):
        """
        Generates output predictions for the encoder.
        """
        if predict_kwargs is None:
            predict_kwargs = {}
        with custom_object_scope():

            pred = self.autoencoder.predict(x_data, batch_size=batch_size, **predict_kwargs)

            if debug_info:
                print('input: {}'.format(x_data))
                print('output: {}'.format(pred))

        return pred

    def evaluate(self,
                 x_data,
                 batch_size=None,
                 digits=4,
                 output_dict=False,
                 debug_info=False) -> Optional[Tuple[float, float, Dict]]:
        x_pred = self.autoencoder.predict(x_data, batch_size=batch_size)

        loss=keras.losses.mean_squared_error(x_data, x_pred)
        print(tf.math.reduce_mean(
            loss, axis=None, keepdims=False, name=None
        ))



    def summary(self):
        self.autoencoder.summary()

    def build_model_arc(self):
        raise NotImplementedError

    def save(self, model_path: str):
        """
        Save model
        Args:
            model_path:

        Returns:

        """
        pathlib.Path(model_path).mkdir(exist_ok=True, parents=True)

        with open(os.path.join(model_path, 'model_info.json'), 'w') as f:
            f.write(json.dumps(self.info(), indent=2, ensure_ascii=True))
            f.close()

        self.tf_model.save_weights(os.path.join(model_path, 'model_weights.h5'))
        logging.info('model saved to {}'.format(os.path.abspath(model_path)))

    def save_info(self, model_path: str):
        pathlib.Path(model_path).mkdir(exist_ok=True, parents=True)

        with open(os.path.join(model_path, 'model_info.json'), 'w') as f:
            f.write(json.dumps(self.info(), indent=2, ensure_ascii=True))
            f.close()




# from tensorflow.keras.callbacks import EarlyStopping, TensorBoard
#
#
# class BaseAutoencoder(object):
#
#     def __index__(self, log_dir='/tmp/autoencoder', stop_early=True):
#         self.autoencoder = None
#         self.encoder = None
#         self.decoder = None
#         self.callbacks = []
#         if log_dir:
#             self.callbacks.append(TensorBoard(log_dir=log_dir))
#         if stop_early:
#             self.callbacks.append(EarlyStopping(monitor='val_loss', patience=2, verbose=1, mode='auto'))
#
#     def fit(self, x_train, x_test=None, epochs=5, batch_size=32):
#
#         test_data = None
#         if x_test:
#             test_data = (x_test, x_test)
#
#         self.autoencoder.fit(x_train, x_train,
#                              nb_epoch=epochs,
#                              batch_size=batch_size,
#                              shuffle=True,
#                              validation_data=test_data,
#                              callbacks=self.callbacks)
#
#     def encode(self, x):
#         return self.encoder.predict(x)
#
#     def decode(self, x):
#         return self.decoder.predict(x)
#
#     def summary(self):
#         self.autoencoder.summary()

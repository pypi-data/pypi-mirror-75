import os
from glob import glob
from typing import Any
from typing import Iterable, Iterator

import numpy as np
import tensorflow as tf
from tensorflow import keras


class DataGenerator(keras.utils.Sequence):

    def __init__(self, x_values, y_values, content_indexer=None, label_indexer=None, x_augmentor=None, batch_size=1,
                 shuffle=False):
        self.y_values = y_values  # array of y_values
        self.x_values = x_values  # array of image paths
        self.batch_size = batch_size  # batch size
        self.shuffle = shuffle  # shuffle bool
        self.on_epoch_end()
        self.content_indexer = content_indexer
        self.label_indexer = label_indexer
        self.augmentor = x_augmentor

    def __len__(self):
        'Denotes the number of batches per epoch'
        if self.x_values is not None:
            return int(np.floor(len(self.x_values) / self.batch_size))
        else:
            return int(np.floor(len(self.y_values) / self.batch_size))

    def set_batch_size(self, new_batch_size):
        self.batch_size = new_batch_size

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        if self.x_values is not None:
            self.indexes = np.arange(len(self.x_values))
        else:
            self.indexes = np.arange(len(self.y_values))

        if self.shuffle:
            np.random.shuffle(self.indexes)

    def __getitem__(self, index):
        'Generate one batch of texts'
        # selects indices of texts for next batch
        indexes = self.indexes[index * self.batch_size: (index + 1) * self.batch_size]

        # select texts and load images
        labels = None
        content = None

        if self.y_values is not None:
            labels = np.array([self.y_values[k] for k in indexes])
            if self.label_indexer:
                labels = self.label_indexer.transform(labels)
            if self.batch_size == 1:
                labels = labels[0]
        if self.x_values is not None:
            # preprocess and augment texts

            content = [self.x_values[k] for k in indexes]
            if self.augmentor:
                content = self.augmentor(content)

            if self.content_indexer:
                content = self.content_indexer.transform(content)

            if self.batch_size == 1:
                content = content[0]
            content = np.array(content)
        return content, labels

    def get_data(self):
        return [x for x, y in self], [y for x, y in self]


class FileListDataGenerator(DataGenerator):

    def __init__(self, file_paths, labels, file_reader, content_indexer=None, label_indexer=None, x_augmentor=None,
                 batch_size=64, shuffle=False):
        super().__init__(x_values=file_paths, y_values=labels, content_indexer=content_indexer,
                         label_indexer=label_indexer, x_augmentor=x_augmentor, batch_size=batch_size, shuffle=shuffle)
        self.file_reader = file_reader

    def __getitem__(self, index):
        'Generate one batch of texts'

        'Generate one batch of texts'
        # selects indices of texts for next batch
        indexes = self.indexes[index * self.batch_size: (index + 1) * self.batch_size]

        # select texts and load images
        labels = None
        content = None

        if self.y_values is not None:
            labels = np.array([self.y_values[k] for k in indexes])
            if self.label_indexer:
                labels = self.label_indexer.transform(labels)

        if self.x_values:
            # preprocess and augment texts

            content = [self.file_reader(self.x_values[k]) for k in indexes]
            if self.augmentor:
                content = self.augmentor(content)

            if self.content_indexer:
                content = self.content_indexer.transform(content)

        if self.batch_size == 1:
            content = content[0]
            labels = labels[0]
        return content, labels


class FolderDataGenerator(FileListDataGenerator):

    def __init__(self, folder_path, file_reader, content_indexer=None, x_augmentor=None,
                 batch_size=64, shuffle=False):
        file_paths = glob('{}/**'.format(folder_path), recursive=True)
        file_paths = [x.replace(os.sep, '/') for x in file_paths if os.path.isfile(x)]
        labels = [os.path.basename(os.path.dirname(x)) for x in file_paths]

        super().__init__(file_paths=file_paths, labels=labels, file_reader=file_reader, content_indexer=content_indexer,
                         x_augmentor=x_augmentor, batch_size=batch_size, shuffle=shuffle)


# class BatchDataSet(Iterable):
#     def __init__(self,
#                  corpus,
#                  *,
#                  content_indexer=None,
#                  label_indexer=None,
#                  seq_length: int = None,
#                  max_position: int = None,
#                  batch_size: int = 64,
#                  buffer_size=2000,
#                  length=None):
#         self.corpus = corpus
#         self.buffer_size = buffer_size
#         self.content_indexer = content_indexer
#         self.label_indexer = label_indexer
#
#         self.seq_length = seq_length
#         self.max_position = max_position
#         self.length=length
#         self.batch_size = batch_size
#
#     def __len__(self) -> int:
#         if self.length:
#             return max(self.length // self.batch_size, 1)
#
#         return max(len(self.corpus) // self.batch_size, 1)
#
#
#     def __iter__(self) -> Iterator:
#         batch_x, batch_y = [], []
#         for x, y in self.corpus:
#             batch_x.append(x)
#             batch_y.append(y)
#             if len(batch_x) == self.batch_size:
#                 if self.content_indexer:
#                     batch_x = self.content_indexer.transform(batch_x)
#
#                 y_tensor = self.label_indexer.transform(batch_y)
#                 yield np.array(batch_x), y_tensor
#                 batch_x, batch_y = [], []
#     def sample(self, generator):
#         buffer, is_full = [], False
#         for sample in generator:
#             buffer.append(sample)
#             if is_full:
#                 i = np.random.randint(len(buffer))
#                 yield buffer.pop(i)
#             elif len(buffer) == self.buffer_size:
#                 is_full = True
#         while buffer:
#             i = np.random.randint(len(buffer))
#             yield buffer.pop(i)
#
#     def items(self, batch_count=None):
#         """
#         take batches from the dataset
#
#         Args:
#             batch_count: number of batch count, iterate forever when batch_count is None.
#         """
#         i = 0
#         should_continue = True
#         while should_continue:
#             for batch_x, batch_y in self.__iter__():
#                 if batch_count is None or i < batch_count:
#                     i += 1
#                     yield batch_x, batch_y
#                 if batch_count and i >= batch_count:
#                     should_continue = False
#                     break
#
#         # x_shape = self.content_indexer.get_tensor_shape(self.batch_size, self.seq_length)
#         # y_shape = self.label_indexer.get_tensor_shape(self.batch_size, self.seq_length)
#         # dataset = tf.texts.Dataset.from_generator(self.__iter__,
#         #                                          output_types=(tf.int64, tf.int64),
#         #                                          output_shapes=(x_shape, y_shape))
#         # dataset = dataset.repeat()
#         # dataset = dataset.prefetch(50)
#         # if batch_count is None:
#         #     batch_count = len(self)
#         # return dataset.take(batch_count)


class Seq2SeqDataSet(Iterable):
    def __init__(self,
                 corpus,
                 *,
                 batch_size: int = 64,
                 encoder_processor,
                 decoder_processor,
                 encoder_seq_length: int = None,
                 decoder_seq_length: int = None):
        self.corpus = corpus

        self.encoder_processor = encoder_processor
        self.decoder_processor = decoder_processor

        self.encoder_seq_length = encoder_seq_length
        self.decoder_seq_length = decoder_seq_length

        self.batch_size = batch_size

    def __len__(self) -> int:
        return max(len(self.corpus) // self.batch_size, 1)

    def __iter__(self) -> Iterator:
        batch_x, batch_y = [], []
        for x, y in self.corpus:
            batch_x.append(x)
            batch_y.append(y)
            if len(batch_x) == self.batch_size:
                x_tensor = self.encoder_processor.transform(batch_x, )
                y_tensor = self.decoder_processor.transform(batch_y, )
                yield x_tensor, y_tensor
                batch_x, batch_y = [], []

    def items(self, batch_count: int = None) -> Any:
        x_shape = [self.batch_size, self.encoder_seq_length]
        y_shape = [self.batch_size, self.decoder_seq_length]
        dataset = tf.data.Dataset.from_generator(self.__iter__,
                                                 output_types=(tf.int64, tf.int64),
                                                 output_shapes=(x_shape, y_shape))
        dataset = dataset.repeat()
        dataset = dataset.prefetch(50)
        if batch_count is None:
            batch_count = len(self)
        return dataset.take(batch_count)

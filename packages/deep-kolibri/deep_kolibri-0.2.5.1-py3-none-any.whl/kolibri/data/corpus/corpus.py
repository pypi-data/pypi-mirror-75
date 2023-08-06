# encoding: utf-8

import os
from operator import itemgetter
from pathlib import Path

import pandas as pd
from tensorflow.keras.utils import get_file

from kolibri import settings as k
from kolibri.data.corpus.data_stream import DataStream
from kolibri.data.corpus.file_stream import FileStream

CORPUS_PATH = os.path.join(k.DATA_PATH, 'corpus')

Path(CORPUS_PATH).mkdir(exist_ok=True, parents=True)


class CONLL2003ENCorpus(FileStream):
    __corpus_name__ = 'conll2003_en'
    __zip_file__name = 'https://www.dropbox.com/s/c65bzd23ho73c0l/conll2003.tar.gz?dl=1'

    def __init__(self, subset_name: str = 'train', task_name: str = 'ner'):

        corpus_path = get_file(self.__corpus_name__,
                               self.__zip_file__name,
                               cache_dir=CORPUS_PATH,
                               untar=True)

        if subset_name not in {'train', 'test', 'valid'}:
            raise ValueError()
        self.task_name = task_name
        self.filepath = os.path.join(corpus_path, f'{subset_name}.txt')
        self.data_index = ['pos', 'chunking', 'ner'].index(self.task_name) + 1
        super().__init__(self.filepath, content_col=0, target_cols=self.data_index, filetype='conll')
        if self.task_name not in {'pos', 'chunking', 'ner'}:
            raise ValueError()
        self.prepare()

    def _load_data(self):
        try:
            raw_data = self.read_function(self.filepath)
            self.n_samples = 0
            for line in raw_data:
                self.n_samples += 1
                for token in line:
                    self.target_values.append(itemgetter(*self.target_columns)(token))

            self.target_values = list(self.target_values)

            self.raw_data = self.read_function(self.filepath)

        except FileNotFoundError:
            raise FileNotFoundError("File {} does not exist.".format(self.filepath))
        pass

    def __iter__(self):

        for token in self.raw_data:
            yield [d[self.content_column] for d in token], [d[self.target_columns[0]] for d in token]


class Sentiment140Corpus(FileStream):
    """

    """

    __corpus_name__ = 'Sentiments140'
    __zip_file__name = "https://www.dropbox.com/s/egk8cwupfs05g00/Sentiments140.tar.gz?dl=1"

    def __init__(self, subset_name='sentiment140_sample'):
        self.corpus_path = get_file(self.__corpus_name__,
                                    self.__zip_file__name,
                                    cache_dir=k.DATA_PATH,
                                    untar=True)

        if subset_name not in {'sentiment140_sample', 'all'}:
            raise ValueError()

        self.file_path = os.path.join(self.corpus_path, f'{subset_name}.csv')

        super().__init__(filepath=self.file_path, content_col=' text', target_cols='label')
        self.prepare()

class CreditCardFraud(DataStream):
    """

    """

    __corpus_name__ = 'creditcard_fraud'
    __zip_file__name = "https://www.dropbox.com/s/7v4tm6lsjkxnvfk/creditcard_fraud.tgz?dl=1"

    def __init__(self, subset_name='creditcard'):
        self.corpus_path = get_file(self.__corpus_name__,
                                    self.__zip_file__name,
                                    cache_dir=k.DATA_PATH,
                                    untar=True)

        if subset_name not in {'creditcard'}:
            raise ValueError()

        self.file_path = os.path.join(self.corpus_path, f'{subset_name}.csv')
        data=pd.read_csv(self.file_path)
        columns=[ c for c in data.columns if c not in ['Class', 'Time']]

        super().__init__(data=data[columns], y=data['Class'].values)
        self.prepare()


class ConsumerComplaintsCorpus(FileStream):
    """

    """

    __corpus_name__ = 'consumer_complaints'
    __zip_file__name = "https://www.dropbox.com/s/8a1pm3gg9e5szso/consumer_complaints.tar.gz?dl=1"

    def __init__(self, subset_name='sample'):
        self.corpus_path = get_file(self.__corpus_name__,
                                    self.__zip_file__name,
                                    cache_dir=k.DATA_PATH,
                                    untar=True)

        if subset_name not in {'sample', 'validate', 'train', 'test'}:
            raise ValueError()

        self.file_path = os.path.join(self.corpus_path, f'{subset_name}.csv')

        super().__init__(filepath=self.file_path, content_col='Consumer_complaint', target_cols=['Product'])
        self.prepare()


if __name__ == "__main__":
    corpus = CreditCardFraud()

    for d in corpus.X:
        print(d)


import unittest

from kolibri.data.corpus.corpus import CONLL2003ENCorpus
from kolibri.data.corpus.corpus import ConsumerComplaintsCorpus


class TestConsumerComplaintsCorpus(unittest.TestCase):

    def test_load_data(self):
        corpus = ConsumerComplaintsCorpus()
        train_x, train_y = corpus.get_data()
        assert len(train_x) == len(train_y)
        assert len(train_x) > 0
        assert train_x[:5] != train_y[:5]
        corpus = ConsumerComplaintsCorpus('test')
        test_x, test_y = corpus.get_data('')
        assert len(test_x) == len(test_y)
        assert len(test_x) > 0

        corpus = ConsumerComplaintsCorpus('train')
        test_x, test_y = corpus.get_data('')
        assert len(test_x) == len(test_y)
        assert len(test_x) > 0

        corpus = ConsumerComplaintsCorpus('validate')
        test_x, test_y = corpus.get_data('')
        assert len(test_x) == len(test_y)
        assert len(test_x) > 0


class TestCONLL2003ENCorpus(unittest.TestCase):

    def test_load_data(self):
        corpus = CONLL2003ENCorpus('train')
        train_x, train_y = corpus.get_data()

        assert len(train_x) == len(train_y)
        assert len(train_x) > 0
        assert train_x[:5] != train_y[:5]

        corpus = CONLL2003ENCorpus('test')
        test_x, test_y = corpus.get_data()
        assert len(test_x) == len(test_y)
        assert len(test_x) > 0

        corpus = CONLL2003ENCorpus('valid')
        test_x, test_y = corpus.get_data()
        assert len(test_x) == len(test_y)
        assert len(test_x) > 0


if __name__ == "__main__":
    pass

import unittest

from kolibri.data.corpus.corpus import ConsumerComplaintsCorpus
from kolibri.dnn.utils import load_data_object
from kolibri.indexers import LabelIndexer
from kolibri.tokenizer import WordTokenizer

tokenizer = WordTokenizer()


class TestClassificationProcessor(unittest.TestCase):
    def test_indexer(self):
        corpus = ConsumerComplaintsCorpus()
        x_set, y_set = corpus.get_data(nb_samples=500)
        indexer = LabelIndexer()
        indexer.build_vocab(x_set, y_set)
        transformed_idx = indexer.transform(y_set[20:40], )

        info_dict = indexer.to_dict()

        p2: LabelIndexer = load_data_object(info_dict)
        assert (transformed_idx == p2.transform(y_set[20:40], )).all()
        assert y_set[20:40] == p2.inverse_transform(transformed_idx)

    # def test_multi_label_processor(self):
    #     from kolibri.texts.corpus import ConsumerComplaintsCorpus
    #     corpus=ConsumerComplaintsCorpus()
    #     x_set, y_set = corpus.get_data(nb_samples=500)
    #     x_set=tokenizer.tokenizer(x_set)
    #     corpus_gen = CorpusGenerator(x_set, y_set)
    #
    #     indexer = LabelIndexer(multi_label=True)
    #     indexer.build_vocab_generator([corpus_gen])
    #     transformed_idx = indexer.transform(y_set[20:40])
    #
    #     info_dict = indexer.to_dict()
    #
    #     p2: LabelIndexer = load_data_object(info_dict)
    #     assert (transformed_idx == p2.transform(y_set[20:40])).all()
    #
    #     x1s = y_set[20:40]
    #     x2s = p2.inverse_transform(transformed_idx)
    #     for sample_x1, sample_x2 in zip(x1s, x2s):
    #         assert sorted(sample_x1) == sorted(sample_x2)


if __name__ == "__main__":
    pass

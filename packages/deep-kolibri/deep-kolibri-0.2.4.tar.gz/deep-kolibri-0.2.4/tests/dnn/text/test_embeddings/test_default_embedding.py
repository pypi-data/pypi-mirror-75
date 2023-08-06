import os
import random
import tempfile
import time
import unittest

from kolibri.data.corpus.corpus import ConsumerComplaintsCorpus
from kolibri.dnn.embeddings import DefaultEmbedding
from kolibri.dnn.tasks.text.classification import BiGRU_Model
from kolibri.dnn.utils import load_data_object
from kolibri.indexers import TextIndexer
from kolibri.logger import logger
from kolibri.tokenizer import WordTokenizer

sample_count = 50


class TestDefaultEmbedding(unittest.TestCase):

    def build_embedding(self):
        embedding = DefaultEmbedding()
        return embedding

    def test_base_cases(self):
        tokenizer = WordTokenizer()
        embedding = self.build_embedding()
        corpus = ConsumerComplaintsCorpus()
        x, y = corpus.get_data(nb_samples=500)
        x = tokenizer.transform(x)
        indexer = TextIndexer()
        indexer.build_vocab(x, y)
        embedding.setup_text_processor(indexer)

        samples = random.sample(x, sample_count)
        res = embedding.embed(samples)
        max_len = max([len(i) for i in samples]) + 2

        if embedding.max_position is not None:
            max_len = embedding.max_position

        assert res.shape == (len(samples), max_len, embedding.embedding_size)

        # Test Save And Load
        embed_dict = embedding.to_dict()
        embedding2 = load_data_object(embed_dict)
        embedding2.setup_text_processor(indexer)
        assert embedding2.embed(samples).shape == (len(samples), max_len, embedding.embedding_size)

    def test_with_model(self):
        tokenizer = WordTokenizer()

        corpus = ConsumerComplaintsCorpus()

        x, y = corpus.get_data(nb_samples=500)
        x = tokenizer.transform(x)
        embedding = self.build_embedding()

        model = BiGRU_Model(embedding=embedding)
        model.build_model(x, y)
        model_summary = []
        embedding.embed_model.summary(print_fn=lambda x: model_summary.append(x))
        logger.debug('\n'.join(model_summary))

        model.fit(x, y, epochs=1)

        model_path = os.path.join(tempfile.gettempdir(), str(time.time()))
        model.save(model_path)


if __name__ == "__main__":
    unittest.main()

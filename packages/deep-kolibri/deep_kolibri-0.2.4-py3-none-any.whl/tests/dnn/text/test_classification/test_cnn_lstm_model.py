import unittest

import tests.dnn.text.test_classification.test_bi_lstm_model as base
from kolibri.dnn.embeddings import WordEmbedding
from kolibri.dnn.tasks.text.classification import CNN_LSTM_Model
from tests.dnn.text.test_embeddings.test_word_embedding import sample_w2v_path


class TestCNN_LSTM_Model(base.TestBiLSTM_Model):
    @classmethod
    def setUpClass(cls):
        cls.EPOCH_COUNT = 1
        cls.TASK_MODEL_CLASS = CNN_LSTM_Model
        cls.w2v_embedding = WordEmbedding(sample_w2v_path)


if __name__ == "__main__":
    unittest.main()

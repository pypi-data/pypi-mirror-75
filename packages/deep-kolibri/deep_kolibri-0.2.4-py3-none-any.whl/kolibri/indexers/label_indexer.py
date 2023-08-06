import collections
import operator
from typing import Dict, Any, Tuple

import numpy as np
import tqdm

from kolibri.indexers.base_indexer import BaseIndexer


class LabelIndexer(BaseIndexer):

    def to_dict(self) -> Dict[str, Any]:
        data = super(LabelIndexer, self).to_dict()
        data['config']['multi_label'] = self.multi_label
        return data

    def __init__(self,
                 multi_label: bool = False,
                 **kwargs: Any) -> None:
        from sklearn.preprocessing import MultiLabelBinarizer
        super(LabelIndexer, self).__init__(**kwargs)
        self.multi_label = multi_label
        self.multi_label_binarizer = MultiLabelBinarizer(self.vocab2idx)

    def build_vocab_generator(self,
                              generators) -> None:
        from sklearn.preprocessing import MultiLabelBinarizer
        if self.vocab2idx:
            return

        vocab2idx: Dict[str, int] = {}
        token2count: Dict[str, int] = {}
        for generator in generators:
            if self.multi_label:
                for _, label in tqdm.tqdm(generator, desc="Preparing classification label vocab dict"):
                    for token in label:
                        count = token2count.get(token, 0)
                        token2count[token] = count + 1
            else:
                for _, label in tqdm.tqdm(generator, desc="Preparing classification label vocab dict"):
                    count = token2count.get(label, 0)
                    token2count[label] = count + 1

        sorted_token2count = sorted(token2count.items(),
                                    key=operator.itemgetter(1),
                                    reverse=True)
        token2count = collections.OrderedDict(sorted_token2count)

        for token, token_count in token2count.items():
            if token not in vocab2idx:
                vocab2idx[token] = len(vocab2idx)
        self.vocab2idx = vocab2idx
        self.idx2vocab = dict([(v, k) for k, v in self.vocab2idx.items()])
        self.multi_label_binarizer = MultiLabelBinarizer(self.vocab2idx)

    def get_tensor_shape(self, batch_size: int, seq_length: int) -> Tuple:
        if self.multi_label:
            return batch_size, len(self.vocab2idx)
        else:
            return (batch_size,)

    def transform(self, samples, **kwargs):
        if self.multi_label:
            sample_tensor = self.multi_label_binarizer.transform(samples)
            return sample_tensor

        sample_tensor = [self.vocab2idx[i] for i in samples]
        return np.array(sample_tensor)

    def inverse_transform(self,
                          labels,
                          *,
                          lengths=None,
                          **kwargs):
        if self.multi_label:
            return self.multi_label_binarizer.inverse_transform(labels)
        else:
            return [self.idx2vocab[i] for i in labels]


if __name__ == "__main__":
    pass

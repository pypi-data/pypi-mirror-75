import numpy as np
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from imblearn.utils import check_target_type
from sklearn.utils import check_X_y

from kolibri.utils.misc import class_label_statistics


class AutoSampler():
    """Random samples texts to bring all class frequencies into a range.
    """

    def __init__(self, min_freq=None, max_freq=None, random_state=None):
        self.min_freq = min_freq
        self.max_freq = max_freq
        self.random_state = random_state
        self.auto_balance = False

        if min_freq and max_freq:
            self.ratio = max_freq / min_freq
        else:
            self.auto_balance = True

    def fit(self, X, y):
        """Find the classes statistics before to perform sampling.
        """
        X, y = check_X_y(X, y, accept_sparse=['csr', 'csc'], dtype=None)
        y = check_target_type(y)

        if self.auto_balance:
            class_stats = class_label_statistics(y)
            std = np.std(class_stats, axis=0)
            self.min_freq = int(class_stats[-1][1] + std[1])
            self.max_freq = int(class_stats[0][1] - std[1])
            self.ratio = self.max_freq / self.min_freq

        freq = np.unique(y, return_counts=True)
        frequencies = dict(zip(freq[0], freq[1]))
        labels = list(freq[0])

        under_dict = {}
        over_dict = {}
        self.ratio_ = self.ratio
        for lbl in labels:
            count = frequencies[lbl]
            if count < self.min_freq:
                under_dict[lbl] = count
                over_dict[lbl] = self.min_freq
            elif count > self.max_freq:
                under_dict[lbl] = self.max_freq
                over_dict[lbl] = self.max_freq
            else:
                under_dict[lbl] = count
                over_dict[lbl] = count
        self.under_sampler = RandomUnderSampler(
            sampling_strategy=under_dict, random_state=self.random_state)
        self.over_sampler = RandomOverSampler(
            sampling_strategy=over_dict, random_state=self.random_state)
        return self

    def sample(self, X, y):
        """Resample the dataset.
        """
        new_X, new_y = self.under_sampler.fit_sample(X, y)
        return self.over_sampler.fit_sample(new_X, new_y)

    def fit_resample(self, X, y):
        return self.fit(X, y).sample(X, y)

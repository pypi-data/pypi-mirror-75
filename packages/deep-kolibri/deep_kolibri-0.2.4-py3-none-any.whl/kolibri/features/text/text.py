import re
import warnings
from collections import defaultdict

import numpy as np
import scipy.sparse as sp
from sklearn.feature_extraction.text import CountVectorizer, _document_frequency
from sklearn.preprocessing import normalize

FLOAT_DTYPES = (np.float64, np.float32, np.float16)
_white_spaces = re.compile(r"\s\s+")


class StreamedTfidfVectorizer(CountVectorizer):
    """Convert a collection of raw documents to a matrix of TF-IDF features.

    """

    def __init__(self, input='content', encoding='utf-8',
                 decode_error='strict', strip_accents=None, lowercase=True,
                 preindexer=None, tokenizer=None, analyzer='word',
                 stop_words=None, token_pattern=r"(?u)\b\w\w+\b",
                 ngram_range=(1, 1), max_df=1.0, min_df=1,
                 max_features=None, vocabulary=None, binary=False,
                 dtype=np.float64, norm='l2', use_idf=True, smooth_idf=True,
                 sublinear_tf=False):

        super().__init__(
            input=input, encoding=encoding, decode_error=decode_error,
            strip_accents=strip_accents, lowercase=lowercase,
            preindexer=preindexer, tokenizer=tokenizer, analyzer=analyzer,
            stop_words=stop_words, token_pattern=token_pattern,
            ngram_range=ngram_range, max_df=max_df, min_df=min_df,
            max_features=max_features, vocabulary=vocabulary, binary=binary,
            dtype=dtype)

        self.use_idf = use_idf
        self.smooth_idf = smooth_idf
        self.sublinear_tf = sublinear_tf
        self.idf_ = None
        self.norm = norm
        self.vocabulary_ = None
        self._idf_diag = None
        self.n_samples = 0

    # Broadcast the TF-IDF parameters to the underlying transformer instance
    # for easy grid search and repr

    def _check_params(self):
        if self.dtype not in FLOAT_DTYPES:
            warnings.warn("Only {} 'dtype' should be used. {} 'dtype' will "
                          "be converted to np.float64."
                          .format(FLOAT_DTYPES, self.dtype),
                          UserWarning)

    def _fit_tf_idf(self, X):
        if not sp.issparse(X):
            X = sp.csr_matrix(X)
        dtype = X.dtype if X.dtype in FLOAT_DTYPES else np.float64

        if self.use_idf:
            n_samples, n_features = X.shape
            df = _document_frequency(X)
            df = df.astype(dtype)

            # perform idf smoothing if required
            df += int(self.smooth_idf)
            n_samples += int(self.smooth_idf)

            # log+1 instead of log makes sure terms with zero idf don't get
            # suppressed entirely.
            idf = np.log(n_samples / df) + 1
            self._idf_diag = sp.diags(idf, offsets=0,
                                      shape=(n_features, n_features),
                                      format='csr',
                                      dtype=dtype)

    def finalize_partial(self):
        if self.use_idf:
            n_features = len(self._idf_diag)

            self._idf_diag = dict(sorted(self._idf_diag.items()))

            df = np.array(list(self._idf_diag.values()))

            # perform idf smoothing if required
            df += int(self.smooth_idf)
            self.n_samples += int(self.smooth_idf)

            # log+1 instead of log makes sure terms with zero idf don't get
            # suppressed entirely.
            idf = np.log(self.n_samples / df) + 1
            self._idf_diag = sp.diags(idf, offsets=0,
                                      shape=(n_features, n_features),
                                      format='csr')

    def _update_tf_idf(self, raw_documents):
        if not self.vocabulary_:
            self.vocabulary_ = defaultdict()
            self.vocabulary_.default_factory = self.vocabulary_.__len__

        if not self._idf_diag:
            self._idf_diag = {}

        analyze = self.build_analyzer()

        for doc in raw_documents:
            self.n_samples += 1
            features = set(analyze(doc))
            for feature in features:
                try:
                    feature_idx = self.vocabulary_[feature]
                    if feature_idx not in self._idf_diag:
                        self._idf_diag[feature_idx] = 1
                    else:
                        self._idf_diag[feature_idx] += 1
                except KeyError:
                    # Ignore out-of-vocabulary items for fixed_vocab=True
                    continue

    def _transform_tf_idf(self, X):
        if not sp.issparse(X):
            X = sp.csr_matrix(X, dtype=np.float64)

        n_samples, n_features = X.shape

        if self.sublinear_tf:
            np.log(X.data, X.data)
            X.data += 1

        if self.use_idf:
            # idf_ being a property, the automatic attributes detection
            # does not work as usual and we need to specify the attribute
            # name:
            expected_n_features = self._idf_diag.shape[0]
            if n_features != expected_n_features:
                raise ValueError("Input has n_features=%d while the model"
                                 " has been trained with n_features=%d" % (
                                     n_features, expected_n_features))
            # *= doesn't work
            X = X * self._idf_diag

        if self.norm:
            X = normalize(X, norm=self.norm, copy=False)

        return X

    def fit(self, raw_documents, y=None):
        """Learn vocabulary and idf from training set.
        Parameters
        ----------
        raw_documents : iterable
            An iterable which yields either str, unicode or file objects.
        y : None
            This parameter is not needed to compute tfidf.
        Returns
        -------
        self : object
            Fitted vectorizer.
        """
        self._check_params()
        X = super().fit_transform(raw_documents)
        self._fit_tf_idf(X)
        return self

    def fit_partial(self, raw_documents, y=None):
        """Learn vocabulary and idf from training set.
        Parameters incrementally
        ----------
        raw_documents : iterable
            An iterable which yields either str, unicode or file objects.
        y : None
            This parameter is not needed to compute tfidf.

       Returns
        -------
        self : object
            Fitted vectorizer.
        """

        self._update_tf_idf(raw_documents)
        return self

    def fit_transform(self, raw_documents, y=None):
        """Learn vocabulary and idf, return term-document matrix.
        This is equivalent to fit followed by transform, but more efficiently
        implemented.
        Parameters
        ----------
        raw_documents : iterable
            An iterable which yields either str, unicode or file objects.
        y : None
            This parameter is ignored.
        Returns
        -------
        X : sparse matrix, [n_samples, n_features]
            Tf-idf-weighted document-term matrix.
        """
        self._check_params()
        X = super().fit_transform(raw_documents)
        self._fit_tf_idf(X)
        # X is already a transformed view of raw_documents so
        # we set copy to False
        return self._transform_tf_idf(X)

    def transform(self, raw_documents, copy="deprecated"):
        """Transform documents to document-term matrix.
        Uses the vocabulary and document frequencies (df) learned by fit (or
        fit_transform).
        Parameters
        ----------
        raw_documents : iterable
            An iterable which yields either str, unicode or file objects.
        copy : bool, default True
            Whether to copy X and operate on the copy or perform in-place
            operations.
            .. deprecated:: 0.22
               The `copy` parameter is unused and was deprecated in version
               0.22 and will be removed in 0.24. This parameter will be
               ignored.
        Returns
        -------
        X : sparse matrix, [n_samples, n_features]
            Tf-idf-weighted document-term matrix.
        """

        # FIXME Remove copy parameter support in 0.24
        if copy != "deprecated":
            msg = ("'copy' param is unused and has been deprecated since "
                   "version 0.22. Backward compatibility for 'copy' will "
                   "be removed in 0.24.")
            warnings.warn(msg, FutureWarning)
        X = super().transform(raw_documents)

        return self._transform_tf_idf(X)

    def _more_tags(self):
        return {'X_types': ['string'], '_skip_test': True}

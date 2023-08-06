import logging

from sklearn.utils import tosequence

from kolibri.data.corpus.base_stream import BaseStream


class Pipeline():
    """ [Experimental] Holds a set of sequential operation (transforms), followed by a single estimator.
    """
    _estimator_type = 'pipeline'

    def __init__(self, steps=None):
        # Default values
        super().__init__()

        self.steps = tosequence(steps)
        self.active = False

        self.__configure()

    def __configure(self):
        """ __configure
        Initial Pipeline configuration. Validates the Pipeline's steps.
        """
        self._validate_steps()

    def predict(self, X):
        """ predict
        Sequentially applies all transforms and then predict with last step.
        Parameters
        ----------
        X: numpy.ndarray of shape (n_samples, n_features)
            All the samples we want to predict the label for.
        Returns
        -------
        list
            The predicted class label for all the samples in X.
        """
        Xt = X
        for name, transform in self.steps[:-1]:
            if transform is not None:
                Xt = transform.transform(Xt, )
        return self.steps[-1][-1].predict(Xt)

    def predict_prob(self, X):
        """ predict
        Sequentially applies all transforms and then predict with last step.
        Parameters
        ----------
        X: numpy.ndarray of shape (n_samples, n_features)
            All the samples we want to predict the label for.
        Returns
        -------
        list
            The predicted class label for all the samples in X.
        """
        Xt = X
        for name, transform in self.steps[:-1]:
            if transform is not None:
                Xt = transform.transform(Xt, )
        return self.steps[-1][-1].predict_prob(Xt)

    def numerize_label_sequences(self, y):
        return self.steps[-1][-1].indexer.numerize_label_sequences(y)

    @property
    def components(self):
        return self.steps

    def fit(self, X, y, X_val=None, y_val=None):

        """ fit
        Sequentially fit and transformer texts in all but last step, then fit
        the model in last step.
        Parameters
        ----------
        X: numpy.ndarray of shape (n_samples, n_features)
            The texts upon which the transforms/estimator will create their
            model.
        y: An array_like object of length_train n_samples
            Contains the true class y_values for all the samples in X.
        Returns
        -------
        Pipeline
            self
        """
        Xt = X
        Xt_val = X_val
        for name, transformer in self.steps[:-1]:
            if transformer is None:
                pass
            if hasattr(transformer, "fit_transform"):
                Xt = transformer.fit_transform(Xt, y)
                if Xt_val is  not None:
                    Xt_val = transformer.fit_transform(Xt_val, y_val)
            else:
                Xt = transformer.fit(Xt, y).transform(Xt, )
                if Xt_val is not None:
                    Xt_val = transformer.transform(Xt_val)

        if self._final_estimator is not None:
            self._final_estimator.fit(Xt, y, Xt_val, y_val)

        return self

    def partial_fit(self, X, y, classes=None):
        """ partial_fit
        Sequentially partial fit and transformer texts in all but last step,
        then partial fit texts in last step.
        Parameters
        ----------
        X : numpy.ndarray of shape (n_samples, n_features)
            The features to train the model.
        y: numpy.ndarray of shape (n_samples)
            An array-like with the class y_values of all samples in X.
        classes: numpy.ndarray
            Array with all possible/known class y_values. This is an optional parameter, except
            for the first partial_fit call where it is compulsory.
        Returns
        -------
        Pipeline
            self
        """
        Xt = X
        for name, transformer in self.steps[:-1]:
            if transformer is None:
                pass
            if hasattr(transformer, 'fit_transform'):
                Xt = transformer.partial_fit_transform(Xt, y, classes=classes)
            elif hasattr(transformer, 'transform'):
                Xt = transformer.transform(Xt)
            else:
                Xt = transformer.partial_fit(Xt, y).transform(Xt, )

        if self._final_estimator is not None:
            if "classes" in self._final_estimator.partial_fit.__code__.co_varnames:
                self._final_estimator.partial_fit(Xt, y, classes)
            else:
                self._final_estimator.partial_fit(Xt, y)
        return self

    def partial_fit_predict(self, X, y):
        """ partial_fit_predict
        Partial fits and transforms texts in all but last step, then partial
        fits and predicts in the last step
        Parameters
        ----------
        X: numpy.ndarray of shape (n_samples, n_features)
            All the samples we want to predict the label for.
        y: An array_like object of length_train n_samples
            Contains the true class y_values for all the samples in X
        Returns
        -------
        list
            The predicted class label for all the samples in X.
        """
        Xt = X
        for name, transform in self.steps[:-1]:
            if transform is None:
                pass
            if hasattr(transform, "partial_fit_transform"):
                Xt = transform.partial_fit_transform(Xt, y)
            else:
                Xt = transform.partial_fit(Xt, y).transform(Xt, )

        if hasattr(self._final_estimator, "partial_fit_predict"):
            return self._final_estimator.partial_fit_predict(Xt, y)
        else:
            return self._final_estimator.partial_fit(Xt, y).predict(Xt)

    def partial_fit_transform(self, X, y=None):
        """ partial_fit_transform
        Partial fits and transforms texts in all but last step, then
        partial_fit in last step
        Parameters
        ----------
        X: numpy.ndarray of shape (n_samples, n_features)
            The texts upon which the transforms/estimator will create their
            model.
        y: An array_like object of length_train n_samples
            Contains the true class y_values for all the samples in X
        Returns
        -------
        Pipeline
            self
        """
        raise NotImplementedError

    def _validate_steps(self):
        """ validate_steps
        Validates all steps, guaranteeing that there's an estimator in its last step.
        Alters the value of self.active according to the validity of the steps.
        Raises
        ------
        TypeError: If the intermediate steps or the final estimator do not implement
        the necessary functions for the pipeline to work, a TypeError is raised.
        """

        names, estimators = zip(*self.steps)
        estimator = estimators[-1]
        transformers = estimators[:-1]

        self.active = True

        for t in transformers:
            if t is None:
                continue
            else:
                if not (hasattr(t, "fit") or hasattr(t, "fit_transform")) or not hasattr(t, "transform"):
                    self.active = False
                    raise TypeError("All intermediate steps, including an evaluator, "
                                    "should implement fit and transform.")

    def stream_fit(self, stream: BaseStream, batch_size=10000):

        logging.basicConfig(format='%(message)s', level=logging.INFO)
        logging.info('Prequential Evaluation')

        while True:
            logging.info('Pre-training on %s samples.', str(batch_size))

            X, y = stream.next(batch_size)
            if len(X) == 0 or len(y) == 0:
                break

            for name, transformer in self.steps[:-1]:
                if hasattr(transformer, "transform"):
                    X = transformer.transform(X, )

            if self._final_estimator is not None:
                self._final_estimator.partial_fit(X, y, stream.target_values)

    def train(self, data, **kwargs):
        """ fit
        Sequentially fit and transform texts in all but last step, then fit
        the model in last step.
        Parameters
        ----------
        training_data: DataStream structure containing training texts

        Returns
        -------
        Pipeline
            self
        """
        training_data = data.get_all_documents()
        for name, transformer in self.steps[:-1]:
            if transformer is None:
                pass
            if hasattr(transformer, "train") and hasattr(transformer, "process"):
                transformer.train(training_data, **kwargs)
            else:
                raise Exception("train or process interface not implemented")

        if self._final_estimator is not None:
            self._final_estimator.train(training_data, **kwargs)

        return self

    def process(self, document, **kwargs):
        """Process an incoming document.
        predict
        Sequentially applies all transforms and then predict with last step.
        Parameters
        ----------
        document: the document to predict.
        Returns
        -------
        list
            The predicted class label for all the samples in X.
        """

        for name, transformer in self.steps[:-1]:
            if transformer is not None:
                transformer.process(document, **kwargs)
        return self.steps[-1][-1].process(document, **kwargs)

    def named_steps(self):
        """ named_steps
        Generates a dictionary to access all the steps' properties.
        Returns
        -------
        dictionary
            A steps dictionary, so that each step can be accessed by name.
        """
        return dict(self.steps)

    def get_info(self):
        info = "Pipeline:\n["
        names, estimators = zip(*self.steps)
        learner = estimators[-1]
        transforms = estimators[:-1]
        i = 0
        for t in transforms:
            try:
                if t.get_info() is not None:
                    info += t.get_info()
                    info += "\n"
                else:
                    info += 'Transform: no info available'
            except NotImplementedError:
                info += 'Transform: no info available'
            i += 1

        if learner is not None:
            try:
                if hasattr(learner, 'get_info'):
                    info += learner.get_info()
                else:
                    info += 'Learner: no info available'
            except NotImplementedError:
                info += 'Learner: no info available'
        info += "]"
        return info

    @property
    def _final_estimator(self):
        """ _final_estimator
        Easy to access estimator.
        Returns
        -------
        Extension of BaseClassifier
            The Pipeline's classifier
        """
        return self.steps[-1][-1]

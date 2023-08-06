import logging
import os
import time
import warnings
from timeit import default_timer as timer

from numpy import unique
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from kolibri.classifier_evaluator.metrics import confusion_matrix
from kolibri.config import TaskType
from kolibri.evaluators.base_evaluator import BaseEvaluator
from kolibri.utils import constants


class ModelEvaluator(BaseEvaluator):
    """ The prequential evaluation method, or interleaved test-then-train method,
    is an alternative to the traditional holdout evaluation, inherited from
    batch setting problems.
    """

    def __init__(self,
                 n_wait=200,
                 max_samples=100000,
                 batch_size=1,
                 pretrain_size=200,
                 train_ratio=0.8,
                 max_time=float("inf"),
                 metrics=None,
                 output_file=None,
                 show_plot=False,
                 is_stream=True,
                 data_points_for_classification=False):

        super().__init__()
        self._method = 'prequential'
        self.n_wait = n_wait
        self.max_samples = max_samples
        self.pretrain_size = pretrain_size
        self.batch_size = batch_size
        self.max_time = max_time
        self.output_file = output_file
        self.show_plot = show_plot
        self.train_ratio = train_ratio
        self.data_points_for_classification = data_points_for_classification

        if metrics is None and data_points_for_classification is False:
            self.metrics = [constants.ACCURACY, constants.KAPPA]

        elif data_points_for_classification is True:
            self.metrics = [constants.DATA_POINTS]

        else:
            self.metrics = metrics

        self.is_stream = is_stream
        self.n_sliding = n_wait

        warnings.filterwarnings("ignore", ".*invalid value encountered in true_divide.*")
        warnings.filterwarnings("ignore", ".*Passing 1d.*")

    def evaluate(self, stream, model, model_names=None, random_state=None):
        """ Evaluates a learner or set of learners on samples from a stream.

        Parameters
        ----------
        stream: Stream
            The stream from which to draw the samples.

        model: StreamModel or list
            The learner or list of learners to evaluate.

        model_names: list, optional (Default=None)
            A list with the names of the learners.

        Returns
        -------
        StreamModel or list
            The trained learner(s).

        """
        self._init_evaluation(model=model, stream=stream, model_names=model_names)

        if self._check_configuration():
            self._reset_globals()
            # Initialize metrics and outputs (plots, log files, ...)
            self._init_metrics()
            #            self._init_plot()
            self._init_file()
            if self.is_stream:
                self.model = self._train_and_test_stream()
            else:
                self.model = self._train_and_test(random_state)

            if self.show_plot:
                self.visualizer.hold()

            return self.model

    def _train_and_test_stream(self):
        """ Method to control the prequential evaluation.

        Returns
        -------
        BaseClassifier extension or list of BaseClassifier extensions
            The trained classification.

        Notes
        -----
        The classifier parameter should be an extension from the BaseClassifier. In
        the future, when BaseRegressor is created, it could be an extension from that
        class as well.

        """
        logging.basicConfig(format='%(message)s', level=logging.DEBUG)
        start_time = timer()
        end_time = timer()
        logging.info('Model Evaluation')
        logging.info('Evaluating %s label(s).', str(self.stream.n_targets))

        n_samples = self.stream.n_remaining_samples()
        if n_samples == -1 or n_samples > self.max_samples:
            n_samples = self.max_samples

        first_run = True
        if self.pretrain_size > 0:
            logging.info('Pre-training on %s samples.', str(self.pretrain_size))

            X, y = self.stream.next(self.pretrain_size)

            for i in range(self.n_models):
                self.model[i].partial_fit(X=X, y=y, classes=unique(self.stream.target_values))

            self.global_sample_count += self.pretrain_size
            first_run = False
        else:
            logging.info('No pre-training.')

        update_count = 0
        logging.info('Evaluating...')
        while ((self.global_sample_count < self.max_samples) & (end_time - start_time < self.max_time) & (
                self.stream.has_more_samples())):
            try:
                X, y = self.stream.next(self.batch_size)

                if X is not None and y is not None:
                    # Test
                    prediction = [[] for _ in range(self.n_models)]
                    for i in range(self.n_models):
                        try:
                            start = time.time()
                            prediction[i].extend(self.model[i].predict(X, return_labels=False))
                            print(time.time() - start)
                        except TypeError:
                            raise TypeError("Unexpected prediction value from {}"
                                            .format(type(self.model[i]).__name__))
                    self.global_sample_count += self.batch_size

                    for j in range(self.n_models):
                        for i in range(len(prediction[0])):
                            y_i = y[i]
                            if self._task_type != TaskType.MULTI_TARGET_REGRESSION:
                                y_i = self.model[j].numerize_label_sequences(y[i])
                            self.mean_eval_measurements[j].add_result(y_i, prediction[j][i])
                            self.current_eval_measurements[j].add_result(y_i, prediction[j][i])
                    self._check_progress(logging, n_samples)

                    # Train
                    if first_run:
                        for i in range(self.n_models):
                            if self._task_type != TaskType.REGRESSION and \
                                    self._task_type != TaskType.MULTI_TARGET_REGRESSION:
                                self.model[i].partial_fit(X, y, self.stream.target_values)
                            else:
                                self.model[i].partial_fit(X, y)
                        first_run = False
                    else:
                        for i in range(self.n_models):
                            self.model[i].partial_fit(X, y)

                    if ((self.global_sample_count % self.n_wait) == 0 or
                            (self.global_sample_count >= self.max_samples) or
                            (self.global_sample_count / self.n_wait > update_count + 1)):
                        if prediction is not None:
                            self._update_metrics()
                        update_count += 1

                end_time = timer()
            except BaseException as exc:
                print(exc)
                if exc is KeyboardInterrupt:
                    self._update_metrics()
                break

        self.evaluation_summary(logging, start_time, end_time)

        if self.is_stream:
            self.stream.restart()

        return self.model

    def _train_and_test(self, random_state=None):
        """ Method to control the prequential evaluation.

        Returns
        -------
        BaseClassifier extension or list of BaseClassifier extensions
            The trained classification.

        Notes
        -----
        The classifier parameter should be an extension from the BaseClassifier. In
        the future, when BaseRegressor is created, it could be an extension from that
        class as well.

        """
        logging.basicConfig(format='%(message)s', level=logging.DEBUG)
        start_time = timer()
        end_time = timer()
        logging.info('Model Evaluation')
        logging.info('Evaluating %s label(s).', str(self.stream.n_targets))

        n_samples = self.stream.n_remaining_samples()
        if n_samples == -1 or n_samples > self.max_samples:
            n_samples = self.max_samples

        X, y = self.stream.next(n_samples)

        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=self.train_ratio,
                                                            random_state=random_state)
        for i in range(self.n_models):
            self.model[i].fit(X=X_train, y=y_train)

        update_count = 0
        logging.info('Evaluating...')
        prediction = [[] for _ in range(self.n_models)]
        for i in range(self.n_models):
            try:
                prediction[i] = self.model[i].predict(X_test)
            except TypeError:
                raise TypeError("Unexpected prediction value from {}".format(type(self.model[i]).__name__))

        for j in range(self.n_models):
            print(classification_report(y_test, prediction[j]))
            print(confusion_matrix(y_test, prediction[j]))
        #           confusion_matrix_plot.plot_confusion_matrix_by_dict(confusion_matrix(y_test, prediction[j]))

        if self.is_stream:
            self.stream.restart()

        return self.model

    def _periodic_holdout(self):
        """ Method to control the holdout evaluation.
    The holdout evaluation method or periodic holdout evaluation method.

    Analyses each arriving sample by updating its statistics, without computing
    performance metrics, nor predicting y_values or regression values.

    The performance evaluation happens at every n_wait analysed samples, at which
    moment the evaluator will test the learners performance on a test set, formed
    by yet unseen samples, which will be used to evaluate performance, but not to
    train the model.

    It's possible to use the same test set for every test made or to dynamically
    create test sets, so that they differ from each other. If dynamic test sets
    are enabled, we use the texts stream to create test sets on the go. This process
    is more likely to generate test sets that follow the current concept, in
    comparison to static test sets.

    Thus, if concept drift is known to be present in the stream, using dynamic
    test sets is recommended. If no concept drift is expected, disabling this
    parameter will speed up the evaluation process.
        """
        self._start_time = timer()
        self._end_time = timer()
        print('Holdout Evaluation')
        print('Evaluating {} label(s).'.format(self.stream.n_targets))

        actual_max_samples = self.stream.n_remaining_samples()
        if actual_max_samples == -1 or actual_max_samples > self.max_samples:
            actual_max_samples = self.max_samples

        first_run = True

        if not self.dynamic_test_set:
            print('Separating {} holdout samples.'.format(self.test_size))
            self.X_test, self.y_test = self.stream.next(self.test_size)
            self.global_sample_count += self.test_size

        performance_sampling_cnt = 0
        print('Evaluating...')
        while ((self.global_sample_count < self.max_samples) & (self._end_time - self._start_time < self.max_time)
               & (self.stream.has_more_samples())):
            try:
                X, y = self.stream.next(self.batch_size)

                if X is not None and y is not None:
                    self.global_sample_count += self.batch_size

                    # Train
                    if first_run:
                        for i in range(self.n_models):
                            if self._task_type == constants.CLASSIFICATION:
                                self.current_eval_measurements[i].compute_training_time_begin()
                                self.model[i].partial_fit(X=X, y=y, classes=self.stream.target_values)
                                self.current_eval_measurements[i].compute_training_time_end()
                            elif self._task_type == constants.MULTI_TARGET_CLASSIFICATION:
                                self.current_eval_measurements[i].compute_training_time_begin()
                                self.model[i].partial_fit(X=X, y=y, classes=unique(self.stream.target_values))
                                self.current_eval_measurements[i].compute_training_time_end()
                            else:
                                self.current_eval_measurements[i].compute_training_time_begin()
                                self.model[i].partial_fit(X=X, y=y)
                                self.current_eval_measurements[i].compute_training_time_end()
                            self.current_eval_measurements[i].update_time_measurements(self.batch_size)
                        first_run = False
                    else:
                        for i in range(self.n_models):
                            # Compute running time
                            self.current_eval_measurements[i].compute_training_time_begin()
                            self.model[i].partial_fit(X, y)
                            self.current_eval_measurements[i].compute_training_time_end()
                            self.current_eval_measurements[i].update_time_measurements(self.batch_size)

                    self._check_progress(actual_max_samples)  # TODO Confirm place

                    # Test on holdout set
                    if self.dynamic_test_set:
                        perform_test = self.global_sample_count >= (self.n_wait * (performance_sampling_cnt + 1)
                                                                    + (self.test_size * performance_sampling_cnt))
                    else:
                        perform_test = (self.global_sample_count - self.test_size) % self.n_wait == 0

                    if perform_test | (self.global_sample_count >= self.max_samples):

                        if self.dynamic_test_set:
                            print('Separating {} holdout samples.'.format(self.test_size))
                            self.X_test, self.y_test = self.stream.next(self.test_size)
                            self.global_sample_count += get_dimensions(self.X_test)[0]

                        # Test
                        if (self.X_test is not None) and (self.y_test is not None):
                            prediction = [[] for _ in range(self.n_models)]
                            for i in range(self.n_models):
                                try:
                                    self.current_eval_measurements[i].compute_testing_time_begin()
                                    prediction[i].extend(self.model[i].predict(self.X_test, return_labels=False))
                                    self.current_eval_measurements[i].compute_testing_time_end()
                                    self.current_eval_measurements[i].update_time_measurements(self.test_size)
                                except TypeError:
                                    raise TypeError("Unexpected prediction value from {}"
                                                    .format(type(self.model[i]).__name__))
                            if prediction is not None:
                                for j in range(self.n_models):
                                    for i in range(len(prediction[0])):
                                        self.mean_eval_measurements[j].add_result(self.y_test[i],
                                                                                  prediction[j][i])
                                        self.current_eval_measurements[j].add_result(self.y_test[i],
                                                                                     prediction[j][i])

                                self._update_metrics()
                            performance_sampling_cnt += 1

                self._end_time = timer()
            except BaseException as exc:
                print(exc)
                if exc is KeyboardInterrupt:
                    self._update_metrics()
                break

        # Flush file buffer, in case it contains texts
        self._flush_file_buffer()

        self.evaluation_summary()

        if self.restart_stream:
            self.stream.restart()

        return self.model

    def set_params(self, parameter_dict):
        """ This function allows the users to change some of the evaluator's parameters,
        by passing a dictionary where keys are the parameters names, and values are
        the new parameters' values.

        Parameters
        ----------
        parameter_dict: Dictionary
            A dictionary where the keys are the names of attributes the user
            wants to change, and the values are the new values of those attributes.

        """
        for name, value in parameter_dict.items():
            if name == 'n_wait':
                self.n_wait = value
            elif name == 'max_samples':
                self.max_samples = value
            elif name == 'pretrain_size':
                self.pretrain_size = value
            elif name == 'batch_size':
                self.batch_size = value
            elif name == 'max_time':
                self.max_time = value
            elif name == 'output_file':
                self.output_file = value
            elif name == 'show_plot':
                self.show_plot = value

    def get_info(self):
        filename = "None"
        if self.output_file is not None:
            _, filename = os.path.split(self.output_file)
        return 'Prequential Evaluator: n_wait: ' + str(self.n_wait) + \
               ' - max_samples: ' + str(self.max_samples) + \
               ' - max_time: ' + str(self.max_time) + \
               ' - output_file: ' + filename + \
               ' - batch_size: ' + str(self.batch_size) + \
               ' - pretrain_size: ' + str(self.pretrain_size) + \
               ' - task_type: ' + self._task_type + \
               ' - show_plot: ' + ('True' if self.show_plot else 'False') + \
               ' - metrics: ' + (str(self.metrics) if self.metrics is not None else 'None')

from kolibri.application.postprocssor_base import PostProcessorBase
from kolibri.application.search import IndexedTextSearch
from kolibri.document import Document


class ScorePostProcessor(PostProcessorBase):
    """
    This is an abstract class that represents the interface
    that all score postprocessors should implement.

    :param search_algorithm_name: The name of the search algorithm that should
        be used to search for close matches to the provided input.
        Defaults to the value of ``Search.name``.

    :param maximum_similarity_threshold:
        The maximum amount of similarity between two document that is required
        before the search process is halted. The search for a matching document
        will continue until a document with a greater than or equal similarity
        is found or the search set is exhausted.
        Defaults to 0.95

    :param candidate_selection_method:
          The a response selection method.
          Defaults to ``get_first_response``

    :param default_response:
          The default response returned by this score adaper
          if there is no other possible response to return.
    :type default_response: str or list or tuple
    """

    def __init__(self, application, **kwargs):
        super().__init__(application, **kwargs)
        from kolibri.application.target_selection import get_first_target

        self.search_algorithm_name = kwargs.get(
            'search_algorithm_name',
            IndexedTextSearch.name
        )

        self.search_algorithm = self.application.search_algorithms[
            self.search_algorithm_name
        ]

        self.maximum_similarity_threshold = kwargs.get(
            'maximum_similarity_threshold', 0.95
        )

        # By default, select the first available response
        self.select_response = kwargs.get(
            'candidate_selection_method',
            get_first_target
        )

        default_responses = kwargs.get('default_response', [])

        # Convert a single string into a list
        if isinstance(default_responses, str):
            default_responses = [
                default_responses
            ]

        self.default_responses = [
            Document(text=default) for default in default_responses
        ]

    def can_process(self, document):
        """
        A preliminary check that is called to determine if a
        score postpressor can process a given document. By default,
        this method returns true but it can be overridden in
        child classes as needed.

        :rtype: bool
        """
        return True

    def process(self, document, additional_candidate_selection_parameters=None):
        """
        Override this method and implement your score for selecting a response to an input document.

        A confidence value and the selected response document should be returned.
        The confidence value represents a rating of how accurate the score postprocessor
        expects the selected response to be. Confidence scores are used to select
        the best response from multiple score postprocessors.

        The confidence value should be a number between 0 and 1 where 0 is the
        lowest confidence level and 1 is the highest.

        :param document: An input document to be processed by the score postprocessor.

        :param additional_candidate_selection_parameters: Parameters to be used when
            filtering results to choose a response from.

        :rtype: Document
        """
        raise NotImplementedError

    def get_default_response(self, input_document):
        """
        This method is called when a score postprocessor is unable to generate any
        other meaningful response.
        """
        from random import choice

        if self.default_responses:
            response = choice(self.default_responses)
        else:
            try:
                response = self.application.storage.get_random()
            except Exception:
                response = input_document

        self.application.logger.info(
            'No known response to the input was found. Selecting a random response.'
        )

        # Set confidence to zero because a random response is selected
        response.confidence = 0

        return response

    @property
    def class_name(self):
        """
        Return the name of the current score postprocessor class.
        This is typically used for logging and debugging.
        """
        return str(self.__class__.__name__)

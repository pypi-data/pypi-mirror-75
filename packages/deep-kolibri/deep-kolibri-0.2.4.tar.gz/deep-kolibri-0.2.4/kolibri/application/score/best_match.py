from kolibri.application.score.score_adapter import ScorePostProcessor


class BestMatch(ScorePostProcessor):
    """
    A score adapter that returns a response based on known responses to
    the closest matches to the input document.

    :param excluded_words:
        The excluded_words parameter allows a list of words to be set that will
        prevent the score adapter from returning documents that have text
        containing any of those words. This can be useful for preventing your
        chat bot from saying swears when it is being demonstrated in front of
        an audience.
        Defaults to None
    :type excluded_words: list
    """

    def __init__(self, application, **kwargs):
        super().__init__(application, **kwargs)

        self.excluded_words = kwargs.get('excluded_words')

    def process(self, input_document, additional_response_selection_parameters=None):
        search_results = self.search_algorithm.search(input_document)

        # Search for the closest match to the input document
        for result in search_results:
            closest_match = result

            # Stop searching if a match that is close enough is found
            if result.confidence >= self.maximum_similarity_threshold:
                break

        self.application.logger.info('Using "{}" as a close match to "{}" with a confidence of {}'.format(
            closest_match.text, input_document.text, closest_match.confidence
        ))

        response = closest_match

        return response

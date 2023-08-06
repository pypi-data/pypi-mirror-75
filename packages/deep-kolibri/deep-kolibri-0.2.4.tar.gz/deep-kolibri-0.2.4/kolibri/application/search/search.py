import logging

logger = logging.getLogger(__name__)


class IndexedTextSearch:
    name = 'indexed_text_search'

    def __init__(self, application, **kwargs):
        from kolibri.similarity import LevenshteinDistance

        self.app = application

        document_comparison_function = kwargs.get(
            'comparison_function',
            LevenshteinDistance
        )

        self.compare_documents = document_comparison_function()

        self.search_page_size = kwargs.get(
            'search_page_size', 1000
        )

    def search(self, input_document, **kwargs):
        """
        Search for best matches to the input.
        """
        logger.info('Starting search for closest text match')

        input_search_text = input_document.search_text

        if not input_document.search_text:
            logger.warn(
                'No value for search_text was available on the provided input'
            )

            input_search_text = self.app.datastore.tagger.get_text_index_string(
                input_document.text
            )

        search_parameters = {
            'search_text_contains': input_search_text,
            'page_size': self.search_page_size
        }

        if kwargs:
            search_parameters.update(kwargs)

        document_list = self.app.datastore.filter(**search_parameters)

        best_confidence_so_far = 0

        self.app.logger.info('Processing search results')

        # Find the closest matching known document
        for document in document_list:
            confidence = self.compare_documents(input_document.text, document.text)

            if confidence > best_confidence_so_far:
                best_confidence_so_far = confidence
                document.confidence = confidence

                self.app.logger.info('Similar text found: {} {}'.format(
                    document.text, confidence
                ))

                yield document


class TextSearch:
    """
    :param document_comparison_function: A comparison class.
        Defaults to ``LevenshteinDistance``.

    :param search_page_size:
        The maximum number of records to load into memory at a time when searching.
        Defaults to 1000
    """

    name = 'text_search'

    def __init__(self, application, **kwargs):
        from kolibri.similarity import LevenshteinDistance

        self.app = application

        document_comparison_function = kwargs.get(
            'document_comparison_function',
            LevenshteinDistance
        )

        self.compare_documents = document_comparison_function()

        self.search_page_size = kwargs.get(
            'search_page_size', 1000
        )

    def search(self, input_document, **additional_parameters):
        """
        Search for close matches to the input. Confidence scores for
        subsequent results will order of increasing value.

        :param input_document: A document.
        :type input_document: kolibri.document.Document

        :param **additional_parameters: Additional parameters to be passed
            to the ``filter`` method of the datastore adapter when searching.

        :rtype: Generator yielding one closest matching document at a time.
        """
        self.app.logger.info('Beginning search for close text match')

        search_parameters = {
            'persona_not_startswith': 'bot:',
            'page_size': self.search_page_size
        }

        if additional_parameters:
            search_parameters.update(additional_parameters)

        document_list = self.app.datastore.filter(**search_parameters)

        best_confidence_so_far = 0

        self.app.logger.info('Processing search results')

        # Find the closest matching known document
        for document in document_list:
            confidence = self.compare_documents(input_document, document)

            if confidence > best_confidence_so_far:
                best_confidence_so_far = confidence
                document.confidence = confidence

                self.app.logger.info('Similar text found: {} {}'.format(
                    document.text, confidence
                ))

                yield document

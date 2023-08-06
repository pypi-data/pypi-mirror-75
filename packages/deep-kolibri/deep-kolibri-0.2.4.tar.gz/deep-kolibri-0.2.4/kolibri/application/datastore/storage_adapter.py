import logging

from kolibri.application.datastore.index_tagger import PosLemmaIndexTagger

logger = logging.getLogger(__name__)


class DatabaseAdapter(object):
    """
    Abstract class that represents the interface
    that all database adapters have to implement.
    """

    def __init__(self, language='en'):
        """
        :param str language: The language for the tagger .
        """

        self.tagger = PosLemmaIndexTagger(language)

    def get_model(self, model_name):
        """
        Return the model class for a given model name.

        model_name is case insensitive.
        """
        get_model_method = getattr(self, 'get_%s_model' % (
            model_name.lower(),
        ))

        return get_model_method()

    def get_object(self, object_name):
        """
        Return the class for a given object name.

        object_name is case insensitive.
        """
        get_model_method = getattr(self, 'get_%s_object' % (
            object_name.lower(),
        ))

        return get_model_method()

    def get_document_object(self):
        from kolibri.document import Document

        DocumentModel = self.get_model('document')

        Document.document_field_names.extend(
            DocumentModel.extra_document_field_names
        )

        return Document

    def count(self):
        """
        Return the number of entries in the database.
        """
        raise NotImplementedError(
            'The `count` method is not implemented by this adapter.'
        )

    def remove(self, document_text):
        """
        Removes the document that matches the input text.
        """
        raise NotImplementedError(
            'The `remove` method is not implemented by this adapter.'
        )

    def filter(self, **kwargs):
        """
        Returns a list of objects from the database.
        The kwargs parameter can contain any number
        of attributes.

        :param page_size: The maximum number of records to load into
            memory at once when returning results.
            Defaults to 1000

        :param order_by: The field that will be sorted

        :param tags: A list of tags. When specified, the results will only
            include documents that have a tag in the provided list.

        :param exclude_text: documents that contain this text will not be retrieved.
            Defaults to None

        :param exclude_text_words: document that contain any word form the list will
        not be retrieved


        :param search_text_contains: If the ``search_text`` field of a
            document from the provided stringù; it will be returned.
        """
        raise NotImplementedError(
            'The `filter` method is not implemented by this adapter.'
        )

    def create(self, **kwargs):
        """
        Creates a new document matching the keyword arguments specified.
        Returns the created document.
        """
        raise NotImplementedError(
            'The `create` method is not implemented by this adapter.'
        )

    def create_multiple(self, documents):
        """
        Creates multiple document entries.
        """
        raise NotImplementedError(
            'The `create_many` method is not implemented by this adapter.'
        )

    def update(self, document):
        """
        Modifies an entry in the database.
        Creates an entry if one does not exist.
        """
        raise NotImplementedError(
            'The `update` method is not implemented by this adapter.'
        )

    def get_random(self):
        """
        Returns a random document from the database.
        """
        raise NotImplementedError(
            'The `get_random` method is not implemented by this adapter.'
        )

    def drop(self):
        """
        Drop the database attached to a given adapter.
        """
        raise NotImplementedError(
            'The `drop` method is not implemented by this adapter.'
        )

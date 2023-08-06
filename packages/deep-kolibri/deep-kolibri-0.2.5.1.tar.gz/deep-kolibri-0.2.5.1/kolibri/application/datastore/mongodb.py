import re

from kolibri.application.datastore import DatabaseAdapter


class MongoDatabaseAdapter(DatabaseAdapter):
    """
    The MongoDatabaseAdapter is an interface that allows
    kolibri to store documents in a MongoDB database.

    :keyword database_uri: The URI of a remote instance of MongoDB.
                           This can be any valid
                           `MongoDB connection string <https://docs.mongodb.com/manual/reference/connection-string/>`_
    :type database_uri: str

    .. code-block:: python

       database_uri='mongodb://example.com:8100/'
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from pymongo import MongoClient
        from pymongo.errors import OperationFailure

        self.database_uri = kwargs.get(
            'database_uri', 'mongodb://localhost:27017/kolibri-database'
        )

        # Use the default host and port
        self.client = MongoClient(self.database_uri)

        # Increase the sort buffer to 42M if possible
        try:
            self.client.admin.command({'setParameter': 1, 'internalQueryExecMaxBlockingSortBytes': 44040192})
        except OperationFailure:
            pass

        # Specify the name of the database
        self.database = self.client.get_database()

        # The mongo collection of document documents
        self.documents = self.database['documents']

    def get_document_model(self):
        """
        Return the class for the document model.
        """
        from kolibri.document import Document

        # Create a datastore-aware document
        document = Document
        document.storage = self

        return document

    def count(self):
        return self.documents.count()

    def mongo_to_object(self, document_data):
        """
        Return Document object when given texts
        returned from Mongo DB.
        """
        Document = self.get_model('document')

        document_data['id'] = document_data['_id']

        return Document(**document_data)

    def filter(self, **kwargs):
        """
        Returns a list of documents in the database
        that match the parameters specified.
        """
        import pymongo

        page_size = kwargs.pop('page_size', 1000)
        order_by = kwargs.pop('order_by', None)
        tags = kwargs.pop('tags', [])
        exclude_text = kwargs.pop('exclude_text', None)
        exclude_text_words = kwargs.pop('exclude_text_words', [])
        search_text_contains = kwargs.pop('search_text_contains', None)

        if tags:
            kwargs['tags'] = {
                '$in': tags
            }

        if exclude_text:
            if 'text' not in kwargs:
                kwargs['text'] = {}
            elif 'text' in kwargs and isinstance(kwargs['text'], str):
                text = kwargs.pop('text')
                kwargs['text'] = {
                    '$eq': text
                }
            kwargs['text']['$nin'] = exclude_text

        if exclude_text_words:
            if 'text' not in kwargs:
                kwargs['text'] = {}
            elif 'text' in kwargs and isinstance(kwargs['text'], str):
                text = kwargs.pop('text')
                kwargs['text'] = {
                    '$eq': text
                }
            exclude_word_regex = '|'.join([
                '.*{}.*'.format(word) for word in exclude_text_words
            ])
            kwargs['text']['$not'] = re.compile(exclude_word_regex)

        if search_text_contains:
            or_regex = '|'.join([
                '{}'.format(re.escape(word)) for word in search_text_contains.split(' ')
            ])
            kwargs['search_text'] = re.compile(or_regex)

        mongo_ordering = []

        if order_by:

            # Sort so that newer datetimes appear first
            if 'created_at' in order_by:
                order_by.remove('created_at')
                mongo_ordering.append(('created_at', pymongo.DESCENDING,))

            for order in order_by:
                mongo_ordering.append((order, pymongo.ASCENDING))

        total_documents = self.documents.find(kwargs).count()

        for start_index in range(0, total_documents, page_size):
            if mongo_ordering:
                for match in self.documents.find(kwargs).sort(mongo_ordering).skip(start_index).limit(page_size):
                    yield self.mongo_to_object(match)
            else:
                for match in self.documents.find(kwargs).skip(start_index).limit(page_size):
                    yield self.mongo_to_object(match)

    def create(self, **kwargs):
        """
        Creates a new document matching the keyword arguments specified.
        Returns the created document.
        """
        Document = self.get_model('document')

        if 'tags' in kwargs:
            kwargs['tags'] = list(set(kwargs['tags']))

        if 'search_text' not in kwargs:
            kwargs['search_text'] = self.tagger.get_text_index_string(kwargs['text'])

        if 'search_target_text' not in kwargs:
            if kwargs.get('in_response_to'):
                kwargs['search_target_text'] = self.tagger.get_text_index_string(kwargs['in_response_to'])

        inserted = self.documents.insert_one(kwargs)

        kwargs['id'] = inserted.inserted_id

        return Document(**kwargs)

    def create_many(self, documents):
        """
        Creates multiple document entries.
        """
        create_documents = []

        for document in documents:
            document_data = document.serialize()
            tag_data = list(set(document_data.pop('tags', [])))
            document_data['tags'] = tag_data

            if not document.search_text:
                document_data['search_text'] = self.tagger.get_text_index_string(document.text)

            if not document.search_target_text and document.in_response_to:
                document_data['search_target_text'] = self.tagger.get_text_index_string(document.in_response_to)

            create_documents.append(document_data)

        self.documents.insert_many(create_documents)

    def update(self, document):
        data = document.serialize()
        data.pop('id', None)
        data.pop('tags', None)

        data['search_text'] = self.tagger.get_text_index_string(data['text'])

        if data.get('in_response_to'):
            data['search_target_text'] = self.tagger.get_text_index_string(data['in_response_to'])

        update_data = {
            '$set': data
        }

        if document.tags:
            update_data['$addToSet'] = {
                'tags': {
                    '$each': document.tags
                }
            }

        search_parameters = {}

        if document.id is not None:
            search_parameters['_id'] = document.id
        else:
            search_parameters['text'] = document.text
            search_parameters['document'] = document.document

        update_operation = self.documents.update_one(
            search_parameters,
            update_data,
            upsert=True
        )

        if update_operation.acknowledged:
            document.id = update_operation.upserted_id

        return document

    def get_random(self):
        """
        Returns a random document from the database
        """
        from random import randint

        count = self.count()

        if count < 1:
            raise Exception('database is empty')

        random_integer = randint(0, count - 1)

        documents = self.documents.find().limit(1).skip(random_integer)

        return self.mongo_to_object(list(documents)[0])

    def remove(self, document_text):
        """
        Removes the document that matches the input text.
        """
        self.documents.delete_one({'text': document_text})

    def drop(self):
        """
        Remove the database.
        """
        self.client.drop_database(self.database.name)

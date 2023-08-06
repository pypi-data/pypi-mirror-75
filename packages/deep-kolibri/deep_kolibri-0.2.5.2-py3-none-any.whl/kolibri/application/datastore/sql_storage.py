import logging

from kolibri.application.datastore.storage_adapter import DatabaseAdapter

logger = logging.getLogger(__name__)


class SQLDatabaseAdapter(DatabaseAdapter):
    """
    The SQLDatabaseAdapter allows kolibri to store documents
    texts in any database supported by the SQL Alchemy ORM.

    All parameters are optional, by default a sqlite database is used.

    :keyword database_uri: eg: sqlite:///database_test.sqlite3',
        The database_uri can be specified to choose database driver.
    :type database_uri: str
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker

        self.database_uri = kwargs.get('database_uri', False)

        # None results in a sqlite in-memory database as the default
        if self.database_uri is None:
            self.database_uri = 'sqlite://'

        # Create a file database if the database is not a connection string
        if not self.database_uri:
            self.database_uri = 'sqlite:///db.sqlite3'

        self.engine = create_engine(self.database_uri, convert_unicode=True)

        if self.database_uri.startswith('sqlite://'):
            from sqlalchemy.engine import Engine
            from sqlalchemy import event

            @event.listens_for(Engine, 'connect')
            def set_sqlite_pragma(dbapi_connection, connection_record):
                dbapi_connection.execute('PRAGMA journal_mode=WAL')
                dbapi_connection.execute('PRAGMA synchronous=NORMAL')

        if not self.engine.dialect.has_table(self.engine, 'Document'):
            self.create_database()

        self.Session = sessionmaker(bind=self.engine, expire_on_commit=True)

    def get_document_model(self):
        """
        Return the document model.
        """
        from kolibri.application.datastore.sqlalchemy_models.models import Document
        return Document

    def get_tag_model(self):
        """
        Return the document model.
        """
        from kolibri.application.datastore.sqlalchemy_models.models import Tag
        return Tag

    def model_to_object(self, document):
        from kolibri.document import Document as DocumentObject

        return DocumentObject(**document.serialize())

    def count(self):
        """
        Return the number of entries in the database.
        """
        Document = self.get_model('document')

        session = self.Session()
        document_count = session.query(Document).count()
        session.close()
        return document_count

    def remove(self, document_text):
        """
        Removes the document that matches the input text.
        Removes any responses from documents where the response text matches
        the input text.
        """
        Document = self.get_model('document')
        session = self.Session()

        query = session.query(Document).filter_by(text=document_text)
        record = query.first()

        session.delete(record)

        self._session_finish(session)

    def filter(self, **kwargs):
        """
        Returns a list of objects from the database.
        The kwargs parameter can contain any number
        of attributes. Only objects which contain all
        listed attributes and in which all values match
        for all listed attributes will be returned.
        """
        from sqlalchemy import or_

        Document = self.get_model('document')
        Tag = self.get_model('tag')

        session = self.Session()

        page_size = kwargs.pop('page_size', 1000)
        order_by = kwargs.pop('order_by', None)
        tags = kwargs.pop('tags', [])
        exclude_text = kwargs.pop('exclude_text', None)
        exclude_text_words = kwargs.pop('exclude_text_words', [])
        search_text_contains = kwargs.pop('search_text_contains', None)

        # Convert a single sting into a list if only one tag is provided
        if type(tags) == str:
            tags = [tags]

        if len(kwargs) == 0:
            documents = session.query(Document).filter()
        else:
            documents = session.query(Document).filter_by(**kwargs)

        if tags:
            documents = documents.join(Document.tags).filter(
                Tag.name.in_(tags)
            )

        if exclude_text:
            documents = documents.filter(
                ~Document.text.in_(exclude_text)
            )

        if exclude_text_words:
            or_word_query = [
                Document.text.ilike('%' + word + '%') for word in exclude_text_words
            ]
            documents = documents.filter(
                ~or_(*or_word_query)
            )

        if search_text_contains:
            or_query = [
                Document.search_text.contains(word) for word in search_text_contains.split(' ')
            ]
            documents = documents.filter(
                or_(*or_query)
            )

        if order_by:

            if 'created_at' in order_by:
                index = order_by.index('created_at')
                order_by[index] = Document.created_at.asc()

            documents = documents.order_by(*order_by)

        total_documents = documents.count()

        for start_index in range(0, total_documents, page_size):
            for document in documents.slice(start_index, start_index + page_size):
                yield self.model_to_object(document)

        session.close()

    def create(self, **kwargs):
        """
        Creates a new document matching the keyword arguments specified.
        Returns the created document.
        """
        Document = self.get_model('document')
        Tag = self.get_model('tag')

        session = self.Session()

        tags = set(kwargs.pop('tags', []))

        if 'search_text' not in kwargs:
            kwargs['search_text'] = self.tagger.get_text_index_string(kwargs['text'])

        document = Document(**kwargs)

        for tag_name in tags:
            tag = session.query(Tag).filter_by(name=tag_name).first()

            if not tag:
                # Create the tag
                tag = Tag(name=tag_name)

            document.tags.append(tag)

        session.add(document)

        session.flush()

        session.refresh(document)

        document_object = self.model_to_object(document)

        self._session_finish(session)

        return document_object

    def create_many(self, documents):
        """
        Creates multiple document entries.
        """
        Document = self.get_model('document')
        Tag = self.get_model('tag')

        session = self.Session()

        create_documents = []
        create_tags = {}

        for document in documents:

            document_data = document.serialize()
            tag_data = document_data.pop('tags', [])

            document_model_object = Document(**document_data)

            if not document.search_text:
                document_model_object.search_text = self.tagger.get_text_index_string(document.text)

            if not document.search_target_text and document.target_text:
                document_model_object.search_target_text = self.tagger.get_text_index_string(document.target_text)

            new_tags = set(tag_data) - set(create_tags.keys())

            if new_tags:
                existing_tags = session.query(Tag).filter(
                    Tag.name.in_(new_tags)
                )

                for existing_tag in existing_tags:
                    create_tags[existing_tag.name] = existing_tag

            for tag_name in tag_data:
                if tag_name in create_tags:
                    tag = create_tags[tag_name]
                else:
                    # Create the tag if it does not exist
                    tag = Tag(name=tag_name)

                    create_tags[tag_name] = tag

                document_model_object.tags.append(tag)
            create_documents.append(document_model_object)

        session.add_all(create_documents)
        session.commit()

    def update(self, document):
        """
        Modifies an entry in the database.
        Creates an entry if one does not exist.
        """
        Document = self.get_model('document')
        Tag = self.get_model('tag')

        if document is not None:
            session = self.Session()
            record = None

            if hasattr(document, 'id') and document.id is not None:
                record = session.query(Document).get(document.id)
            else:
                record = session.query(Document).filter(
                    Document.text == document.text,
                    Document.document == document.document,
                ).first()

                # Create a new document entry if one does not already exist
                if not record:
                    record = Document(
                        text=document.text,
                        document=document.document,
                        persona=document.persona
                    )

            # Update the response value
            record.in_response_to = document.in_response_to

            record.created_at = document.created_at

            record.search_text = self.tagger.get_text_index_string(document.text)

            if document.in_response_to:
                record.search_target_text = self.tagger.get_text_index_string(document.in_response_to)

            for tag_name in document.get_tags():
                tag = session.query(Tag).filter_by(name=tag_name).first()

                if not tag:
                    # Create the record
                    tag = Tag(name=tag_name)

                record.tags.append(tag)

            session.add(record)

            self._session_finish(session)

    def get_random(self):
        """
        Returns a random document from the database.
        """
        import random

        Document = self.get_model('document')

        session = self.Session()
        count = self.count()
        if count < 1:
            raise Exception('database is empty')

        random_index = random.randrange(0, count)
        random_document = session.query(Document)[random_index]

        document = self.model_to_object(random_document)

        session.close()
        return document

    def drop(self):
        """
        Drop the database.
        """
        Document = self.get_model('document')
        Tag = self.get_model('tag')

        session = self.Session()

        session.query(Document).delete()
        session.query(Tag).delete()

        session.commit()
        session.close()

    def create_database(self):
        """
        Populate the database with the tables.
        """
        from kolibri.application.datastore.sqlalchemy_models.models import Base
        Base.metadata.create_all(self.engine)

    def _session_finish(self, session, document_text=None):
        from sqlalchemy.exc import InvalidRequestError
        try:
            session.commit()
        except InvalidRequestError:
            # Log the document text and the exception
            logger.exception(document_text)
        finally:
            session.close()

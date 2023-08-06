from kolibri.document import Document


class MemoryLearner():
    """
    Allows a chat bot to be trained using a list of strings
    where the list represents a conversation.
    """

    def __init__(self, application):
        self.application = application

    def fit(self, X, y):
        raise NotImplementedError

    def train(self, texts, target_texts, **kwargs):
        """
        Train model based on the provided list of
        documents.
        """

        documents_to_create = []

        for conversation_count, text in enumerate(texts):
            document_search_text = self.application.datastore.tagger.get_text_index_string(text)
            target_document_text = target_texts[conversation_count]
            target_document_search_text = self.application.datastore.tagger.get_text_index_string(target_document_text)

            document = Document(
                text=text,
                search_text=document_search_text,
                target_text=target_document_text,
                search_target_text=target_document_search_text,
                label='training'
            )

            documents_to_create.append(document)

        self.application.datastore.create_many(documents_to_create)

from datetime import datetime

from kolibri.utils import ordered


class DocumentBase(object):
    """
    This class has shared methods used to
    normalize different document models.
    """

    document_field_names = [
        'id',
        'text',
        'search_text',
        'label',
        'tags',
        'created_at',
    ]

    extra_document_field_names = []

    def get_document_field_names(self):
        """
        Return the list of field names for the statement.
        """
        return self.document_field_names + self.extra_document_field_names

    def get_tags(self):
        """
        Return the list of tags for this statement.
        """
        return self.tags

    def add_tags(self, *tags):
        """
        Add a list of strings to the statement as tags.
        """
        self.tags.extend(tags)

    def serialize(self):
        """
        :returns: A dictionary representation of the statement object.
        :rtype: dict
        """
        data = {}
#        print(self.get_document_field_names())
        for field_name in self.get_document_field_names():
            format_method = getattr(self, 'get_{}'.format(
                field_name
            ), None)

            if format_method:
                data[field_name] = format_method()
            else:
                data[field_name] = getattr(self, field_name)

        return data


class Document(DocumentBase):


    __slots__ = (
        'id',
        'text',
        'search_text',
        'label',
        'target_text',
        'search_target_text',
        'tags',
        'created_at',
        'confidence',
        'output_properties'
    )
    def __init__(self,  **kwargs ):
        self.id = kwargs.get('id')
        self.text = kwargs.get('text', '')
        self.created_at = kwargs.get('created_at', datetime.now())
        self.label = kwargs.get('label', '')
        self.output_properties = kwargs.get('output_properties', set())
        self.tags = kwargs.pop('tags', [])
        self.search_text = kwargs.get('search_text', '')
        self.target_text= kwargs.get('target_text', '')
        self.search_target_text= kwargs.get('search_target_text', '')
        self.extra_document_field_names.extend(['target_text', 'search_target_text'])
        self.time = kwargs.get('time', None)
        self.target = kwargs.get('target', None)
        self.tokens = None

        output_properties = kwargs.get('output_properties', None)

        if output_properties:
            self.output_properties = output_properties
        else:
            self.output_properties = set()

        self.data={}



    def set_output_property(self, prop):
        self.output_properties.add(prop)

    def entities(self):
        return self.data['entities']

    def as_dict(self, only_output_properties=False):
        if only_output_properties:
            d = {key: value
                 for key, value in self.__dict__.items()
                 if key in self.output_properties}
            return dict(d, text=self.text)
        else:
            d = self
        return dict(target=d.label, text=self.text)

    def __eq__(self, other):
        if not isinstance(other, Document):
            return False
        else:
            return ((other.text, ordered(other.data)) ==
                    (self.text, ordered(self.data)))

    def __hash__(self):
        return hash((self.text, str(ordered(self.data))))

    # @property
    # def sentences(self):
    #     if self.tokens:
    #         return self.tokens
    #     else:
    #         return self._sentences
    #
    # @sentences.setter
    # def sentences(self, new_sentences):
    #     self._sentences = new_sentences

    @classmethod
    def build(cls, text, aClass=None, entities=None):
        data = {}
        if aClass:
            data["label"] = aClass
        if entities:
            data["entities"] = entities
        return cls(text)

from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from kolibri import settings as constants
from kolibri.document import DocumentBase


class ModelBase(object):
    """
    An augmented base class for SqlAlchemy models.
    """

    @declared_attr
    def __tablename__(cls):
        """
        Return the lowercase class name as the name of the table.
        """
        return cls.__name__.lower()

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )


Base = declarative_base(cls=ModelBase)

tag_association_table = Table(
    'tag_association',
    Base.metadata,
    Column('tag_id', Integer, ForeignKey('tag.id')),
    Column('document_id', Integer, ForeignKey('document.id'))
)


class Tag(Base):
    """
    A tag that describes a document.
    """

    name = Column(
        String(constants.TAG_NAME_MAX_LENGTH),
        unique=True
    )


class Document(Base, DocumentBase):
    """
    A Document represents a sentence or phrase.
    """

    confidence = 0

    text = Column(
        String(constants.DOCUMENT_TEXT_MAX_LENGTH)
    )

    search_text = Column(
        String(constants.DOCUMENT_TEXT_MAX_LENGTH),
        nullable=False,
        server_default=''
    )

    label = Column(
        String(constants.DOCUMENT_LABEL_MAX_LENGTH),
        nullable=False,
        server_default=''
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    target_text = Column(
        String(constants.DOCUMENT_TEXT_MAX_LENGTH),
        nullable=True
    )

    search_target_text = Column(
        String(constants.DOCUMENT_TEXT_MAX_LENGTH),
        nullable=False,
        server_default=''
    )

    tags = relationship(
        'Tag',
        secondary=lambda: tag_association_table,
        backref='documents'
    )

    def get_tags(self):
        """
        Return a list of tags for this document.
        """
        return [tag.name for tag in self.tags]

    def add_tags(self, *tags):
        """
        Add a list of strings to the document as tags.
        """
        self.tags.extend([
            Tag(name=tag) for tag in tags
        ])

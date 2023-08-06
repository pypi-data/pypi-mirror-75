import logging

from kolibri import utils
from kolibri.application.search import *

logger = logging.getLogger(__name__)


class App(object):
    """
    A conversational dialog chat bot.
    """

    def __init__(self, name, **kwargs):
        self.name = name

        database_adapter = kwargs.get('database_adapter', 'kolibri.application.datastore.SQLDatabaseAdapter')

        self.datastore = utils.misc.initialize_class(database_adapter, **kwargs)

        postprocessors = kwargs.get('postprocessor', [
            'kolibri.application.score.BestMatch'
        ])

        primary_search_algorithm = IndexedTextSearch(self, **kwargs)
        text_search_algorithm = TextSearch(self, **kwargs)

        self.search_algorithms = {
            primary_search_algorithm.name: primary_search_algorithm,
            text_search_algorithm.name: text_search_algorithm
        }
        self.postprocessors = []

        for postprocessor in postprocessors:
            postprocessor_class = utils.initialize_class(postprocessor, self, **kwargs)
            self.postprocessors.append(postprocessor_class)

        self.logger = logger
        # Allow the app to save input it receives so that it can learn
        self.read_only = kwargs.get('read_only', False)

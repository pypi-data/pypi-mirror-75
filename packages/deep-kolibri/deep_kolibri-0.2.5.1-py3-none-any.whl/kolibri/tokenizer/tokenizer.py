"""
Tokenizer Interface
"""

from kolibri.kolibri_component import Component


class Tokenizer(Component):
    def __init__(self, config={}):
        super().__init__(config)
        self.tokenizer = None

    def tokenize(self, text):
        raise NotImplementedError

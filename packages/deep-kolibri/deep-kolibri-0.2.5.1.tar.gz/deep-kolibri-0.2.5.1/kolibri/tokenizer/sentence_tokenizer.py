from kolibri.tokenizer.tokenizer import Tokenizer
from kolibri.tools.sentence_splitter import split_single


class SentenceTokenizer(Tokenizer):
    name = "sentence_tokenizer"

    provides = ["sentences"]

    def process(self, document, **kwargs):
        document.sentences = self.tokenize(document.text)
        document.raw_text = None

    def tokenize(self, text):
        sentences = split_single(text)

        return [sent.strip() for sent in sentences if len(sent.strip()) > 0]

    def transform(self, X):
        return [self.tokenize(x) for x in X]

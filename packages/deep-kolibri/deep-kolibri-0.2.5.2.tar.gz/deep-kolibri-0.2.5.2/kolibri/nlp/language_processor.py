import logging

from kolibri.sentence import Sentence
from kolibri.stopwords import get_stop_words
from kolibri.token import Token
from kolibri.tokenizer.sentence_tokenizer import split_single
from kolibri.tools.freeling.pyfreeling import freelingWrapper


class LanguageProcessor:
    def __init__(self, language='en', logging_level=logging.WARNING):
        self.logging_level = logging_level
        self.freelang = freelingWrapper(50101)

        self.language = language
        logging.basicConfig(level=self.logging_level)
        self.stopwords = get_stop_words(self.language)

    def __enter__(self):
        return self

    def process_annotated(self, annotated):
        sentence_elements = annotated.split('\n')
        sentence = Sentence()
        for words in sentence_elements:
            element = words.split()
            token = Token()
            token.id = element[0]
            token.text = str(element[1])
            token.lemma = element[2]
            token.coarse_pos = element[3]
            token.pos = element[4]
            token.is_stop = token.text in self.stopwords
            token.is_alpha = token.is_alpha = token.text.isalpha()
            token.isnumeric = token.text.isnumeric()
            token.islower = token.text.islower()
            token.istitle = token.text.istitle()
            token.isupper = token.text.isupper()
            token.data_dic = {d.split('=')[0]: d.split('=')[1] for d in element[5].split('|')}
            sentence.tokens.append(token)

        return sentence

    def __call__(self, text, split_sentences=False):
        sentences = []
        if split_sentences:
            sents = split_single(text)
            annotated = self.freelang.process_sentences(sents)
        else:
            annotated = self.freelang.process_sentences([text])

        for ann in annotated:
            sentences.append(self.process_annotated(ann))
        return sentences

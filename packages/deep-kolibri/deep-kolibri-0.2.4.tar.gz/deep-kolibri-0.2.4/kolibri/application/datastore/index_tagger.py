import string


class PosLemmaIndexTagger(object):

    def __init__(self, language='en'):
        from kolibri.nlp.language_processor import LanguageProcessor
        self.nlp = LanguageProcessor(language)
        self.language = language

        self.punctuation_table = str.maketrans(dict.fromkeys(string.punctuation))

    def get_text_index_string(self, text):
        """
        Return a string of text containing part-of-speech, lemma pairs.
        """
        bigram_pairs = []

        if len(text) <= 2:
            text_without_punctuation = text.translate(self.punctuation_table)
            if len(text_without_punctuation) >= 1:
                text = text_without_punctuation

        document = self.nlp(text)

        if len(text) <= 2:
            bigram_pairs = [
                token.lemma_.lower() for token in document
            ]
        else:
            tokens = [
                token for token in document[0].tokens if token.is_alpha and not token.is_stop
            ]

            if len(tokens) < 2:
                tokens = [
                    token for token in document[0].tokens if token.is_alpha
                ]

            for index in range(1, len(tokens)):
                bigram_pairs.append('{}:{}'.format(
                    tokens[index - 1].pos,
                    tokens[index].lemma.lower()
                ))

        if not bigram_pairs:
            bigram_pairs = [
                token.lemma.lower() for token in document[0].tokens
            ]

        return ' '.join(bigram_pairs)

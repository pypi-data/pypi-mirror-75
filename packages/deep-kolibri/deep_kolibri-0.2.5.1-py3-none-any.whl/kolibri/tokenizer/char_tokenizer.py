import string
import sys
import warnings

from six.moves import range

from kolibri.stopwords import get_stop_words
from kolibri.tokenizer.tokenizer import *

if sys.version_info < (3,):
    maketrans = string.maketrans
else:
    maketrans = str.maketrans

punctuations = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n'


def remove_punctuations(text, split=' ', filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n'):
    if sys.version_info < (3,):
        if isinstance(text, unicode):  # noqa: F821
            translate_map = {
                ord(c): unicode(split) for c in filters  # noqa: F821
            }
            text = text.translate(translate_map)
        elif len(split) == 1:
            translate_map = maketrans(filters, split * len(filters))
            text = text.translate(translate_map)
        else:
            for c in filters:
                text = text.replace(c, split)
    else:
        translate_dict = {c: split for c in filters}
        translate_map = maketrans(translate_dict)
        text = text.translate(translate_map)
    return text.strip()


def ngram(text, n=1, stride=None):
    if stride == None:
        stride = n
    return [text[i:i + n] for i in range(0, len(text), stride)]


def text_to_word_sequence(text,
                          filters=None,
                          lower=True, split=" "):
    """Converts a text to a sequence of words (or tokens).
    # Arguments
        text: Input text (string).
        filters: list (or concatenation) of characters to filter out, such as
            punctuation. Default: ``!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\\t\\n``,
            includes basic punctuation, tabs, and newlines.
        lower: boolean. Whether to convert the input to lowercase.
        split: str. Separator for word splitting.
    # Returns
        A list of words (or tokens).
    """
    if lower:
        text = text.lower()

    if filters:
        text = remove_punctuations(text, split, filters)
    seq = text.split(split)
    return [i for i in seq if i]


class CharTokenizer(Tokenizer):
    """Text tokenization utility class inspired from keras
    """
    name = "char_tokenizer"

    provides = ["tokens"]
    defaults = {
        "remove-stopwros": False,
        "language": 'en',
        "lower-case": True,
        "remove-punct": False,
        "ngram": 1
    }

    def __init__(self, config, **kwargs):
        # Legacy support
        super().__init__(config)
        if 'nb_words' in kwargs:
            warnings.warn('The `nb_words` argument in `Tokenizer` '
                          'has been renamed `num_words`.')
            num_words = kwargs.pop('nb_words')
        if kwargs:
            raise TypeError('Unrecognized keyword arguments: ' + str(kwargs))
        self.lower = self.component_config['lower-case']
        self.remove_stopwords = self.component_config['remove-stopwros']
        self.remove_punctuations = self.component_config["remove-punct"]
        self.punctuations = None
        if self.remove_punctuations:
            self.punctuations = punctuations
        if self.remove_stopwords:
            self.stopwords = get_stop_words(self.component_config['language'])
        self.ngram = self.component_config['ngram']

    def fit(self, training_data, target):
        return self

    def transform(self, texts, **kwargs):
        return self.texts_to_sequences(texts)

    def tokenize(self, text):
        return self.texts_to_sequences([text])

    def process(self, document, **kwargs):
        if hasattr(document, '_sentences'):
            document.tokens = []
            for sentence in document.sentences:
                document.tokens.append(self.texts_to_sequences(sentence))
            document.sentences = None
        else:
            document.tokens = self.texts_to_sequences([document.text])[0]
            document.raw_text = None

    def get_info(self):
        return "char_tokenizer"

    def texts_to_sequences(self, texts):
        """Transforms each text in texts to a sequence of integers.
        Only top `num_words-1` most frequent words will be taken into account.
        Only words known by the tokenizer will be taken into account.
        # Arguments
            texts: A list of texts (strings).
        # Returns
            A list of sequences.
        """

        return list(self.texts_to_sequences_generator(texts))

    def texts_to_sequences_generator(self, texts):
        """Transforms each text in `texts` to a sequence of integers.
        Each item in texts can also be a list,
        in which case we assume each item of that list to be a token.
        Only top `num_words-1` most frequent words will be taken into account.
        Only words known by the tokenizer will be taken into account.
        # Arguments
            texts: A list of texts (strings).
        # Yields
            Yields individual sequences.
        """

        for text in texts:
            if self.remove_stopwords:
                text = text_to_word_sequence(text, filters=self.punctuations)
                text = ' '.join([t for t in text if t not in self.stopwords])
            elif self.remove_punctuations:
                text = remove_punctuations(text, filters=self.punctuations)

            if self.lower:
                text = text.lower()
            yield ngram(text, self.ngram)

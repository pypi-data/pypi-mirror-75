from strsimpy.levenshtein import Levenshtein
from strsimpy.normalized_levenshtein import NormalizedLevenshtein

from kolibri.similarity.distance import Distance

levenshtein = Levenshtein()
normalised_levenshtein = NormalizedLevenshtein()


class LevenshteinDistance(Distance):

    def __init__(self, normalize=True):
        self.normalize = normalize

    def compare(self, string1, string2):
        if self.normalize:
            return normalised_levenshtein.distance(string1, string2)
        return levenshtein.distance(string1, string2)

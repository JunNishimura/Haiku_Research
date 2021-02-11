import itertools
import collections

class CoOccurrenceAnalyzer(object):
    def __init__(self):
        self.cmb_cnt = []

    def analyze(self, sentences, sep):
        words_list = [ sentence.split(sep) for sentence in sentences]
        word_cmbs = [list(itertools.combinations(words, 2)) for words in words_list]
        word_cmbs = [[tuple(sorted(cmb)) for cmb in cmbs] for cmbs in word_cmbs]
        cmb_list = []
        for cmbs in word_cmbs:
            cmb_list.extend(cmbs)
        self.cmb_cnt = collections.Counter(cmb_list)

    def get_cooccurrence_words(self, word):
        
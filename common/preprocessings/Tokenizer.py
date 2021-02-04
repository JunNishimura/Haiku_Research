import MeCab
import unidic
from collections import namedtuple

class MeCabTokenizer(object):
    def __init__(self, dic_path=''):
        option = ''
        if dic_path:
            option += '-d {}'.format(dic_path)
        self.tagger = MeCab.Tagger(option)

    def wakati(self, text):
        words = [token.surface for token in self.tokenize(text)]
        return words 
    
    def tokenize(self, text):
        node = self.tagger.parseToNode(text)
        token = namedtuple('Token', 'surface pos pos_detail lemma base')

        while node:
            features = node.feature.split(',')
            
            if features[0] != u'BOS/EOS': # skip BOS/EOS written in the first line
                pos = features[0]
                pos_detail = features[1]
                lemma = node.surface if len(features) <= 7 else features[7]
                base = node.surface if len(features) <= 12 else features[12]
                yield token(node.surface, 
                            pos, 
                            pos_detail, 
                            lemma,
                            base)
            node = node.next
    
    def filter_by_pos(self, text, pos=('名詞', )):
        filtered_words = [token for token in self.tokenize(text) if token.pos in pos]
        return filtered_words
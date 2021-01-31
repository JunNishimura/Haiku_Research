import MeCab
import unidic
from collections import namedtuple

class MeCabTokenizer(object):
    def __init__(self, dic_path=''):
        option = ''
        if dic_path:
            option += '-d {}'.format(dic_path)
        self.tagger = MeCab.Tagger(option)

    def wakachi(self, text):
        words = [token.surface for token in self.tokenize(text)]
        return words 
    
    def tokenize(self, text):
        node = self.tagger.parseToNode(text)
        token = namedtuple('Token', 'surface pos pos_detail base')

        while node:
            features = node.feature.split(',')
            
            if features[0] != u'BOS/EOS': # skip BOS/EOS written in the first line
                pos = features[0]
                pos_detail = features[1]
                base = node.surface if len(features) <= 7 else features[7]
                yield token(node.surface, 
                            pos, 
                            pos_detail, 
                            base)
            node = node.next
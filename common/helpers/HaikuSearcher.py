import pandas as pd

class HaikuSearcher(object):
    def __init__(self, df):
        self.df = df

    # isinのリスト版
    def list_isin(_list, _source):
        # もし_sourceが文字列ならリストに変換
        if type(_source) is str:
            _source = _source.split()
        for item in _list:
            if item in _source:
                return True
        return False

    # 単語から俳句を検索
    def search(self, words, pos):
        result = self.df[self.df[pos].apply(lambda x: x.split()).apply(lambda x: self.list_isin(x, words))]
        return result['俳句']
        
    # 名詞から俳句を検索
    def search_from_noun(self, nouns):
        self.search(nouns, pos='名詞')
        
    # 動詞から俳句を検索
    def search_from_verb(self, verbs):
        self.search(verbs, pos='動詞')
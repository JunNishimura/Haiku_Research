import sys, os
sys.path.append(os.pardir)
import matplotlib.pyplot as plt
import MeCab
from common.utils import *
from haiku_tokenizer import Haiku_parser

haijin_name = {
    'basyo': '松尾芭蕉',
    'kikaku': '宝井其角',
    'ransetu': '服部嵐雪',
    'kyorai': '向井去来',
    'jousou': '内藤丈草',
    'kyoroku': '森川許六',
    'sanpuu': '杉山杉風',
    'sikou': '各務支考',
    'hokusi': '立花北枝',
    'yaba': '志太野坡',
    'etujin': '越智越人',
    'sora': '河合曾良',
    'izen': '広瀬惟然', 
    'dohou': '服部土芳',
}

haijin_list = {
    'basyo',
    'kikaku',
    'ransetu',
    'kyorai',
    'jousou',
    'kyoroku',
    'sanpuu',
    'sikou',
    'hokusi',
    'yaba',
    'etujin',
    'sora',
    'izen', 
    'dohou',
}
border = 10 # 再頻出ワード top10を比較する

def draw_word_count(mTagger):
    # map settings 
    plt.rcParams["font.family"] = "IPAexGothic"
    n_rows = 3
    n_cols = 5
    fig, ax = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(12, 8))
    fig.suptitle('俳人 単語ランキング', size=23)
    fig.subplots_adjust(wspace=0.4, hspace=0.6)
    ax[-1, -1].axis('off')
    
    # loop haijin list
    for idx, haijin in enumerate(haijin_list):
        path = "../data/{}.csv".format(haijin)
        haiku_list = csv_haiku_extract(path, 1)
        morpho_list = get_list_morphoAna(m, haiku_list)
        nouns = extract_words_lexicalCategory(morpho_list, '名詞')
        
        # print out result
        top10_dict = {}
        print('----- {} -----\n'.format(haijin_name[haijin]))
        for i, (k, v) in enumerate(get_wordCount_dict(nouns).items()):
            if i > border:
                break
            top10_dict.setdefault(k, v)
            print(k, v)

        # draw a map 
        ax[idx//n_cols, idx%n_cols].bar(top10_dict.keys(), top10_dict.values())
        ax[idx//n_cols, idx%n_cols].set(title=haijin_name[haijin])
    plt.show()

if __name__ == "__main__":
    m = MeCab.Tagger ("-Ochasen")

    for idx, haijin in enumerate(haijin_list):
        if idx == 1:
            break
        path = "../data/{}.csv".format(haijin)
        haiku_list = csv_haiku_extract(path, 1)
        morphemes = morphological_analyzer(m, haiku_list)
        lexical_categories = extract_lexicalCategory(morphemes)
        for lex_cat in lexical_categories:
            print(lex_cat, extract_words_lexicalCategory(lex_cat, morphemes))
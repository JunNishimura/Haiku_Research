import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from wordcloud import WordCloud

# 単語集合から「哉」を取り除く関数
def kireji_remove(x):
    words = []
    for word in x.split(' '):
        if word != '哉':
            words.append(word)
    return ' '.join(words)

def main():
    haijin = ['松尾芭蕉', '与謝蕪村', '小林一茶', '正岡子規', '夏目漱石']
    df = pd.read_pickle('../../data/pickles/pos_df.pickle')
    selected_df = df[df.index.isin(haijin)].copy()

    # 上記関数を適用
    selected_df['名詞'] = selected_df['名詞'].map(kireji_remove)

    wordcloud = WordCloud(background_color="white", width=900, height=600)
    wordcloud.generate(selected_df.loc['松尾芭蕉', '名詞'])
    plt.imshow(wordcloud)
    plt.show()

if __name__=='__main__':
    main()
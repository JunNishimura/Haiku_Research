import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
import re
from common.utils import *

def remove_bracket(txt):
    '''
    remove （）bracket from the passed text
    '''
    return re.sub("（.*）", "", txt)

def kigo_scrape(season, url, save2txt=False):
    kigo_list = []

    try:
        source = requests.get(url)
        soup   = BeautifulSoup(source.content, 'html.parser')
        align_left = soup.find_all("td", {"class": "font1", "align": "left"})
        for i, line in enumerate(align_left):
            a_tag = line.find("a")
            if a_tag is not None:
                # 季語の追加
                kigo_list.append(remove_bracket(a_tag.get_text()+"\n"))
            if i % 4 == 3:
                # 傍題を季語リストに追加
                boudai = line.get_text().replace('\xa0', '\n')
                if boudai != '\n':
                    if '・' in boudai:
                        # 傍題が複数の場合（・で区切られている場合）
                        boudai = boudai.replace('\n', '')
                        kigo_list += [ remove_bracket(b+'\n') for b in boudai.split('・')]
                    elif '、' in boudai:
                        # 傍題が複数の場合（、で区切られている場合）
                        boudai = boudai.replace('\n', '')
                        kigo_list += [ remove_bracket(b+'\n') for b in boudai.split('、')]
                    else:
                        # 傍題が一つの場合
                        kigo_list.append(remove_bracket(boudai))
        print("success to scrape {} kigo".format(season))
    except Exception as e:
        print(season, e)

    if save2txt:
        with open("../../data/Kigo/kigo_{}.txt".format(season), "w", encoding='utf-8') as f:
            f.writelines(kigo_list)

import MeCab
if __name__ == '__main__':
    kigo_dict = {
        'spring' : "http://www.haiku-data.jp/kigo_list.php?season_cd=1#result",
        'summer' : "http://www.haiku-data.jp/kigo_list.php?season_cd=2#result",
        'fall'   : "http://www.haiku-data.jp/kigo_list.php?season_cd=3#result",
        'winter' : "http://www.haiku-data.jp/kigo_list.php?season_cd=4#result",
        'newyear': "http://www.haiku-data.jp/kigo_list.php?season_cd=5#result",
    }

    for season, url in kigo_dict.items():
        kigo_scrape(season, url, save2txt=True)
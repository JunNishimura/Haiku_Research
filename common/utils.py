import MeCab
import requests
from bs4 import BeautifulSoup
from collections import Counter

def csv_haiku_extract(csv_path, col):
    '''
    function to return extract column from the csv
    '''
    h_list = []
    with open(csv_path) as f:
        lines = f.readlines() 
        for line in lines:
            h_list.append(line.split(',')[col])
        del h_list[0] # 先頭行は列名なので消す

    return h_list

def extract_surface(m_tagger, text):
    '''
    function to extract surface from text
    '''
    surfaces = []
    for t in text:
        node = m_tagger.parseToNode(t)
        while node:
            if node.feature.split(',')[0] != u'BOS/EOS':
                surfaces.append(node.surface)
            node = node.next

    return surfaces

def morphological_analyzer(m_tagger, text):
    '''
    execute morphological analysis and return surface, base, word class1, word class2
    '''
    morphemes = []
    node = m_tagger.parseToNode(text)
    while node:
        nf_split = node.feature.split(',')
        if nf_split[0] != u'BOS/EOS':
            d = {
                'surface': node.surface,
                'base'   : nf_split[6],
                'pos'    : nf_split[0],
                'pos1'   : nf_split[1],
            }
            morphemes.append(d)
        node = node.next

    return morphemes

def get_wordCount_dict(words_list, descending=True):
    """
    create and return a dictionary which has words as key and word counts as values.
    """
    wc = Counter(words_list)
    return dict(sorted(wc.items(), key=lambda x: x[1], reverse=descending))

def extract_lexicalCategory(morphemes):
    '''extract lexical category from morpheme list'''
    lexical_category = set()
    for morpheme in morphemes:
        lexical_category.add(morpheme['pos'])
    
    return list(lexical_category)

def extract_words_lexicalCategory(category, morphemes):
    '''
    extract words from the list based on the lexical category (word class)
    '''
    words = []
    for morpheme in morphemes:
        if morpheme['pos'] == category:
            words.append(morpheme['surface'])
    
    return words

def haiku_urls(haijin, is_categorized):
    '''
    Return haiku urls of given haijin

    Parameter
    ----------------------
    haijin: 俳人
    is_categorized: 分類されているか否か
    '''
    # put all urls into the list
    URL_BASE = 'http://www5c.biglobe.ne.jp/~n32e131/haiku/'
    URL      = URL_BASE + str(haijin) + '.html'
    URL_list = [URL]

    if is_categorized:
        category_id = 0

        while True:
            category_id += 1
            page_id = 1
            url = URL_BASE + '{}{}{}.html'.format(str(haijin), str(category_id), str(page_id).zfill(2))
            r = requests.get(url)
            if r.status_code != requests.codes.ok:
                break
            URL_list.append(url)

            while True:
                page_id += 1
                url = URL_BASE + '{}{}{}.html'.format(str(haijin), str(category_id), str(page_id).zfill(2))
                r = requests.get(url)
                if r.status_code != requests.codes.ok:
                    break 
                URL_list.append(url)
    else:   
        page_id = 0
        while True:
            page_id += 1
            url = URL_BASE + str(haijin) + str(page_id).zfill(2) + '.html'
            r = requests.get(url)
            if r.status_code != requests.codes.ok:
                break 
            URL_list.append(url)

    return URL_list

def haiku_scraper(haijin, url_list, save2txt=False):
    '''
    Scraping designated haijin's haiku from http://www5c.biglobe.ne.jp/~n32e131/haiku/index.html
    
    Parameter
    ----------------------
    url_list: urlリスト
    '''
    haiku_list = []
    
    # scrape haiku from the given urls 
    try:
        for url in url_list:
            source = requests.get(url)
            soup   = BeautifulSoup(source.content, 'html.parser')
            p_tags = soup.find(class_='naka').find_all('p')
            for p_tag in p_tags:
                haiku_list.append(p_tag.text+'\n')
        print("success to scrape {}'s haiku".format(haijin))
    except Exception as e:
        print(haijin, e)

    if save2txt:
        with open('../../data/' + str(haijin) + '_raw.txt', 'w', encoding='utf-8') as f:
            f.writelines(haiku_list)
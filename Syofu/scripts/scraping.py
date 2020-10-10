from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import re


def basyo_scraping(save2txt=False):
    '''
    Scraping Basyo's haiku from http://www2.yamanashi-ken.ac.jp/~itoyo/basho/haikusyu/Default.htm
    '''
    basyo_haiku_list = []

    url = 'http://www2.yamanashi-ken.ac.jp/~itoyo/basho/haikusyu/Default.htm'
    source = requests.get(url)
    soup   = BeautifulSoup(source.content, 'html.parser')

    a_tags = soup.find_all('a')
    for a in a_tags:
        if len(a.text) > 5: #5文字以下の俳句以外の文字列が混ざっていることを確認した
            basyo_haiku_list.append(a.text+'\n') 

    if save2txt:
        with open('test.txt', 'w', encoding='utf-8') as f:
            f.writelines(basyo_haiku_list)

    
if __name__ == '__main__':
    haijin_dict = {
        'kikaku': 9,
        'ransetu': 6,
        'kyorai': 4,
        'jousou': 3,
        'kyoroku': 5,
        'sanpuu': 4,
        'sikou': 4,
        'hokusi': 3,
        'yaba': 3,
        'etujin': 2,
        'sora': 2,
        'izen': 2, 
        'dohou': 2,
    }

    for k, v in haijin_dict.items():
        haiku_scraper(k, v, save2txt=True)
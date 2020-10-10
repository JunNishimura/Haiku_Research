import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from common.utils import *

if __name__ == '__main__':
    haijins = [
        'bashou',
        'buson',
        'issa',
        'siki',
        'souseki',
        'ryunosuke',
        'kyoshi',
        'housai',
        'hekigotoh',
        'hisajo',
    ]
    
    for haijin in haijins:
        if haijin == 'housai':
            is_cat = False
        else:
            is_cat = True
        url_list = haiku_urls(haijin, is_categorized=is_cat)
        haiku_scraper(haijin, url_list, save2txt=True)
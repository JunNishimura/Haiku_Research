import sys, os
sys.path.append(os.pardir)
from common.utils import *
import MeCab 

def Haiku_parser(mTagger, sentence):
    node = mTagger.parseToNode(sentence)
    token_dict = {}
    while node:
        node_split = node.feature.split(',')
        if node_split[0] != u'BOS/EOS' and (len(node_split) >= 8):
            token_dict.setdefault(node.surface, node_split[7])
        node = node.next
    moji_list = list(token_dict.keys())
    yomi_list = list(token_dict.values())
    # 文字リストと音読みリストの長さが異なる場合はreturn
    if len(moji_list) != len(yomi_list):
        return 

    # 17音でない場合はreturn
    oto = sum([len(yomi) for yomi in yomi_list])
    if oto != 17:
        return 
    idx = 0
    oto = 0
    kami_no_ku = ''
    while idx < len(yomi_list):
        oto += len(yomi_list[idx])
        kami_no_ku += moji_list[idx]
        idx += 1
        if oto == 5:
            break 
        if oto > 5:
            return
        
    naka_no_ku = ''
    oto = 0
    while idx < len(yomi_list):
        oto += len(yomi_list[idx])
        naka_no_ku += moji_list[idx]
        idx += 1
        if oto == 7:
            break 
        if oto > 7:
            return 

    shimo_no_ku = ''
    oto = 0
    while idx < len(yomi_list):
        oto += len(yomi_list[idx])
        shimo_no_ku += moji_list[idx]
        idx += 1
        if oto == 5:
            break 
        if oto > 5:
            return 

    return (kami_no_ku, naka_no_ku, shimo_no_ku)
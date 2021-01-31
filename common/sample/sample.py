import MeCab

def main():
    tagger = MeCab.Tagger("-d ../../dic/UniDic-wabun_1603")
    print(tagger.parse("花の顔に晴うてしてや朧月"))

if __name__=="__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'lbbxsxlz'

import threading
import time
#加载HanLP
from jpype import *

'''
CONLL标注格式包含10列，分别为：
   ———————————————————————————
   ID	FORM	LEMMA	CPOSTAG	POSTAG	FEATS	HEAD	DEPREL	PHEAD	PDEPREL
———————————————————————————
   本次评测只用到前８列，其含义分别为：
   1	ID	当前词在句子中的序号，１开始.
   2	FORM	当前词语或标点
   3	LEMMA	当前词语（或标点）的原型或词干，在中文中，此列与FORM相同
   4	CPOSTAG	当前词语的词性（粗粒度）
   5	POSTAG	当前词语的词性（细粒度）
   6	FEATS	句法特征，在本次评测中，此列未被使用，全部以下划线代替。
   7	HEAD	当前词语的中心词
   8	DEPREL	当前词语与中心词的依存关系
   在CONLL格式中，每个词语占一行，无值列用下划线'_'代替，列的分隔符为制表符'\t'，行的分隔符为换行符'\n'；句子与句子之间用空行分隔。
'''

'''
#依存标签
HED = "核心关系"
SBV = "主谓关系"
VOB = "动宾关系"
IOB = "间宾关系"
FOB = "前置宾语"
DBL = "兼语"
ATT = "定中关系"
ADV = "状中结构"
CMP = "动补结构"
COO = "并列关系"
POB = "介宾关系"
LAD = "左附加关系"
RAD = "右附加关系"
IS = "独立结构"
WP = "标点符号"
'''

startJVM(getDefaultJVMPath(), "-Djava.class.path=D:\workspace\HanLP\hanlp-1.2.8-release\hanlp-1.2.8.jar;D:\workspace\HanLP\hanlp-1.2.8-release")
HanLP = JClass('com.hankcs.hanlp.HanLP')
#语法依存分析
DependencyParser = JClass('com.hankcs.hanlp.dependency.nnparser.NeuralNetworkDependencyParser')
#CoNLLWord = JClass('com.hankcs.hanlp.corpus.dependency.CoNll.CoNLLWord')
#CoNLLSentence = JClass('com.hankcs.hanlp.corpus.dependency.CoNll.CoNLLSentence')
#分词，包含在HanLP.segment中
#NLPTokenizer = JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')
Suggester = JClass('com.hankcs.hanlp.suggest.Suggester')

# 依存句法分析
def parser_deal(string):
    print("--------依存句法分析-------- ")
    print("HanLP依存句法分析 ")
    #依存标签中文标识
    #csentence = HanLP.parseDependency(str)
    #t0 = time.clock()
    #依存标签英文标识
    Parser = DependencyParser().enableDeprelTranslator(False)
    #print("init take time %s" %(time.clock() - t0))
    csentence = Parser.parse(string)
    print(csentence)
    global wordArray
    wordArray = csentence.getWordArray()
    for cword in wordArray:
        print('%s -- %s -- %s' %(cword.LEMMA, cword.DEPREL, cword.HEAD.LEMMA))

# 创建文本推荐对象
def sentence_suggester():
    global suggester
    suggester = Suggester()
    file = open("qa.txt", "rb")
    print("==========文本内容========")
    for line in file:
        #print(line)
        sentence = line.decode('utf-8')
        print(sentence,end = "")
        suggester.addSentence(sentence)
    file.close()
    print("\n")

# 依存句法分析，首次调用耗时较久，
# 之后调用就不再耗时，目前原因未知
# 估计与Java类型转换到python类型有关系
parser_deal("依存句法分析")
#sentence_suggester()

n = 1
while(n > 0):
    str = input("please input a sentence or input quit to exit \n")
    #str = "世界上最高的山峰是哪座山？"
    if str == "quit":
        break
    #elif str == "":
    elif len(str) < 1:
        print(len(str))
        continue
    print(40*"=")
    print("HanLP分词与词性标注 ")
    print(HanLP.segment(str))
    #str_list = HanLP.segment(str)
    #for a in str_list:
    #    print(a)
    #print(NLPTokenizer.segment(str))
    #创建线程
    #td = threading.Thread(target=parser_deal(str))
    #td.start()
    #td.join()
    t1 = time.clock()
    parser_deal(str)
    print("parser_deal take time %s" %(time.clock() - t1))
    print("--------关键词抽取--------")
    print("HanLP关键词抽取 ")
    keywords = HanLP.extractKeyword(str, 4)
    print(keywords)
    if len(keywords) < 1:
        print("无法提取到关键字")
        continue
    print("HanLP短语抽取 ")
    phrase = HanLP.extractPhrase(str, 2)
    print(phrase)
    if len(phrase) >= 1:
        key = phrase[0]
    elif len(phrase) < 1 and len(keywords) >= 1:
        key = keywords[0]
    print(key)
    for word in wordArray:
        if(word.DEPREL == "SBV"):
            key_word = word.LEMMA
            print(key_word)
            for s_word in wordArray:
                if (s_word.DEPREL == "ATT" and s_word.HEAD.LEMMA == key_word):
                    key_word_2 = s_word.LEMMA
                    print(key_word_2)
                    KEY = key_word_2 + key_word
                    print(KEY)
                    break
            break
    #print("========根据关键字找类似的句子========")
    #print(suggester.suggest(key,1))
shutdownJVM()
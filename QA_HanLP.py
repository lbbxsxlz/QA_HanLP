#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'lbbxsxlz'

import threading
#加载HanLP
from jpype import *
startJVM(getDefaultJVMPath(), "-Djava.class.path=D:\workspace\HanLP\hanlp-1.2.8-release\hanlp-1.2.8.jar;D:\workspace\HanLP\hanlp-1.2.8-release")
HanLP = JClass('com.hankcs.hanlp.HanLP')
#语法依存分析
#CoNLLWord = JClass('com.hankcs.hanlp.corpus.dependency.CoNll.CoNLLWord')
#CoNLLSentence = JClass('com.hankcs.hanlp.corpus.dependency.CoNll.CoNLLSentence')
#cword = CoNLLWord(-1, "##空白##", "NULL", "null")
#csentence = CoNLLSentence(None)
#NLPTokenizer = JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')
Suggester = JClass('com.hankcs.hanlp.suggest.Suggester')

def parser_deal(str):
    print("--------依存句法分析-------- ")
    print("HanLP依存句法分析 ")
    csentence = HanLP.parseDependency(str)
    #print(csentence)
    wordArray = csentence.getWordArray();
    for cword in wordArray:
        print('%s -- %s -- %s' %(cword.LEMMA, cword.DEPREL, cword.HEAD.LEMMA))

#创建文本推荐对象
suggester = Suggester()
file = open("lbb_test.txt", "rb")
print("==========文本内容========")
for line in file:
    #print(line)
    sentence = line.decode('utf-8')
    print(sentence,end = "")
    suggester.addSentence(sentence)
file.close()
print("\n")

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
    td = threading.Thread(target=parser_deal(str))
    td.start()
    #td.join()
    print("--------关键词抽取--------")
    print("HanLP关键词抽取 ")
    keywords = HanLP.extractKeyword(str, 4)
    print(keywords)
    if len(keywords) < 1:
        print("无法提取到关键字")
        continue
    print("HanLP短语抽取 ")
    phrase = HanLP.extractPhrase(str, 4)
    print(phrase)
    if len(phrase) >= 1:
        key = phrase[0]
    elif len(phrase) < 1 and len(keywords) >= 1:
        key = keywords[0]
    print(key)
    print("========根据关键字找类似的句子========")
    print(suggester.suggest(key,1))
    #n = 0
shutdownJVM()
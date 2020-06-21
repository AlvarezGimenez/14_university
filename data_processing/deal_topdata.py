'''
@author: Hongwentao
本文件处理新闻数据，并且最后提取词云的关键词，便于后面词云图的生成
'''
import csv
import os
import numpy as np
import pandas as pd
import jieba
import jieba.analyse
from wordcloud import WordCloud
from top import all_top
import matplotlib.pyplot as plt
import Levenshtein

data_path="../data/top_data/"
filter_path="../data_processing/"

def get_top_word():
    '''
                该函数用于获取各个学校的新闻信息，通过提取这些语句中的所有语句，提取高频词
                返回一个字典格式的结果，例子如下：
    
    '''
    final_result={}
    school_name=os.listdir(data_path)
    get_word=[]
    for name in school_name:
        final_path=data_path+name+"/final_"+name+".csv"
        file=open(final_path,encoding="utf-8")
        a=pd.read_csv(file,sep=',',header=None,usecols=[0,]);
        b=np.array(a)
        c=b.tolist()
        for x in c:  
            words=jieba.analyse.extract_tags(x[0], topK=20,allowPOS=('n','nt','nz','nl','ng'))
            get_word=get_word+words
    final_word=[]
    for word in get_word:
        if not filter(word):
            final_word.append(word)
    for word in final_word:    
        if word not in final_result.keys():
            final_result[word]=1;
        else:
            final_result[word]=final_result[word]+1
    have_sort=sorted(final_result.items(), key=lambda x: x[1],reverse = True)
    final_sort_result=dict(have_sort)
    return final_sort_result      

def add_filter_file(word):
    '''
                添加过滤的词语，如想在过滤中过滤掉一个词语，可以输入该词语。
    '''
    with open(filter_path+'filter.txt','a') as r:
        r.write(word+"\n")
    
def delete_filter_file(word):
    '''
                删除过滤的词语，如想在过滤中不需要过滤掉一个词语，可以输入该词语，将其从filter.txt中删除。
    '''
    with open(filter_path+'filter.txt','r') as r:
        lines=r.readlines()
    with open(filter_path+'filter.txt','w') as w:
        for l in lines:
            if word not in l:
                w.write(l) 

def filter(word):
    '''
                用于过滤掉不需要的词语
    '''
    with open(filter_path+'filter.txt','r') as r:
        lines=r.readlines()
        for line in lines:
            if word in line:
                return True           
def main():
    #add_filter_file(word)
    get_top_word()
if __name__=='__main__':
    main();        
    
'''
@author: Hong wentao
@attention: 该文件是用于爬取软科最好学科排名,以及提取其中14所学校相关学科排名的数据
'''
import urllib.request
import requests
from bs4 import BeautifulSoup
import re
import csv
from xpinyin import Pinyin
import os
import time
from selenium import webdriver
import pandas as pd
import numpy as np
path='../data/subject_data/ruanke_best_subject/'
university_name=["河北大学","山西大学","内蒙古大学","南昌大学","郑州大学","广西大学","海南大学","贵州大学","云南大学","西藏大学","青海大学","宁夏大学","新疆大学","石河子大学"]

field_name=["哲学", "经济学", "法学", "教育学", "文学", "历史学", "理学", "工学",
            "农学", "医学", "管理学", "艺术学" ]
subject_name=[
            [ "哲学" ],
            [ "理论经济学", "应用经济学" ],
            [ "法学", "政治学", "社会学", "民族学", "马克思主义理论" ],
            [ "教育学", "心理学", "体育学" ],
            [ "中国语言文学", "外国语言文学", "新闻传播学" ],
            [ "考古学", "中国史", "世界史" ],
            [ "数学", "物理学", "化学", "天文学", "地理学", "大气科学", "海洋科学", "地球物理学", "地质学",
                    "生物学", "生态学", "统计学" ],
            [ "力学", "机械工程","仪器科学与技术", "材料科学与工程", "冶金工程", "动力工程及工程热物理",
                    "电气工程", "电子科学与技术", "信息与通信工程", "控制科学与工程", "计算机科学与技术", "建筑学",
                    "土木工程", "水利工程", "测绘科学与技术", "化学工程与技术", "地质资源与地质工程", "矿业工程",
                    "石油与天然气工程", "纺织科学与工程", "轻工技术与工程", "交通运输工程", "船舶与海洋工程",
                    "航空宇航科学与技术", "核科学与技术", "农业工程","林业工程", "环境科学与工程", "生物医学工程",
                    "食品科学与工程", "城乡规划学", "软件工程", "安全科学与工程","网络空间安全" ],
            [ "作物学", "园艺学", "农业资源与环境", "植物保护", "畜牧学", "兽医学", "林学", "水产", "草学" ],
            [ "基础医学", "临床医学", "口腔医学", "公共卫生与预防医学", "中医学", "中西医结合", "药学", "中药学",
                    "特种医学", "护理学" ],
            [ "管理科学与工程", "工商管理", "农林经济管理", "公共管理", "图书情报与档案管理" ],
            [ "艺术学理论", "音乐与舞蹈学", "戏剧与影视学", "美术学", "设计学" ]
            ]
subject_dic={}

def group(field_name,subject_name):
    '''
                将学科名和学科门类组合起来，放到一个字典里
    '''
    final_result={}
    for i in range(0,len(field_name)):
         final_result[field_name[i]]=subject_name[i]
    return final_result

def to_pinyin(word):
    '''
                将汉字转为拼音字母,下面的replace作用将拼音字符串之间的‘-’消除
    '''
    pin = Pinyin()
    result = pin.get_pinyin(word)
    final=result.replace('-','') 
    return final
    
def mkdir(subject_dic):
    '''
                创建各学科门类以及学科名的文件夹
    '''
    field_name=(list)(subject_dic)
    for name in field_name:
        for x in subject_dic[name]:
            field_path=path+name+'/'+x
            isExists=os.path.exists(field_path)
            # 判断结果
            if not isExists:
                # 如果不存在则创建目录
                # 创建目录操作函数
                os.makedirs(field_path)

'''
以下部分为webdriver爬虫部分
'''

def search(url):
    #利用get()方法获取网页信息并返回
    return driver.get(url)

def parse_one_page(page):
    #查找出玩野中全部的 tr 标签并赋给 tr_list
    table=driver.find_elements_by_tag_name('table')
    tr_list =table[0].find_elements_by_tag_name('tr')
    return tr_list   

def get_all_html(subject_dic):
    '''
                爬取所有学科的排名数据
    '''
    global driver
    driver = webdriver.Chrome()
    base_html="http://www.zuihaodaxue.com/BCSR/"
    rear_html=".html"
    for name in field_name:
        for subject in subject_dic[name]:
            for year in range(2017,2019):
                try:
                    print(subject)
                    final_path=path+name+'/'+subject+'/'+subject+"_"+str(year)+".csv"
                    isExists=os.path.exists(final_path)
                    if not isExists:
                        final_html=base_html+to_pinyin(subject)+str(year)+rear_html
                        if subject=="音乐与舞蹈学":
                            final_html=base_html+"yinyueyuwudaoxue"+str(year)+rear_html
                        html=search(final_html)
                        tr_list = parse_one_page(html)
                        with open(final_path,"a+",encoding="utf-8") as csvfile:
                            writer = csv.writer(csvfile,lineterminator='\n')
                            row=[]
                            th_list =tr_list[0].find_elements_by_tag_name('th')
                            for i in th_list:
                                row.append(i.text)
                            writer.writerow(row)
                            for i in range(1, len(tr_list)-1):
                                #找出 tr_list 中的全部 td 标签
                                td_list =tr_list[i].find_elements_by_tag_name('td')
                                data_list=[]
                                for x in td_list:
                                    data_list.append(x.text)
                                writer.writerow(data_list)
                except Exception as e:
                    print(subject+"有问题")
                    print(e)
    print("end")
    driver.close()

def get_14_data(subject_dic):
    '''
                提取我们所需14所学校的数据
    '''
    for name in field_name:
        for subject in subject_dic[name]:
            for year in range(2017,2019):
                final_path=path+name+'/'+subject+'/'+subject+"_"+str(year)+".csv"
                isExists=os.path.exists(final_path)
                if isExists:
                    file=open(final_path,encoding="utf-8")
                    a=pd.read_csv(file,sep=',',skip_blank_lines=False);
                    b=np.array(a)
                    c=b.tolist()
                    create_path=final_path=path+name+'/'+subject+'/'+"final_"+subject+"_"+str(year)+".csv"
                    isExists=os.path.exists(create_path)
                    if not isExists:
                        with open(create_path,"a+",encoding="utf-8") as csvfile:
                            writer = csv.writer(csvfile,lineterminator='\n')
                            if year==2017:
                                row=["排名","百分位段","院校名称","博士点","重点学科","总分"]
                                writer.writerow(row)
                                for every in c:
                                    if every[2] in university_name:
                                        writer.writerow(every)
                            else:
                                row=[str(year)+"排名",str(year-1)+"排名","百分位段","院校名称","博士点","重点学科","总分"]
                                writer.writerow(row)
                                for every in c:
                                    if every[3] in university_name:
                                        writer.writerow(every)
                else:
                    print(subject+'_'+str(year)+"不存在")
    

def main():
    subject_dic=group(field_name,subject_name)#将相应学科和学科门类组成字典
    #mkdir(subject_dic)#创建相应文件夹
    #get_all_html(subject_dic)#爬取并收集全部学科的排名数据
    get_14_data(subject_dic)
    
if __name__=='__main__':
    main();
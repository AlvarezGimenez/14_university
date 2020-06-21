'''
@author: Hong wentao
@attention: 该文件是用于爬取各学校热门信息,并进行初步过滤
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
import Levenshtein
import matplotlib.pyplot as plt
import pymysql
import traceback

data_path='../data/top_data/'
university_name=["河北大学","山西大学","内蒙古大学","南昌大学","郑州大学","广西大学","海南大学","贵州大学","云南大学","西藏大学","青海大学","宁夏大学","新疆大学","石河子大学"]               
#abbr_name 简称
abbr_name={"河北大学":["河北大","河大"],"山西大学":["山大"],"内蒙古大学":["内大"],"南昌大学":["南大","昌大"],"郑州大学":["郑大"],"广西大学":["西大"],"海南大学":["海大"],"贵州大学":["贵大"],"云南大学":["云大"],"西藏大学":["藏大"],"青海大学":["青大"],"宁夏大学":["宁大"],"新疆大学":["新大"],"石河子大学":["石大"]}#简写

#https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=郑州大学+-baijiahao&x_bfe_rqs=03E80&x_bfe_tjscore=0.010740&tngroupname=organic_news&pn=50
final_point=[]
def mkdir():
        for name in university_name:
            final_path=data_path+name
            isExists=os.path.exists(final_path)
            # 判断结果
            if not isExists:
                # 如果不存在则创建目录
                # 创建目录操作函数
                os.makedirs(final_path)
'''
webdriver爬虫爬取学校的热点信息,以下部分只包括十四所大学的各自部分，不包括整体
'''
def search(url):
    #利用get()方法获取网页信息并返回
    return driver.get(url)

def parse_one_page(page):
    results=driver.find_elements_by_class_name("result")
    return results  

def get_info(school_name):
    '''
                提取14所大学的最近的相关热点信息，以百度搜索引擎为准，搜索前十页的相关内容，搜索方式的资讯类的按焦点搜索
    '''
    global driver
    driver = webdriver.Chrome()
    front_html="https://www.baidu.com/s?tn=news&rtt=1&bsst=1&cl=2&wd="
    rear_html="+-baijiahao&x_bfe_rqs=03E80&x_bfe_tjscore=0.004088&tngroupname=organic_news&pn="
    final_path=data_path+school_name+"/"+school_name+".csv"
    isExists=os.path.exists(final_path)
    final_result=[]
    if isExists:
        os.remove(final_path)
    for i in range(0,5):
        html=front_html+school_name+rear_html+str(i*10)
        if i==0:
            html="https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&word="+school_name+"%20-baijiahao"
        page=search(html)
        results=parse_one_page(page)
        time.sleep(1)
        data_list=[]
        with open(final_path,"a+",encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile,lineterminator='\n')
            for result in results:
                line=[]
                text=result.find_elements_by_tag_name("a")
                line.append(text[0].text)
                line.append(text[0].get_attribute("href"))
                writer.writerow(line)
                data_list.append(line)
        if len(data_list)==0:
            print(school_name+":"+str(i+1)+"页有问题")
        final_result.append(data_list)                             
    driver.close()
    print("已结束")
    
def filter_same(word,line):
    '''
                过滤掉基本类似的新闻
    '''
    for i in range(0,len(line)):
        result=Levenshtein.ratio(word,line[i])
        if result==1:
            return False
        final_point.append(result)
        '''
        if result>=0.5:
            return False
        '''
    return True

def filter_top_data(school_name,year):
    '''
    #用于过滤过去的和不相关信息
    #school_name:学校名称
    #year:当年年份
    '''
    final_path=data_path+school_name+"/"+school_name+".csv"
    f = open(final_path,"r",encoding='utf-8')   #设置文件对象
    datas =csv.reader(f) 
    new_path=data_path+school_name+"/"+"final_"+school_name+".csv"
    isExists=os.path.exists(new_path)
    if isExists:
        os.remove(new_path)
    final_result=[]
    with open(new_path,"a+",encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile,lineterminator='\n')
            total_title=[]
            for data in datas:
                line=[]
                first=False
                second=False
                href=data[1]
                if str(year) in href:
                    second=True
                abbr_list=(list)(abbr_name[school_name])
                abbr_list.append(school_name)
                for name in abbr_list:
                    if name in data[0]:
                        first=True
                if ((first==True) and (second==True)):
                    if filter_same(data[0], total_title):
                        total_title.append(data[0]) 
                        line.append(data[0])
                        line.append(href)
                        final_result.append(line)
                        writer.writerow(line)   
    print(school_name+"已完成")
    f.close()

def operate_mysql():
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='hong1997JIUjiang', db='new_point', 
                             charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    return connection
def write_mysql(final_point):
    db=operate_mysql()
    cursor=db.cursor()
    for point in final_point:
        sql = "INSERT INTO point (point_value) VALUES ('%f')"%(point)
        try:
            # 执行sql语句  
            cursor.execute(sql)
            # 执行sql语句
            db.commit()
        except Exception as e:
            # 发生错误时回滚
            traceback.print_exc()
            db.rollback()
            print("failed")
            # 关闭数据库连接
    db.close()

    
def read_mysql():
    db=operate_mysql()
    cursor=db.cursor()
    sql = "select point_value from point"
    try:
        # 执行sql语句  
        cursor.execute(sql)
        # 执行sql语句
        db.commit()
        results=cursor.fetchall() 
    except Exception as e:
        # 发生错误时回滚
        traceback.print_exc()
        db.rollback()
        print("failed")
        # 关闭数据库连接
    db.close()
    final_result=[]
    for result in results:
        final_result.append(result["point_value"])
    print(final_result)
    return final_result
    
  
def show_boxplot(data):
    data=np.array(final_point)
    plt.boxplot(data , sym='o' , whis=0.05)
    plt.show()
 
def main():
    #mkdir()
    for name in university_name:
        get_info(name)
        filter_top_data(name,2019)
    write_mysql(final_point)
    data=read_mysql()
    show_boxplot(data)
    print("已结束")
if __name__=='__main__':
    main();    
        
        
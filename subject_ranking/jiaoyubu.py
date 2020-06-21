'''
@author: Hong wentao
@attention: 该文件是用于提取14所学校的学科评级数据。数据来源：教育部第四次学科评估
'''
import urllib.request
import requests
from bs4 import BeautifulSoup
import re
import csv
from matplotlib.pyplot import flag
path="../data"
def readhtml(url):#url转换为html格式
    head={}
    data={}
    head['User-Agent']="Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)"
    req=urllib.request.Request(url,data,head)
    response=urllib.request.urlopen(req)
    html=response.read()
    html=html.decode('utf-8')
    return html
def get(html):
    '''
                统计14所高校参评学科的具体数据
    '''
    soup=BeautifulSoup(html,"html.parser");
    all=soup.find("tbody")
    datas=all.find_all("tr")
    no_deal_data=[]
    for data in datas:
        sentence=data.get_text()
        no_deal_data.append(sentence)
    rule=re.compile(r'\d{4}.')
    all_subject={}
    before_subject_name=[]
    school=[]
    per_school=[]
    for i in range(2,len(no_deal_data)):
        if(re.search(rule,no_deal_data[i])):
            before_subject_name.append(no_deal_data[i])
            school.append(per_school)
            per_school=[]
        else:
            per_school.append(no_deal_data[i])
    school.append(per_school)
    school.pop(0)   
    subject_name=[]
    for name in before_subject_name:
        second=name.split()
        subject_name.append(second[1])
    all_subject=dict(map(lambda x,y:[x,y],subject_name,school))
    university_name=["河北大学","山西大学","内蒙古大学","南昌大学","郑州大学","广西大学","海南大学","贵州大学","云南大学","西藏大学","青海大学","宁夏大学","新疆大学","石河子大学"]
    have_subject={}
    for uni_name in university_name:
        subject_list=[]
        have_subject[uni_name]=subject_list
        flag="."+uni_name
        judge_name=re.compile(flag)
        for name in subject_name:
            for sch_name in all_subject[name]:
                if(re.search(judge_name,sch_name)):
                    l=-(len(uni_name))
                    ranking=sch_name[:l]
                    subject_str=[]
                    subject_str.append(name)
                    subject_str.append(ranking)
                    subject_list.append(subject_str)
    for uni_name in university_name:
        final_name_path=path+"/subject_data/jiaoyubu_xuekepinggu/"+"pinggu_"+uni_name+".csv"
        final_subject=have_subject[uni_name]
        with open(final_name_path,"a+",encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile,lineterminator='\n')   
            for i in final_subject:
                writer.writerow(i)
def main():
    #html=readhtml("http://www.360doc.com/content/18/0705/08/91243_767830851.shtml")#全国第四轮学科评估结果2017
    f=open(r"1.txt",encoding="utf-8")
    html=f.read()
    f.close()
    get(html)
if __name__=='__main__':
    main();
'''
@author: Hong wentao
@attention: 该文件是过滤和提取数据的
'''
import csv
import codecs
import pandas as pd
import numpy as np
path="../data/total_data/ruanke/"
def filter_co_name(filename):
    final_path=path+filename+".csv"
    file=open(final_path,encoding="utf-8")
    a=pd.read_csv(file,sep=',',skip_blank_lines=False);
    a["学校名称"]=a["学校名称"].astype(str)
    a["学校名称"]=a["学校名称"].apply(lambda x :x.split(' ')[-1])
    a.to_csv(final_path,index=False, encoding='utf-8')
def view(filename):
    final_path=path+filename+".csv"
    file=open(final_path,encoding="utf-8")
    a=pd.read_csv(file,sep=',',skip_blank_lines=False);
    print(a)
def get_want_data(year):
    university_name=["河北大学","山西大学","内蒙古大学","南昌大学","郑州大学","广西大学","海南大学","贵州大学","云南大学","西藏大学","青海大学","宁夏大学","新疆大学","石河子大学"]
    final_path=path+year+".csv"
    file=open(final_path,encoding="utf-8")
    a=pd.read_csv(file,sep=',',header=None,skip_blank_lines=False);
    b=np.array(a)
    head=list(b[0])
    head.insert(0,"排名")
    get_data=[]
    get_data.append(head)
    for i in range(1,len(b)):
        if b[i][0] in university_name:
            c=list(b[i])
            c.insert(0,str(i))
            get_data.append(c)
    final_name=path+"final_"+year+".csv"
    with open(final_name,"a+",encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile,lineterminator='\n')
        for i in range(0, len(get_data)):
            writer.writerow(get_data[i])
def main():
   #filter_co_name("2017") 
   #view("2018")
   get_want_data("2016")
if __name__=='__main__':
    main();
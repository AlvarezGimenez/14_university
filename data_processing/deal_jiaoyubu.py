'''
@author: Hongwentao
本文件处理教育部第四次评估的所有的数据，同时提供数据接口，作为图形可视化的数据来源
'''
import csv
import pandas as pd
import numpy as np
data_path="../data/subject_data/jiaoyubu_xuekepinggu/"
university_name=["河北大学","山西大学","内蒙古大学","南昌大学","郑州大学","广西大学","海南大学","贵州大学","云南大学","西藏大学","青海大学","宁夏大学","新疆大学","石河子大学"]
rank=["A+","A","A-","B+","B","B-","C+","C","C-"]
def get_total_jiaoyubu():
    '''
                提取14所学校在教育部第四次学科评估中，参评学科的相关数据
                以字典形式展现，字典无特殊排序
                字典格式：
                学校名：{}
    {}内是以等级排名为字典的学科名，例子如下：
    '河北大学': {'A+': [], 'A': [], 'A-': [], 'B+': [], 'B': ['中国语言文学', '新闻传播学'],。。。'C-'['外国语言文学',。。。'美术学']}
                等级排名的字典内的学科名数据是一个list列表
    '''
    final_result={}
    c=[]
    rank=["A+","A","A-","B+","B","B-","C+","C","C-"]
    for name in university_name:
        final_path=data_path+"pinggu_"+name+'.csv'
        file=open(final_path,encoding="utf-8")
        per={}
        subject=[]
        try:
            a=pd.read_csv(file,sep=',',skip_blank_lines=False);
            b=np.array(a)
            c=b.tolist()
            subject=c
        except Exception:
            print(name+"没有数据")
        finally:
            for every in rank:
                subject_name=[]
                for i in subject:
                    if(i[1]==every):
                        subject_name.append(i[0])
                per[every]=subject_name
            final_result[name]=per           
    return final_result   

'''
下面是几种大类别（A,B,C）具体的分类
比如，一所学校A等级有哪些学科，B等级，C等级各有多少
'''

def A_rank():
    '''
                等级为 A的
                最后返回一个字典，格式如下：
                学校名:[[1][2][3]]
    value中的list里，1，2，3分别代表+，，-三种等级，这三个list中对应着相应学科
    '''
    data=get_total_jiaoyubu()
    final_result={}
    signs=['+','','-']
    for name in university_name:
        new_list=[]
        for sign in signs:
            new_list.append(data[name]['A'+sign])
        final_result[name]=new_list
    return final_result
    
def B_rank():
    '''
                等级为 B的
                最后返回一个字典，格式如下：
                学校名:[[1][2][3]]
    value中的list里，1，2，3分别代表+，，-三种等级，这三个list中对应着相应学科
    '''
    data=get_total_jiaoyubu()
    final_result={}
    signs=['+','','-']
    for name in university_name:
        new_list=[]
        for sign in signs:
            new_list.append(data[name]['B'+sign])
        final_result[name]=new_list
    return final_result

def C_rank():
    '''
                等级为 C的
                最后返回一个字典，格式如下：
                学校名:[[1][2][3]]
    value中的list里，1，2，3分别代表+，，-三种等级，这三个list中对应着相应学科
    '''
    data=get_total_jiaoyubu()
    final_result={}
    signs=['+','','-']
    for name in university_name:
        new_list=[]
        for sign in signs:
            new_list.append(data[name]['C'+sign])
        final_result[name]=new_list
    return final_result

def main():
    rank=["A+","A","A-","B+","B","B-","C+","C","C-"]
    datas=[]
    datas.append(A_rank())
    datas.append(B_rank())
    datas.append(C_rank())
    for name in university_name:
        list_a={}
        count=0
        for data in datas:
            for i in range(0,len(data[name])):
                if len(data[name][i])==0:
                    continue
                else:
                    list_a[rank[count*3+i]]=data[name][i]
            count=count+1        
        print(name)
        print(list_a)

if __name__=='__main__':
    main();
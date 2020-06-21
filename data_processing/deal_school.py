'''
@author: Hongwentao
获取学各学校的相关数据
'''
from data_processing import deal_ruanke
import os
import numpy as np
import pandas as pd
data_path="../data/subject_data/ruanke_best_subject/"
university_name=["河北大学","山西大学","内蒙古大学","南昌大学","郑州大学","广西大学","海南大学","贵州大学","云南大学","西藏大学","青海大学","宁夏大学","新疆大学","石河子大学"]

def get_school_data(year):
    '''
                获 取各学校每年的课程评价数据,数据从2017年开始
                返回数据为字典
                示例如下：广西大学 :{2017:[['农学', '作物学', 22], ['农学', '林学', 17],。。。],2018:[。。。]},...,南昌大学,....
                
    '''
    final_result={}
    first_names=os.listdir(data_path)
    for first_name in first_names:
        first_path=data_path+first_name+"/"
        second_names=os.listdir(first_path)
        for second_name in second_names:
            second_path=first_path+second_name+"/"
            datas=deal_ruanke.every_subject_ruanke(first_name, second_name)
            for year in range(2017,year+1):
                
                try:
                   for school in datas[year]:
                       year_result={}
                       name_list=[]
                       name_list.append(first_name)
                       name_list.append(second_name)
                       name_list.append(school[0])
                       if school[2] not in final_result.keys():
                           new_list=[]
                           new_list.append(name_list)
                           year_result[year]=new_list
                           final_result[school[2]]=year_result
                       else:
                           year_result=final_result[school[2]]
                           if year in year_result.keys():
                               old_list=year_result[year]
                               old_list.append(name_list)
                               year_result[year]=old_list
                           else:
                               new_list=[]
                               new_list.append(name_list)
                               year_result[year]=new_list
                           final_result[school[2]]=year_result                                              
                except Exception:
                        #print(second_name+str(year)+"没有")
                        continue
    return final_result

def get_subject(school_name,this_year):
    '''
                各学校的各学科每年度的排名
    '''
    total_datas=get_school_data(this_year)
    datas=total_datas[school_name]
    final_result={}
    year_list=(list)(datas.keys())
    for year in year_list:
        for subject in datas[year]:
            year_result={}
            if subject[1] not in final_result.keys():
                name_list=[]
                name_list.append(subject[0])
                year_result[year]=subject[2]
                new_list=[]
                new_list.append(name_list)
                new_list.append(year_result)
                final_result[subject[1]]=new_list
            else:
                year_result=final_result[subject[1]][1]
                year_result[year]=subject[2]
                final_result[subject[1]][1]=year_result
    print(school_name+":")
    print(final_result)

def get_best_subject_school(school_name,year):
    '''
                获取学校里最好的学科
    school_name:学校名
    year:需要的年份
            河北大学:中国史 16 26.0%
    '''
    total_datas=get_school_data(year)
    datas=total_datas[school_name][year]
    final_result={}
    try:
        final_result={}
        data={}
        for subject in datas:
            total_number=deal_ruanke.number_of_subject__ruanke(subject[0], subject[1])
            final_grade=float(subject[2]/(total_number[year]))
            final_result[subject[1]]=final_grade
            data_list=[]
            data_list.append(subject[2])
            data_list.append(total_number[year])
            data[subject[1]]=data_list
        final_list=sorted(final_result.items(), key=lambda x: x[1],reverse = False)
        final_result=dict(final_list)
        a=(list)(final_result.keys())[0]
        b=data[a]
        final_return=[]
        final_return.append(school_name)
        final_return.append(a)
        final_return.append(b[0])
        final_return.append(str(round(final_result[a],2)*100)+"%")
        return final_return
    except Exception:
        print(school_name+str(year)+"无学科")

def get_subject_develop(school_name,this_year):
    '''
    
    '''
    if(this_year<2018):
        print("该年度没有该排名数据")
        return 0
    total_datas=get_school_data(this_year)
    datas=total_datas[school_name]
    final_result={}
    data={}
    for now in datas[this_year]:
        last_year=this_year-1
        subject=now[1]
        now_grade=now[2]
        for before in datas[last_year]:
            if subject==before[1]:
                before_grade=before[2]
                rate=(-(now_grade-before_grade)/before_grade)
                data_list=[]
                data_list.append(rate)
                data_list.append(now_grade)
                data_list.append(before_grade)
                data[subject]=data_list
                final_result[subject]=rate
                break
    final_list=sorted(final_result.items(), key=lambda x: x[1],reverse =True)
    final_result=dict(final_list)
    a=(list)(final_result.keys())[0]
    b=round(data[a][0],2)*100
    print(school_name+":"+a+":"+str(b)+"% "+str(data[a][2]-data[a][1]))        
        

def main():
    for name in university_name:
        get_subject(name, 2018)
if __name__=='__main__':
    main();
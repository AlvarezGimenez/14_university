'''
@author: Hongwentao
本文件处理软科(2016-2018)的所有的数据，同时提供数据接口，作为图形可视化的数据来源
'''
import csv
import pandas as pd
import numpy as np
import os
data_path="../data"
university_name=["河北大学","山西大学","内蒙古大学","南昌大学","郑州大学","广西大学","海南大学","贵州大学","云南大学","西藏大学","青海大学","宁夏大学","新疆大学","石河子大学"]
def get_total_ruanke(begin_year,end_year):
    '''
                提取并处理软科的最好大学的数据，此处处理的是14所全部的数据
                最后返回一个字典值
                字典格式：学校名称：列表[2016-2019]
                列表内是学校信息，格式如下
    [0-13][排名  ,学校名称 ,省市 ,总分,生源质量（新生高考成绩得分）,培养结果（毕业生就业率）,科研规模（论文数量·篇）,科研质量（论文质量·FWCI）,顶尖成果（高被引论文·篇）,顶尖人才（高被引学者·人）,科技服务（企业科研经费·千元）,产学研合作（校企合作论文·篇）,成果转化（技术转让收入·千元）]
    '''
    final_result={}
    final_path=data_path+"/total_data/ruanke/final_"
    for i in range(begin_year,end_year+1):
        year=str(i)
        file=open(final_path+year+".csv",encoding="utf-8")
        a=pd.read_csv(file,sep=',',skip_blank_lines=False);
        b=np.array(a)
        c=b.tolist()
        scl_name={}
        for s in range(0,len(c)):
            scl_name[c[s][1]]=s
        for name in university_name:
            if name in scl_name.keys():
                if name in final_result.keys():
                    new=list(final_result[name])
                    new.append(c[scl_name[name]])
                    final_result[name]=new
                else:
                    new=[]
                    new.append(c[scl_name[name]])
                    final_result[name]=new
            else:
                if name in final_result.keys():
                    new=list(final_result[name])
                    fake=[]
                    new.append(fake)
                    final_result[name]=new
                else:
                    new=[]
                    fake=[]
                    new.append(fake)
                    final_result[name]=new 
    return final_result   

'''
以下部分是部分项的数据提取函数
[排名  ,总分,生源质量（新生高考成绩得分）,培养结果（毕业生就业率）,科研规模（论文数量·篇）,科研质量（论文质量·FWCI）,顶尖成果（高被引论文·篇）,顶尖人才（高被引学者·人）,科技服务（企业科研经费·千元）,产学研合作（校企合作论文·篇）,成果转化（技术转让收入·千元）]
'''

def ranking_ruanke(begin_year,end_year):
    '''
                软科排名中各学校的排名数据,返回一个字典值，格式如下：
                学校名：（2016-2018）年的各年排名，如果该年无排名数据，则记为nan
                字典无特意排序
    '''
    data=get_total_ruanke(begin_year,end_year)
    #university_name
    final_result={}
    for name in university_name:
        all=data[name]#获取该大学的所有年份数据
        end=[]
        for year in all:
            if(len(year)==0):
                end.append('nan')
            else:
                if(year[0]=='nan'):
                    end.append('nan')
                else:
                    end.append(year[0])
        final_result[name]=end
    return final_result    

def grade_ruanke(begin_year,end_year):
    '''
                软科排名中各学校的排名数据,返回一个字典值，格式如下：
                学校名：（2016-2018）年的各年总分数据，如果该年无该数据，则记为nan
                字典无特意排序
    '''
    data=get_total_ruanke(begin_year,end_year)
    #university_name
    final_result={}
    for name in university_name:
        all=data[name]#获取该大学的所有年份数据
        end=[]
        for year in all:
            if(len(year)==0):
                end.append('nan')
            else:
                if(year[3]=='nan'):
                    end.append('nan')
                else:
                    end.append(year[3])
        final_result[name]=end
    return final_result    

def stu_quality_ruanke(begin_year,end_year):
    '''
                软科排名中各学校的排名数据,返回一个字典值，格式如下：
                学校名：（2016-2018）年的各年学生生源质量数据，如果该年无该数据，则记为nan
                字典无特意排序
    '''
    data=get_total_ruanke(begin_year,end_year)
    #university_name
    final_result={}
    for name in university_name:
        all=data[name]#获取该大学的所有年份数据
        end=[]
        for year in all:
            if(len(year)==0):
                end.append('nan')
            else:
                if(year[4]=='nan'):
                    end.append('nan')
                else:
                    end.append(year[4])
        final_result[name]=end
    return final_result   

def develop_result_ruanke(begin_year,end_year):
    '''
                软科排名中各学校的排名数据,返回一个字典值，格式如下：
                学校名：（2016-2018）年的各年培养结果数据，如果该年无该数据，则记为nan
                字典无特意排序
    '''
    data=get_total_ruanke(begin_year,end_year)
    #university_name
    final_result={}
    for name in university_name:
        all=data[name]#获取该大学的所有年份数据
        end=[]
        for year in all:
            if(len(year)==0):
                end.append('nan')
            else:
                if(isinstance(year[5],float)):
                    end.append('nan')
                else:
                    end.append(year[5])
        final_result[name]=end
    return final_result  

def scientific_scale_ruanke(begin_year,end_year):
    '''
                软科排名中各学校的排名数据,返回一个字典值，格式如下：
                学校名：（2016-2018）年的各年科研规模数据，如果该年无该数据，则记为nan
                字典无特意排序
    '''
    data=get_total_ruanke(begin_year,end_year)
    #university_name
    final_result={}
    for name in university_name:
        all=data[name]#获取该大学的所有年份数据
        end=[]
        for year in all:
            if(len(year)==0):
                end.append('nan')
            else:
                if(isinstance(year[6],float)):
                    end.append('nan')
                else:
                    end.append(year[6])
        final_result[name]=end
    return final_result  

def scientific_quanlity_ruanke(begin_year,end_year):
    '''
                软科排名中各学校的排名数据,返回一个字典值，格式如下：
                学校名：（2016-2018）年的各年科研质量数据，如果该年无该数据，则记为nan
                字典无特意排序
    '''
    data=get_total_ruanke(begin_year,end_year)
    #university_name
    final_result={}
    for name in university_name:
        all=data[name]#获取该大学的所有年份数据
        end=[]
        for year in all:
            if(len(year)==0):
                end.append('nan')
            else:
                if(isinstance(year[7],float)):
                    end.append('nan')
                else:
                    end.append(year[7])
        final_result[name]=end
    return final_result 

def top_result_ruanke(begin_year,end_year):
    '''
                软科排名中各学校的排名数据,返回一个字典值，格式如下：
                学校名：（2016-2018）年的各年顶尖成果数据，如果该年无该数据，则记为nan
                字典无特意排序
    '''
    data=get_total_ruanke(begin_year,end_year)
    #university_name
    final_result={}
    for name in university_name:
        all=data[name]#获取该大学的所有年份数据
        end=[]
        for year in all:
            if(len(year)==0):
                end.append('nan')
            else:
                if(isinstance(year[8],float)):
                    end.append('nan')
                else:
                    end.append(year[8])
        final_result[name]=end
    return final_result 

def top_people_ruanke(begin_year,end_year):
    '''
                软科排名中各学校的排名数据,返回一个字典值，格式如下：
                学校名：（2016-2018）年的各年顶尖人才数据，如果该年无该数据，则记为nan
                字典无特意排序
    '''
    data=get_total_ruanke(begin_year,end_year)
    #university_name
    final_result={}
    for name in university_name:
        all=data[name]#获取该大学的所有年份数据
        end=[]
        for year in all:
            if(len(year)==0):
                end.append('nan')
            else:
                if(isinstance(year[9],float)):
                    end.append('nan')
                else:
                    end.append(year[9])
        final_result[name]=end
    return final_result 

def scientific_service_ruanke(begin_year,end_year):
    '''
                软科排名中各学校的排名数据,返回一个字典值，格式如下：
                学校名：（2016-2018）年的各年科研服务数据，如果该年无该数据，则记为nan
                字典无特意排序
    '''
    data=get_total_ruanke(begin_year,end_year)
    #university_name
    final_result={}
    for name in university_name:
        all=data[name]#获取该大学的所有年份数据
        end=[]
        for year in all:
            if(len(year)==0):
                end.append('nan')
            else:
                if(isinstance(year[10],float)):
                    end.append('nan')
                else:
                    end.append(year[10])
        final_result[name]=end
    return final_result 

def industry_university_institute_cooperation_ruanke(begin_year,end_year):
    '''
                软科排名中各学校的排名数据,返回一个字典值，格式如下：
                学校名：（2016-2018）年的各年产学研合作数据，如果该年无该数据，则记为nan
                字典无特意排序
    '''
    data=get_total_ruanke(begin_year,end_year)
    #university_name
    final_result={}
    for name in university_name:
        all=data[name]#获取该大学的所有年份数据
        end=[]
        for year in all:
            if(len(year)==0):
                end.append('nan')
            else:
                if(isinstance(year[11],float)):
                    end.append('nan')
                else:
                    end.append(year[11])
        final_result[name]=end
    return final_result 

def achievements_ruanke(begin_year,end_year):
    '''
                软科排名中各学校的排名数据,返回一个字典值，格式如下：
                学校名：（2016-2018）年的各年成果转化数据，如果该年无该数据，则记为nan
                字典无特意排序
    '''
    data=get_total_ruanke(begin_year,end_year)
    #university_name
    final_result={}
    for name in university_name:
        all=data[name]#获取该大学的所有年份数据
        end=[]
        for year in all:
            if(len(year)==0):
                end.append('nan')
            else:
                if(isinstance(year[12],float)):
                    end.append('nan')
                else:
                    end.append(year[12])
        final_result[name]=end
    return final_result      

def every_subject_ruanke(name,subject_name):
    '''
                各个学科里这14个学校的排名，如果有学校的此专业进入该榜单，返回该学校名,排名和百分位段的字典形式,如果榜单里无14所学校，则返回一个空字典
                如果该排名有几年的数据,则按照字典形式，按照年份排序输出一个字典形式的返回值
                name:大的门类名，如经济学,subject_name:具体的学科名，如理论经济学
                最后返回格式如下：
     {2017: [[37, '前50%', '云南大学'], [45, '前50%', '南昌大学'], [46, '前50%', '山西大学'], [55, '前50%', '广西大学'], [58, '前50%', '河北大学']], 2018:          
    '''
    path=data_path+"/subject_data/ruanke_best_subject/"+name+"/"+subject_name+"/"+"final_"+subject_name+"_"
    final_result={}
    for year in range(2017,2019):
        if year==2017:
            final_path=path+str(year)+'.csv'
            isExists=os.path.exists(final_path)
            if isExists:
                data_list=[]
                try:
                    file=open(final_path,encoding="utf-8")
                    a=pd.read_csv(file,sep=',',skip_blank_lines=False);
                    b=np.array(a)
                    c=b.tolist()
                    for every in c:
                        line=[]
                        for i in range(0,3):
                            line.append(every[i])
                        data_list.append(line)
                except Exception:
                    print(final_path+str(year)+"没有数据")
                finally:
                    final_result[year]=data_list
        else:
            final_path=path+str(year)+'.csv'
            isExists=os.path.exists(final_path)
            if isExists:
                data_list=[]
                try:
                    file=open(final_path,encoding="utf-8")
                    a=pd.read_csv(file,sep=',',skip_blank_lines=False);
                    b=np.array(a)
                    c=b.tolist()
                    for every in c:
                        line=[]
                        for i in range(0,4):
                            if i==1:
                                continue
                            line.append(every[i])
                        data_list.append(line)
                except Exception:
                    print(final_path+year+"没有数据")
                finally:
                    final_result[year]=data_list
    return final_result

def number_of_subject__ruanke(name,subject_name):
    '''
                用于获得该专业参评学校的总数量
                格式：｛2017：xx，2018：xx｝
    '''
    path=data_path+"/subject_data/ruanke_best_subject/"+name+"/"+subject_name+"/"+subject_name+"_"
    final_result={}
    for year in range(2017,2019):
        final_path=path+str(year)+".csv"
        try:
            file=open(final_path,encoding="utf-8")
            a=pd.read_csv(file,sep=',',skip_blank_lines=False);
            b=np.array(a)
            c=b.tolist()
            x=len(c)
        except Exception:
            x=0
        finally:
            final_result[year]=x
    return final_result
'''     
#测试部分
def main():
    data=number_of_subject__ruanke("法学", "法学")
    print(data)

if __name__=='__main__':
    main();   
'''
    
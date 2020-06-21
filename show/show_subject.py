'''
@author: Hong wentao
@attention: 该文件是用于编写各学科的排名情况（学校排名）
'''
from data_processing import deal_jiaoyubu
from data_processing import deal_ruanke
import numpy as np
from pyecharts import Bar, Timeline
from pyecharts import Page
import os

html_path="../html/subject_html/"
university_name=["河北大学","山西大学","内蒙古大学","南昌大学","郑州大学","广西大学","海南大学","贵州大学","云南大学","西藏大学","青海大学","宁夏大学","新疆大学","石河子大学"]    
data_path="../data/subject_data/"
stand_height=150
stand_width="100%"

def show_space():
    '''
                用以间隔
    '''
    bar = Bar("",width=stand_width,height=stand_height)
    return bar

def show_ruanke_best(begin_year,end_year):
    '''
    @author: Hong wentao
             用于展示每一个学科的学校的排名可视化，使用的是软科最好大学排名的数据
    '''
    path=data_path+"ruanke_best_subject/"
    ruanke_html_path=html_path+"ruanke/"
    isExists=os.path.exists(ruanke_html_path)
    if not isExists:
        os.makedirs(ruanke_html_path)
    first_names=os.listdir(path)
    for first_name in first_names:
        first_data_path=path+first_name+"/"
        first_html_path=ruanke_html_path+first_name+"/"
        isExists=os.path.exists(first_html_path)
        if not isExists:
            os.makedirs(first_html_path)
        second_names=os.listdir(first_data_path)
        for second_name in second_names:
            second_data_path=first_data_path+second_name+"/"
            second_html_path=first_html_path+second_name+"/"
            isExists=os.path.exists(second_html_path)
            if not isExists:
                os.makedirs(second_html_path)
            data=deal_ruanke.every_subject_ruanke(first_name,second_name)    
            timeline = Timeline(is_auto_play=False, timeline_bottom=0,width=stand_width)
            for i in range(begin_year,end_year+1):
                bar = Bar(second_name+str(i)+"年大学排名数据")
                try:
                    want_data=data[i]
                    nan='空白区域说明该学校当年无该数据'
                    final_data=[]
                    have_name=[]
                    before_median=[]
                    for x in want_data:
                        have_name.append(x[2])
                    for name in university_name:
                        if name not in have_name:
                            final_data.append("nan")
                        else:
                            for x in want_data:
                                if x[2]==name:    
                                    final_data.append(x[0])
                                    before_median.append(x[0])
                                    break;
                    a=np.array(before_median).astype("int")
                    median=np.median(a).astype("int")
                    bar.add("排名  "+nan, university_name,final_data, is_label_show=True,is_stack=True,xaxis_interval=0,xaxis_name_size=15,xaxis_rotate=0,yaxis_name_rotate=0,xaxis_name_pos="end", xaxis_name="学校名",yaxis_name="排名",yaxis_name_gap=10,yaxis_name_pos="end",mark_point=["max","min"],mark_line_raw=[{"yAxis": median,"name":"中位数","lineStyle": {
                        "color": 'black'
                        }}])
                    timeline.add(bar, str(i)+'年') 
                    timeline.render(second_html_path+second_name+".html") 
                except Exception:
                    print(first_name+" "+second_name+str(i)+"没有")
                    continue    
            timeline.render(second_html_path+second_name+".html")  

def main():
    show_ruanke_best(2017,2018)
     
if __name__=='__main__':
    main();
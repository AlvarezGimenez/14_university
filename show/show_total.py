'''
@author: Hong wentao
@attention: 该文件是用于展示最终数据展现的可视化结果,最终所有的可视化结果图，显示在一个页面里
'''
from data_processing import deal_jiaoyubu
from data_processing import deal_ruanke
import numpy as np
from pyecharts import Bar, Timeline
from pyecharts import Page
from pyecharts.echarts.option import mark_line
from pyecharts import Funnel
from pyecharts import Geo
import os
html_path="../html/total_html/"
data_path="../data/"
stand_height=150
stand_width="100%"

def show_space():
    '''
                用以间隔
    '''
    bar = Bar("",width=stand_width,height=stand_height)
    return bar
def begin():
    '''
                用以开头间隔
    '''
    bar = Bar("",width=stand_width,height=50)
    return bar

def show_total_ruanke(begin_year,end_year):
    '''
    1.软科总体排名
    @author: Hong wentao
             最终的可视化结果呈现出的是2016年至今这14所学校在软科最好大学排名中的排名名次
    ''' 
    datas=deal_ruanke.ranking_ruanke(begin_year,end_year)
    university_name=(list)(datas.keys())
    ranking_datas=(list)(datas.values())
    timeline = Timeline(is_auto_play=False, timeline_bottom=0,width=stand_width)
    for i in range(0,end_year-begin_year+1):
        bar = Bar("软科"+str(2016+i)+"年大学排名数据")
        want_data=[]
        nan=''
        before_median=[]
        for x in ranking_datas:
            want_data.append(x[i])
            if x[i]=="nan":
                nan="（如果某学校当年无数据，则该区域为为空白）"
            else:
                before_median.append(x[i])
        a=np.array(before_median).astype("int")
        median=np.median(a).astype("int")
        bar.add("排名  "+nan, university_name,want_data, is_label_show=True,is_stack=True,xaxis_interval=0,xaxis_name_size=15,xaxis_rotate=0,yaxis_name_rotate=0,xaxis_name_pos="end", xaxis_name="学校名",yaxis_name="排名",yaxis_name_gap=10,yaxis_name_pos="end",mark_point=["max","min"],mark_line_raw=[{"yAxis": median,"name":"中位数","lineStyle": {
                        "color": 'black'
                    }}])
        timeline.add(bar, str(2016+i)+' 年')
    return timeline 

def show_subject_jiaoyubu():
    '''
    2.教育部学科排名
    @author: Hong wentao
                最终的可视化结果呈现出的是2017年教育部第四次学科评估中，各学校各等级的学科数比较结果
    ''' 
    a_datas=deal_jiaoyubu.A_rank()  
    b_datas=deal_jiaoyubu.B_rank()  
    c_datas=deal_jiaoyubu.C_rank()  
    university_name=(list)(a_datas.keys())
    a_list=(list)(a_datas.values())
    b_list=(list)(b_datas.values())
    c_list=(list)(c_datas.values())
    a_want=[]
    b_want=[]
    c_want=[]
    for school in a_list:
        count=0
        for rank in school:
            count=count+len(rank)
        a_want.append(count)
    for school in b_list:
        count=0
        for rank in school:
            count=count+len(rank)
        b_want.append(count)
    for school in c_list:
        count=0
        for rank in school:
            count=count+len(rank)
        c_want.append(count)
    bar = Bar("2017年教育部第四次全国学科评估（最新）",width=stand_width)
    bar.add("A等级",university_name,a_want, is_label_show=True,is_stack=False,xaxis_interval=0,xaxis_name_size=15,xaxis_rotate=0,xaxis_name_pos="end", xaxis_name="学校名",yaxis_name="数目",yaxis_name_pos="end",yaxis_name_gap=10)
    bar.add("B等级",university_name,b_want, is_label_show=True,is_stack=False,xaxis_interval=0,xaxis_name_size=15,xaxis_rotate=0,xaxis_name_pos="end", xaxis_name="学校名",yaxis_name="数目",yaxis_name_pos="end",yaxis_name_gap=10)
    bar.add("C等级",university_name,c_want, is_label_show=True,is_stack=False,xaxis_interval=0,xaxis_name_size=15,xaxis_rotate=0,xaxis_name_pos="end", xaxis_name="学校名",yaxis_name="数目",yaxis_name_pos="end",yaxis_name_gap=10)
    return bar

def show_best_subject_all(begin_year,end_year):
    '''
    3.14所学校中总体最好的学科展示（前五）
    @author: Hong wentao
                最终的可视化结果呈现出的是软科最好大学排名数据的结果
                数据说明：该数据采取软科最好大学排名，最好的学科取的是中位数排名前5的学校。并且，必须满足至少有5所学校具有该学科，通过实验验证所确定阈值。
    '''
    path=data_path+"subject_data/ruanke_best_subject/" 
    first_names=os.listdir(path)
    all_datas={}
    timeline = Timeline(is_auto_play=False, timeline_bottom=0,width=stand_width)
    for first_name in first_names:
        first_path=path+first_name+"/"
        second_names=os.listdir(first_path)
        for second_name in second_names:
            data=deal_ruanke.every_subject_ruanke(first_name, second_name)
            number_total=deal_ruanke.number_of_subject__ruanke(first_name, second_name)
            all_datas[second_name]=data    
    name=list(all_datas.keys())
    datas=list(all_datas.values())
    for year in range(begin_year,end_year+1):
        final_result={}
        for j in range(0,len(name)):
            all_year=datas[j]
            try:
                long=len(all_year[year])
                judge=False
                if(long>4):
                    judge=True
                rank_list=[]
                for per in all_year[year]:
                    rank_list.append(per[0])
                before_median=np.array(rank_list)
                median=np.median(before_median).astype("int")
                if judge:
                    final_result[name[j]]=median/number_total[begin_year]
            except Exception:
                continue
        final_list=sorted(final_result.items(), key=lambda x: x[1],reverse = False)
        final_dict=dict(final_list)
        final_name=(list(final_dict.keys()))[0:5]
        final_data=(list(final_dict.values()))[0:5]
        funnel = Funnel(str(year)+"年综合排名最好的五个学科", width=600, height=400, title_pos='left')
        funnel.add(
            "学科",
            final_name,
            final_data,
            is_label_show=True,
            label_pos="inside",
            label_text_color="#fff",
            funnel_sort="ascending",
            legend_pos="center",
            tooltip_formatter="{b}",
            )                
        timeline.add(funnel, str(year)+' 年')
    return timeline

def show_map_school(begin_year,end_year):
    '''
                用地图展示各学校的排名，这样可以观察地域与学校排名的关系
    '''
    datas=deal_ruanke.ranking_ruanke(begin_year,end_year)
    university_name=(list)(datas.keys())
    ranking_datas=(list)(datas.values())
    timeline = Timeline(is_auto_play=False, timeline_bottom=0,width=stand_width,height=500)
    for i in range(begin_year,end_year+1):        
        data=[] 
        dict={} 
        nan=''
        for j in range(0,len(university_name)):
            line=[]
            line.append(university_name[j])
            if(ranking_datas[j][i-begin_year]=="nan"):
                continue
            line.append(ranking_datas[j][i-begin_year])
            line_tuple=(tuple)(line)
            data.append(line_tuple)
            dict[university_name[j]]=ranking_datas[j][i-begin_year]
            if(i==2016):
                nan="(云南大学，青海大学，西藏大学未纳入排名)"
        geo = Geo(str(i)+"年度全国大学排名"+nan, "全国大学排名", title_color="#000",
        title_pos="center", width=1600,
        height=400, background_color='#DCDCDC')
        attr, value = geo.cast(data)
        geo.add("", attr, value, visual_range=[0, 600], maptype='china',visual_text_color="#000",
                symbol_size=20, is_visualmap=True,is_roam=False,visual_top="center",geo_normal_color="#404a59",visual_range_text=["high","low"],visual_range_color=['#50a3ba' ,'#faef61','#d94e5d'],label_formatter="{c0}",tooltip_formatter="{b}:  [经度(E)，纬度(N)，排名]  {c}名")
        geo
        timeline.add(geo,str(i)+'年')
    return timeline 
      
def main():
    page = Page() #初始化
    space=show_space()
    header=begin()
    page.add(header)
    first=show_total_ruanke(2016, 2018)
    page.add(first)
    page.add(space)
    second=show_subject_jiaoyubu()
    page.add(second)
    page.add(space)
    third=show_map_school(2016,2018)
    page.add(third)
    page.add(space)
    forth=show_best_subject_all(2017, 2018)
    page.add(forth)
    page.render(html_path+"total.html")  

if __name__=='__main__':
    main();

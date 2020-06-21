'''
@author: Hongwentao
用于展示关键词的词云图
'''
from wordcloud import WordCloud
from data_processing import deal_topdata
from data_processing.deal_topdata import get_top_word
import random
img_path="../top/"

def random_color_func(word=None, font_size=None, position=None,  orientation=None, font_path=None, random_state=None):
        h  = random.randint(120,250)
        s = int(100.0 * 255.0 / 255.0)
        l = int(100.0 * float(random.randint(60, 120)) / 255.0)
        return "hsl({}, {}%, {}%)".format(h, s, l)

def operation():
    datas=deal_topdata.get_top_word()
    word_list=(list(datas.keys()))[0:50]
    cloud_text=",".join(word_list)
    wc = WordCloud(
        background_color="white", #背景颜色
        max_words=200, #显示最大词数
        font_path=img_path+'simhei.ttf',  #使用字体
        min_font_size=45,
        max_font_size=100, 
        width=1960,  #图幅宽度
        height=900,
        prefer_horizontal=1.0,
        color_func = random_color_func
        )
    wc.generate(cloud_text)
    wc.to_file(img_path+"wordcloud.png")
def main():
    operation()

if __name__=='__main__':
    main();
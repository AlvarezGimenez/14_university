'''
2018
'''
import tabula
import csv
import pandas as pd
df = tabula.read_pdf(r"E:\Eclipse\14_university/2018.pdf", encoding='gbk', pages='all')
filename="E:\Eclipse\14_university\2018.pdf"
df.to_csv(filename)
    

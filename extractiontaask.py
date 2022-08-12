import re
import psycopg2
import os, shutil
from pdf_parser import data_extractor_numbers,data_extractor_alphanumeric,data_extractor_string
import sys
from datetime import datetime
import pandas as pd
import psycopg2
conn = psycopg2.connect(host="localhost", database="postgres",user="postgres", password="admin", port="5432")
cursor = conn.cursor()

# query1 = '''create table Rajni(Start_Time text,File_Name text,Vendor_Name text,Discription text,Invoice_No text,Invoice_Date text,PO_No text,PO_date text,GSTIN_Lohia text,GSTIN_Client text,HSN text,RATE text,Quantity text,Amount text,Grand_Total text,End_Time text)'''
# cursor.execute(query1)
# conn.commit()

sys.path.append(r"C:\Users\As\AppData\Local\Programs\Python\Python310\Lib\site-packages\aws_lib_")

from aws_lib_.aws_ocr_main import main_call


Pdf_Data = {}

l=['(',')','.','/','-',',','%','&']

def Trigger(input_path):
    output_path=r'C:\Users\As\Desktop\Sequalstring\excelfinaltask\folder9'#out put path.......
    text1=''
    os.chdir(output_path)
    # main_call(input_path)
    
    text_all=''
    for file in os.listdir(output_path):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        Pdf_Data['Start_Time']=current_time
        Pdf_Data['File_Name']=file
        if file.endswith('text.txt'):
            file_path= f'{output_path}\\{file}'
            with open(file_path,encoding='utf-8') as f:
                lines=f.read()
                # print(lines)
                text1=text1+lines
                # print(text1)

    # for file in os.listdir(r"C:\Users\As\Desktop\Sequalstring\excelfinaltask\outputttt"):
    #    os.remove(r"C:\Users\As\Desktop\Sequalstring\excelfinaltask\outputttt\\"+file)

    return text1
# Trigger(r"C:\Users\As\Desktop\Sequalstring\excelfinaltask\allpdf\img20220127_15213615.pdf")


def extract_all():
    input_path = ''
    New_Data = Trigger(input_path)
    New_Data = ' '.join(New_Data.split('\n'))
    print(New_Data)
    
    data_extractor_alphanumeric(New_Data,'TAX',1,Pdf_Data,'(Manufactures','Vendor_Name',l,'[A-Za-z]+\s[A-Za-z\s]+\.\s\&\s[A-Za-z]+',0)
    if Pdf_Data['Vendor_Name']==0:
        data_extractor_alphanumeric(New_Data,'.ph',1,Pdf_Data,'Original','Vendor_Name',l,'[A-Za-z]+\s[A-Za-z.\s]+\s\&\s[A-Za-z]+',0)
    data_extractor_alphanumeric(New_Data,'Inv.No.',1,Pdf_Data,'LOHIA','Invoice_No',l,'[A-Z]+\/[0-9]+\/[0-9]+',0)
    if Pdf_Data['Invoice_No']==0:
        data_extractor_alphanumeric(New_Data,'Invoice No.',1,Pdf_Data,'LOHIA','Invoice_No',l,'[0-9-0-9]+\/\w+\/\d+',0)
    data_extractor_alphanumeric(New_Data,'Date',1,Pdf_Data,'CHAUBEPUR','Invoice_Date',l,'\d+\-\w+\-\d+',0)
    if Pdf_Data['Invoice_Date']==0:
        data_extractor_alphanumeric(New_Data,'Date :',1,Pdf_Data,'LOHIA','Invoice_Date',l,'\d+\-\w+\-\d+',0)
    data_extractor_alphanumeric(New_Data,'P.O.No.',1,Pdf_Data,'P.O.Dt.','PO_No',l,'\d+',0)
    if Pdf_Data['PO_No']==0:
        data_extractor_alphanumeric(New_Data,'PO.No',1,Pdf_Data,'Date','PO_No',l,'[A-Z]+\d+',0)
    data_extractor_alphanumeric(New_Data,'P.O.Dt.',1,Pdf_Data,'Description','PO_date',l,'\d+\-\w+\-\d+',0)
    if Pdf_Data['PO_date']==0:
        data_extractor_alphanumeric(New_Data,'Date',3,Pdf_Data,'Description','PO_date',l,'\d+\-\w+\-\d+',0)
    data_extractor_alphanumeric(New_Data,'GST No',2,Pdf_Data,'P.O','GSTIN_Lohia',l,'\d+\w+',0)
    if Pdf_Data['GSTIN_Lohia']==0:
        data_extractor_alphanumeric(New_Data,'GSTIN',2,Pdf_Data,'Vendor Code','GSTIN_Lohia',l,'\d+\w+',0)
    data_extractor_alphanumeric(New_Data,'GSTIN No.',1,Pdf_Data,'Original','GSTIN_Client',l,'\d+\w+',0)
    if Pdf_Data['GSTIN_Client']==0:
        data_extractor_alphanumeric(New_Data,'GSTIN',1,Pdf_Data,'Name','GSTIN_Client',l,'\d+\w+',0)
    data_extractor_alphanumeric(New_Data,'TOTAL',1,Pdf_Data,'(in Words','Grand_Total',l,'[0-9.,0-9]+',0)
    if Pdf_Data['Grand_Total']==0:
        data_extractor_alphanumeric(New_Data,'Total',2,Pdf_Data,'(Rs.in Words :','Grand_Total',l,'[0-9,0-9]+',0)
    if Pdf_Data['Grand_Total']==0:
        data_extractor_alphanumeric(New_Data,'Total',2,Pdf_Data,'(Rs.in Words :','Grand_Total',l,'[0-9]+',0)
    if Pdf_Data['Grand_Total']==0:
        data_extractor_alphanumeric(New_Data,'TOTAL',1,Pdf_Data,'(in Werds','Grand_Total',l,'[0-9.,0-9]+',0)
    table = re.search(r'(?s)Value.*?Total',New_Data).group()
    # print(table)
    able = re.sub(r'Value|Total|1305569000|57083410|57083510|1215145000','',table)
    # print(able)
    if Pdf_Data['File_Name']=='img20220125_14541803-pdf-response.json':
        mul = re.findall(r'(?s)[A-Za-z\s.-]+\s[A-Z0-9a-z()"\s,-.]+\.\d+\s[0-9.,]+',able)
        # print(mul)
        for i in range(len(mul)):
            Split_Data = mul[i].split()
            # print(Split_Data)
            Pdf_Data['HSN']=Split_Data[-5]
            Pdf_Data['RATE']=Split_Data[-2]
            Pdf_Data['Quantity']=Split_Data[-3]
            Pdf_Data['Amount']=Split_Data[-1]
            dis = mul[i].split()[0:-5]
            Discription = ' '.join(dis)
            Pdf_Data['Discription']=Discription
            nows = datetime.now()
            curren = nows.strftime("%H:%M:%S")
            Pdf_Data['End_Time']=curren
            print(Pdf_Data)
            query2 = f''' insert into rajni values('{Pdf_Data['Start_Time']}','{Pdf_Data['File_Name']}','{Pdf_Data['Vendor_Name']}','{Pdf_Data['Discription']}','{Pdf_Data['Invoice_No']}','{Pdf_Data['Invoice_Date']}','{Pdf_Data['PO_No']}','{Pdf_Data['PO_date']}','{Pdf_Data['GSTIN_Lohia']}','{Pdf_Data['GSTIN_Client']}','{Pdf_Data['HSN']}','{Pdf_Data['RATE']}','{Pdf_Data['Quantity']}','{Pdf_Data['Amount']}','{Pdf_Data['Grand_Total']}','{Pdf_Data['End_Time']}') '''
            cursor.execute(query2)
            conn.commit() 
    if Pdf_Data['File_Name']=='img20220124_17060431-pdf-response.json' or Pdf_Data['File_Name']=='img20220124_17042225-pdf-response.json' or Pdf_Data['File_Name']=='img20220124_17072611-pdf-response.json':
        mul = re.findall(r'(?s)[A-Z]+\s[A-Z]+\s[A-Z]+\s[A-Z0-9-.\/]+\s[0-9]+\s[A-Z]+\s[0-9]+\s[0-9.]+\s[0-9,]+\.\d+',able)
        # print(mul)
        for i in range(len(mul)):
            Split_Data = mul[i].split()
            print(Split_Data)
            Pdf_Data['HSN']=Split_Data[-5]
            Pdf_Data['RATE']=Split_Data[-2]
            Pdf_Data['Quantity']=Split_Data[-3]
            Pdf_Data['Amount']=Split_Data[-1]
            dis = mul[i].split()[1:-5]
            Discription = ' '.join(dis)
            Pdf_Data['Discription']=Discription
            nows = datetime.now()
            curren = nows.strftime("%H:%M:%S")
            Pdf_Data['End_Time']=curren
            print(Pdf_Data)
            query2 = f''' insert into rajni values('{Pdf_Data['Start_Time']}','{Pdf_Data['File_Name']}','{Pdf_Data['Vendor_Name']}','{Pdf_Data['Discription']}','{Pdf_Data['Invoice_No']}','{Pdf_Data['Invoice_Date']}','{Pdf_Data['PO_No']}','{Pdf_Data['PO_date']}','{Pdf_Data['GSTIN_Lohia']}','{Pdf_Data['GSTIN_Client']}','{Pdf_Data['HSN']}','{Pdf_Data['RATE']}','{Pdf_Data['Quantity']}','{Pdf_Data['Amount']}','{Pdf_Data['Grand_Total']}','{Pdf_Data['End_Time']}') '''
            cursor.execute(query2)
            conn.commit()

    else:
        mul = re.findall(r'(?s)[A-Za-z\s.-]+\s[A-Z0-9a-z()"\s,-]+\.\d+\s[0-9.,]+',able)
        # print(mul)
        for i in range(len(mul)):
            Split_Data = mul[i].split()
            # print(Split_Data)
            Pdf_Data['HSN']=Split_Data[-5]
            Pdf_Data['RATE']=Split_Data[-2]
            Pdf_Data['Quantity']=Split_Data[-3]
            Pdf_Data['Amount']=Split_Data[-1]
            dis = mul[i].split()[0:-5]
            Discription = ' '.join(dis)
            Pdf_Data['Discription']=Discription
            nows = datetime.now()
            curren = nows.strftime("%H:%M:%S")
            Pdf_Data['End_Time']=curren
            print(Pdf_Data)
            # query2 = f''' insert into rajni values('{Pdf_Data['Start_Time']}','{Pdf_Data['File_Name']}','{Pdf_Data['Vendor_Name']}','{Pdf_Data['Discription']}','{Pdf_Data['Invoice_No']}','{Pdf_Data['Invoice_Date']}','{Pdf_Data['PO_No']}','{Pdf_Data['PO_date']}','{Pdf_Data['GSTIN_Lohia']}','{Pdf_Data['GSTIN_Client']}','{Pdf_Data['HSN']}','{Pdf_Data['RATE']}','{Pdf_Data['Quantity']}','{Pdf_Data['Amount']}','{Pdf_Data['Grand_Total']}','{Pdf_Data['End_Time']}') '''
            # cursor.execute(query2)
            # conn.commit()

    df=pd.read_sql_query('select * from rajni',con=conn)
    df.to_excel(r'C:\Users\As\Desktop\Sequalstring\excelfinaltask\Rajni.xlsx',index=False)
extract_all()


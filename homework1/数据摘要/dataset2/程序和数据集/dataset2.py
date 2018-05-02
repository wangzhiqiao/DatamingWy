# -*- coding: UTF-8 -*-
__author__ = 'Potato'

import xlrd
import json

#打开excel
def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print ('open failed',e)

#获取数据
def init():
    #打开excel表格
    file= 'dataset2.xlsx'
    data = open_excel(file)
    #进入表单“Sheet1”
    table = data.sheet_by_name('Sheet1')
    #获得Sheet1的行数与列数
    rows = table.nrows  #行数
    cols = table.ncols  #列数
    #把所有列的内容分别保存
    #获取标称变量的值（选取6列）
    nominalData={}
    nominalData["PlayType"]=table.col_values(2) #PlayType
    nominalData["PassOutcome"]=table.col_values(3)  #PassOutcome
    nominalData["PassLength"]=table.col_values(4)  #PassLength
    nominalData["PassLocation"]=table.col_values(5)#PassLocation


    #Number of Timesecs
    Time={}
    Time["TimeSecs"]=table.col_values(0)

  
    #yrdline
    yrdline={}
    yrdline["yrdline100"]=table.col_values(1)

 

    return nominalData,Time,yrdline



#求出标称量的频数
def nominalDatayrdline(nominalData):
    #PlayType
    nominalDataPermitType={}
    for item in nominalData["PlayType"]:
        if item not in nominalDataPermitType.keys():
            nominalDataPermitType[item]=1
        else:
            nominalDataPermitType[item]+=1

    #PassOutcome
    nominalDataCurrentStatus={}
    for item in nominalData["PassOutcome"]:
        if item not in nominalDataCurrentStatus.keys():
            nominalDataCurrentStatus[item]=1
        else:
            nominalDataCurrentStatus[item]+=1

    #PassLength
    nominalDataExistingUse={}
    for item in nominalData["PassLength"]:
        if item not in nominalDataExistingUse.keys():
            nominalDataExistingUse[item]=1
        else:
            nominalDataExistingUse[item]+=1

    #PassLocation
    nominalDataProposedUse={}
    for item in nominalData["PassLocation"]:
        if item not in nominalDataProposedUse.keys():
            nominalDataProposedUse[item]=1
        else:
            nominalDataProposedUse[item]+=1


    #标称变量的频数统计结果整体保存为json对象
    nominalDatayrdline={}
    nominalDatayrdline["PlayType"]=nominalDataPermitType
    nominalDatayrdline["PassOutcome"]=nominalDataCurrentStatus
    nominalDatayrdline["PassLength"]=nominalDataExistingUse
    nominalDatayrdline["PassLocation"]=nominalDataProposedUse

    #print json.dumps(nominalDatayrdline,indent=1)
    #保存结果
    fileIn=open(r"F:\nominalDatayrdline2.json",'w')
    data_save=json.dumps(nominalDatayrdline,indent=1)
    fileIn.write(data_save)

#数值属性，给出最大、最小、均值、中位数、四分位数及缺失值的个数
def statistic(Time,yrdline):
    (Time,yrdline)=cleaning(Time,yrdline)
    result={}
    #水样化学参数统计
    for key in Time:
        result[key]={}
        result[key]["max"]=max(Time[key])
        result[key]["min"]=min(Time[key])
        result[key]["mean"]=sum(Time[key])/len(Time[key])
        result[key]["midian"]=midian(Time[key])
        result[key]["quartiles"]=quartiles(Time[key])
        result[key]["miss_num"]=407688-len(Time[key])
    #yrdline 的统计
    for key in yrdline:
        result[key]={}
        result[key]["max"]=max(yrdline[key])
        result[key]["min"]=min(yrdline[key])
        result[key]["mean"]=sum(yrdline[key])/len(yrdline[key])
        result[key]["midian"]=midian(yrdline[key])
        result[key]["quartiles"]=quartiles(yrdline[key])
        result[key]["miss_num"]=407688-len(yrdline[key])
    #print json.dumps(result ,indent=1)
    #保存结果
    fileIn=open(r"F:\statistic_max_min_etc2.json",'w')
    data_save=json.dumps(result ,indent=1)
    fileIn.write(data_save)


#求中位数
def midian(arr):
    arr.sort()
    if(len(arr)%2==0):
        return (arr[len(arr)//2]+arr[len(arr)//2-1])//2.0
    else:
        return arr[len(arr)//2]

#求四分位数
def quartiles(arr):
    arr.sort()
    Q=[]
    Q1=arr[(len(arr)+1)//4-1]
    Q2=arr[((len(arr)+1)//4)*2-1]
    Q3=arr[((len(arr)+1)//4)*3-1]
    Q.append(Q1)
    Q.append(Q2)
    Q.append(Q3)
    return Q

#数据清洗 将缺失部分剔除（“XXXXXX”删除）
def cleaning(Time,yrdline):
    weed_Time=Time
    weed_yrdline=yrdline
    cleaning_weed(weed_Time)
    cleaning_weed(weed_yrdline)
    return Time,yrdline


#将缺失部分剔除（“XXXXXX”删除）
def cleaning_weed(obj):
    for key in obj.keys():
        tmp=[]
        for i in range(0, len(obj[key])):
            if(isinstance(obj[key][i],(float,int))==True):
                tmp.append(obj[key][i])
        obj[key]=tmp

if __name__=="__main__":
    #打开excel获取数据
    (nominalData,Time,yrdline)=init()
    #对标称属性，给出每个可能取值的频数，
    nominalDatayrdline(nominalData)
    #数值属性，给出最大、最小、均值、中位数、四分位数及缺失值的个数
    statistic(Time,yrdline)

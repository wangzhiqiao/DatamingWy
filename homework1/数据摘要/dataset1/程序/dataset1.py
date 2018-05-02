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
    file= 'dataset1.xlsx'
    data = open_excel(file)
    #进入表单“Sheet1”
    table = data.sheet_by_name('Sheet1')
    #获得Sheet1的行数与列数
    rows = table.nrows  #行数
    cols = table.ncols  #列数
    #把所有列的内容分别保存
    #获取标称变量的值（选取6列）
    nominalData={}
    nominalData["Permit Type"]=table.col_values(0) #Permit Type
    nominalData["Current Status"]=table.col_values(1)  #Current Status
    nominalData["Existing Use"]=table.col_values(2)  #Existing Use
    nominalData["Proposed Use"]=table.col_values(3)#Proposed Use
    nominalData["Existing Construction Type"]=table.col_values(4)#Existing Construction Type
    nominalData["Proposed Construction Type"]=table.col_values(5)#Proposed Construction Type

    #Number of Existing/proposed Stories
    Numberofstories={}
    Numberofstories["existingstories"]=table.col_values(6)
    Numberofstories["proposedstories"]=table.col_values(7)
  
    #cost
    cost={}
    cost["Estimated"]=table.col_values(8)
    cost["Revised"]=table.col_values(9)
 

    return nominalData,Numberofstories,cost



#求出标称量的频数
def nominalDatacost(nominalData):
    #Permit Type
    nominalDataPermitType={}
    for item in nominalData["Permit Type"]:
        if item not in nominalDataPermitType.keys():
            nominalDataPermitType[item]=1
        else:
            nominalDataPermitType[item]+=1

    #Current Status
    nominalDataCurrentStatus={}
    for item in nominalData["Current Status"]:
        if item not in nominalDataCurrentStatus.keys():
            nominalDataCurrentStatus[item]=1
        else:
            nominalDataCurrentStatus[item]+=1

    #Existing Use
    nominalDataExistingUse={}
    for item in nominalData["Existing Use"]:
        if item not in nominalDataExistingUse.keys():
            nominalDataExistingUse[item]=1
        else:
            nominalDataExistingUse[item]+=1

    #Proposed Use
    nominalDataProposedUse={}
    for item in nominalData["Proposed Use"]:
        if item not in nominalDataProposedUse.keys():
            nominalDataProposedUse[item]=1
        else:
            nominalDataProposedUse[item]+=1

    #Existing Construction Type
    nominalDataExistingCT={}
    for item in nominalData["Existing Construction Type"]:
        if item not in nominalDataExistingCT.keys():
            nominalDataExistingCT[item]=1
        else:
            nominalDataExistingCT[item]+=1

     #Proposed Construction Type
    nominalDataExistingPT={}
    for item in nominalData["Proposed Construction Type"]:
        if item not in nominalDataExistingPT.keys():
            nominalDataExistingPT[item]=1
        else:
            nominalDataExistingPT[item]+=1

    #标称变量的频数统计结果整体保存为json对象
    nominalDatacost={}
    nominalDatacost["Permit Type"]=nominalDataPermitType
    nominalDatacost["Current Status"]=nominalDataCurrentStatus
    nominalDatacost["Existing Use"]=nominalDataExistingUse
    nominalDatacost["Proposed Use"]=nominalDataProposedUse
    nominalDatacost["Existing Construction Type"]=nominalDataExistingCT
    nominalDatacost["Proposed Construction Type"]=nominalDataExistingPT
    #print json.dumps(nominalDatacost,indent=1)
    #保存结果
    fileIn=open(r"F:\nominalDatacost.json",'w')
    data_save=json.dumps(nominalDatacost,indent=1)
    fileIn.write(data_save)

#数值属性，给出最大、最小、均值、中位数、四分位数及缺失值的个数
def statistic(Numberofstories,cost):
    (Numberofstories,cost)=cleaning(Numberofstories,cost)
    result={}
    #水样化学参数统计
    for key in Numberofstories:
        result[key]={}
        result[key]["max"]=max(Numberofstories[key])
        result[key]["min"]=min(Numberofstories[key])
        result[key]["mean"]=sum(Numberofstories[key])/len(Numberofstories[key])
        result[key]["midian"]=midian(Numberofstories[key])
        result[key]["quartiles"]=quartiles(Numberofstories[key])
        result[key]["miss_num"]=198898-len(Numberofstories[key])
    #cost 的统计
    for key in cost:
        result[key]={}
        result[key]["max"]=max(cost[key])
        result[key]["min"]=min(cost[key])
        result[key]["mean"]=sum(cost[key])/len(cost[key])
        result[key]["midian"]=midian(cost[key])
        result[key]["quartiles"]=quartiles(cost[key])
        result[key]["miss_num"]=198898-len(cost[key])
    #print json.dumps(result ,indent=1)
    #保存结果
    fileIn=open(r"F:\statistic_max_min_etc.json",'w')
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
def cleaning(Numberofstories,cost):
    weed_Numberofstories=Numberofstories
    weed_cost=cost
    cleaning_weed(weed_Numberofstories)
    cleaning_weed(weed_cost)
    return Numberofstories,cost


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
    (nominalData,Numberofstories,cost)=init()
    #对标称属性，给出每个可能取值的频数，
    nominalDatacost(nominalData)
    #数值属性，给出最大、最小、均值、中位数、四分位数及缺失值的个数
    statistic(Numberofstories,cost)

# -*- coding: UTF-8 -*-
__author__ = 'Wangyu'

import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pylab as pl
import scipy.stats as stats

def readFile(path):
    fileObj=open(path)
    data=fileObj.read()
    return data

def show():
    data=readFile("data.json")
    data=json.loads(data)
    for key in data["cost"].keys():
        ai= data["cost"][key]
       # ai.sort()

        pl.figure()
        pl.hist(ai,bins=50,normed=True)
        pl.savefig(key+"_histogram.svg")
        pl.close()

        #QQ
        pl.figure()
        stats.probplot(ai,dist="norm",plot=plt)
        plt.title(key+"_qq plot")
        plt.savefig(key+"_qq-plot.svg")
        plt.close()
    
        #box plot
        fig=plt.figure(1,figsize=(9,6))
        axes = fig.add_subplot(111)
        boxplot=axes.boxplot(ai)
        fig.savefig(key+"_box-plot.svg",bbox_inches='tight')
        plt.close()

    for key in data["Numberofstories"].keys():
        ai= data["Numberofstories"][key]
       # ai.sort()

        pl.figure()
        pl.hist(ai,bins=50,normed=True)
        pl.savefig(key+"_histogram.svg")
        pl.close()

        #QQ
        pl.figure()
        stats.probplot(ai,dist="norm",plot=plt)
        plt.title(key+"_qq plot")
        plt.savefig(key+"_qq-plot.svg")
        plt.close()

        #box plot
        fig=plt.figure(1,figsize=(9,6))
        axes = fig.add_subplot(111)
        boxplot=axes.boxplot(ai)
        fig.savefig(key+"_box-plot.svg",bbox_inches='tight')
        plt.close()
if __name__=="__main__":
    show()
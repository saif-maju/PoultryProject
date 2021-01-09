import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import StringIO
import seaborn as sns
import pandas as pd

def barChart(x,y,title,xlabel,ylabel):
    sns.set_theme(style="whitegrid")
    fig = plt.figure(figsize=(9,5)) 
    plt.bar(x,y, alpha=0.8)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.close()
    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)
    image = imgdata.getvalue()
    return image

def violinChart(x,title,xlabel,ylabel):
    sns.set_theme(style="whitegrid")
    fig = plt.figure(figsize=(9,5)) 
    plt.violinplot(x,showmeans=True, showmedians=True,
        showextrema=True)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.close()
    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)
    image = imgdata.getvalue()
    return image


def histChart(x,title,xlabel,ylabel):
    sns.set_theme(style="whitegrid")
    fig = plt.figure(figsize=(9,5)) 
    plt.hist(x,bins=20)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.close()
    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)
    image = imgdata.getvalue()
    return image


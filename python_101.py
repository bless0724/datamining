# -*- coding: utf-8 -*-     支持文件中出现中文字符
#####################################################################
import decorator
import numpy as np
import pandas as pd
from scipy import signal
import math
import matplotlib.pylab as plt #绘图
import os
import gc   #gc模块提供一个接口给开发者设置垃圾回收的选项
import time

def list_of_groups(init_list, childern_list_len):#设定滑动时间窗，每一个sharp wave为一个list
    list_of_groups = zip(*(iter(init_list),) *childern_list_len)
    end_list = [list(i) for i in list_of_groups]
    count = len(init_list) % childern_list_len
    end_list.append(init_list[-count:]) if count !=0 else end_list
    return end_list


#读取文件第一列，保存在s1列表中
###########################################################################################################
start = 113 #从start开始做N个文件的图                    #设立变量start，作为循环读取文件的起始
N = 1                                                      #设立变量N，作为循环读取文件的增量
for e in range(start,start+N):                            #读取113&1文件
    data = open(r'20151026_%d' % (e)).read()     #设立data列表变量，python 文件流，%d处，十进制替换为e值，.read读文件
    data = data.split( )                                  #以空格为分隔符，返回数值列表data
    data = [float(s) for s in data]                       #将列表data中的数值强制转换为float类型

    s1 = data[0:45000*4:4]                          #list切片L[n1:n2:n3]  n1代表开始元素下标；n2代表结束元素下标
                                                    #n3代表切片步长，可以不提供，默认值是1，步长值不能为0
####################################################################################################################

#滤波
##################################################################################################################
    fs = 3000                                           #设立频率变量fs
    lowcut = 1
    highcut = 30
    order = 2                                           #设立滤波器阶次变量
    nyq = 0.5*fs                                        #设立采样频率变量nyq，采样频率=fs/2。
    low = lowcut/nyq
    high = highcut/nyq
    b, a = signal.butter(order, [low, high], btype='band') #设计巴特沃斯带通滤波器 “band”
    s1_filter1 = signal.lfilter(b,a,s1)                 #将s1带入滤波器，滤波结果保存在s1_filter1中
###################################################################################################################

#计算相关性与相异性
###################################################################################################################
    cor = []
    idcompare = []
    time_window = 1800
    wave = list_of_groups(s1_filter1, time_window) #滑动时间窗设为1800
    count = int(len(s1_filter1)/ time_window) #计算有多少个sharp_wave
    for i in range(0, count-1):
        for j in range(i+1, count):
            wave2 = pd.Series(wave[j])
            wave1 = pd.Series(wave[i])
            cor1 = math.fabs(wave1.corr(wave2)) #计算两个sharp_wave的pearson相关系数
            cor.append(cor1) #记录相关系数
            idcompare.append([i+1, j+1]) #记录两个波的id
    data2 = pd.DataFrame({'idcompare': idcompare, 'cor': cor}) #将波的对和相关系数存在data2中
    data2 = data2.sort_values(by='cor', axis=0, ascending=False) #按照相关系数大小排序
    data2 = data2.reset_index(drop=True) #重置data2的编号
    data2_length = len(data2) #计算data2的行数
    print("最相关的三对：")
    for i in range(3):  #输出最相关的三对
        print("第", i+1, "对:", (data2.loc[i, 'idcompare'])[0]*time_window, "与", (data2.loc[i, 'idcompare'])[1]*time_window)
        print("相关系数为:", round(data2.loc[i,"cor"], 4), "\n")
    print("最相异的三对：")
    for i in range(3):  #输出最相异的三对
        print("第", i+1, "对:", (data2.loc[data2_length-1-i, 'idcompare'])[0]*time_window, "与", (data2.loc[data2_length-1-i, 'idcompare'])[1]*time_window)
        print("相关系数为:", round(data2.loc[data2_length-1-i, "cor"], 4), "\n")
###################################################################################################################

#画图
###################################################################################################################
    fig1 = plt.figure()                             #创建画图对象，开始画图
    ax1 = fig1.add_subplot(211)                     #在一张figure里面生成多张子图，将画布分割成2行1列， 图像画在从左到右从上到下的第1块

    plt.plot(s1_filter1[(data2.loc[i, 'idcompare'])[0]*time_window:((data2.loc[i, 'idcompare'])[0]+1)*time_window],color='r') #绘制最相关的波其一
    ax1.set_title('Similar singals')               #设定title为Similar singals
    plt.ylabel('Amplitude')                         #设定子图211的Y轴lable为amplitude

    ax2 = fig1.add_subplot(212)
                    # 在一张figure里面生成多张子图，将画布分割成2行1列， 图像画在从左到右从上到下的第2块

    plt.plot(s1_filter1[(data2.loc[i, 'idcompare'])[1]*time_window:((data2.loc[i, 'idcompare'])[1]+1)*time_window],color='r') #绘制最相关的波其二
    plt.ylabel('Amplitude')                         #设定子图212的Y轴lable为amplitude

    fig2 = plt.figure()  # 创建画图对象，开始画图
    ax3 = fig2.add_subplot(211) # 在一张figure里面生成多张子图，将画布分割成2行1列， 图像画在从左到右从上到下的第1块

    plt.plot(
        s1_filter1[(data2.loc[data2_length-1-i, 'idcompare'])[0] * time_window:((data2.loc[data2_length-1-i, 'idcompare'])[0] + 1) * time_window],
        color='r')  # 绘制最相异的波其一
    ax3.set_title('Different singals')  # 设定title为Different singals
    plt.ylabel('Amplitude')  # 设定子图211的Y轴lable为amplitude

    ax4 = fig2.add_subplot(212)
    # 在一张figure里面生成多张子图，将画布分割成2行1列， 图像画在从左到右从上到下的第2块

    plt.plot(
        s1_filter1[(data2.loc[data2_length-1-i, 'idcompare'])[1] * time_window:((data2.loc[data2_length-1-i, 'idcompare'])[1] + 1) * time_window],
        color='r')  # 绘制最相异的波其二
    plt.ylabel('Amplitude')  # 设定子图212的Y轴lable为amplitude

    plt.show()
##################################################################################################################
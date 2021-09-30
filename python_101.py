# -*- coding: utf-8 -*-     支持文件中出现中文字符
#########################################################################

"""
Created on Fri Jan 06 10:08:42 2017

@author: Yuyangyou

代码功能描述：（1）读取Sharp_waves文件，
              （2）采用巴特沃斯滤波器，进行60-240Hz滤波
              （3）画图
              （4）....

"""
#####################################################################
import decorator
import numpy as np
import pandas as pd
from scipy import signal
import math
import matplotlib
import matplotlib.pylab as plt #绘图
#from numpy import *
import os
import gc   #gc模块提供一个接口给开发者设置垃圾回收的选项
import time

# def correlation_coefficient(array1, array2, n): #计算相关系数
#     sum1 = 0.0
#     sum2 = 0.0
#     sum11 = 0.0
#     sum22 = 0.0
#     sum12 = 0.0
#     for i in range(0, n):
#         sum1 += array1[i]
#         sum2 += array2[i]
#         sum12 += array1[i]*array2[i]
#         sum11 += math.pow(array1[i], 2)
#         sum22 += math.pow(array2[i], 2)
#     cov12 = (n*sum12-sum1*sum2)/math.pow(n, 2)
#     var1 = (n*sum11-math.pow(sum1, 2))/math.pow(n, 2)
#     var2 = (n*sum22-math.pow(sum2, 2))/math.pow(n, 2)
#     cor = cov12/math.sqrt(var1 * var2)
#     return cor

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
for e in range(start,start+N):                            #循环2次，读取113&114两个文件
    data = open(r'20151026_%d' % (e)).read()     #设立data列表变量，python 文件流，%d处，十进制替换为e值，.read读文件
    data = data.split( )                                  #以空格为分隔符，返回数值列表data
    data = [float(s) for s in data]                       #将列表data中的数值强制转换为float类型

<<<<<<< HEAD
    s1 = data[0:45000*4:4]                          #list切片L[n1:n2:n3]  n1代表开始元素下标；n2代表结束元素下标
=======
    s1 = data[0:14994*4:4]                          #list切片L[n1:n2:n3]  n1代表开始元素下标；n2代表结束元素下标
>>>>>>> ee377eee7885028e693f39a8ebfaae505a983e6a
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
    b,a = signal.butter(order,[low,high],btype='band') #设计巴特沃斯带通滤波器 “band”
    s1_filter1 = signal.lfilter(b,a,s1)                 #将s1带入滤波器，滤波结果保存在s1_filter1中
    #print(s1_filter1)
###################################################################################################################

#计算相关性与相异性
###################################################################################################################
    cor = []
    #id = []
    idcompare = []
<<<<<<< HEAD
    time_window = 1800
    wave = list_of_groups(s1_filter1 ,time_window) #滑动时间窗设为1666ms
    count = int(len(s1_filter1)/ time_window) #计算有多少个sharp_wave
=======
    wave = list_of_groups(s1_filter1 ,1666)#滑动时间窗设为1666ms
    count = int(len(s1_filter1)/ 1666)#计算有多少个sharp_wave
>>>>>>> ee377eee7885028e693f39a8ebfaae505a983e6a
    # for i in range(0,count):
    #     id.append(i+1)
    # data1 = pd.DataFrame({'id': id, 'wave': wave})
    # print(data1)
    for i in range(0, count-1):
        for j in range(i+1, count):
            wave2 = pd.Series(wave[j])
            wave1 = pd.Series(wave[i])
<<<<<<< HEAD
            cor1 = math.fabs(wave1.corr(wave2)) #计算两个sharp_wave的pearson相关系数
            cor.append(cor1) #记录相关系数
            idcompare.append([i+1,j+1]) #记录两个波的id
            #cor.append([math.fabs(correlation_coefficient(wave[i], wave[j], 1666)),[i+1,j+1]])
    data2 = pd.DataFrame({'idcompare': idcompare, 'cor': cor}) #将波的对和相关系数存在data2中
    data2 = data2.sort_values(by='cor', axis=0, ascending=False) #按照相关系数大小排序
    data2 = data2.reset_index(drop=True) #重置data2的编号
    data2_length = len(data2) #计算data2的行数
    #print(data2)
    print("最相关的三对：")
    for i in range(3):
        print("第", i+1, "对:", (data2.loc[i, 'idcompare'])[0]*time_window, "与", (data2.loc[i, 'idcompare'])[1]*time_window)
        print("相关系数为:", round(data2.loc[i,"cor"], 4), "\n")
    print("最相异的三对：")
    for i in range(3):
        print("第", i+1, "对:", (data2.loc[data2_length-1-i, 'idcompare'])[0]*time_window, "与", (data2.loc[data2_length-1-i, 'idcompare'])[1]*time_window)
        print("相关系数为:", round(data2.loc[data2_length-1-i, "cor"], 4), "\n")
=======
            cor1 = math.fabs(wave1.corr(wave2))#计算两个sharp_wave的pearson相关系数
            cor.append(cor1)#记录相关系数
            idcompare.append([i+1,j+1])#记录两个波的id
            #cor.append([math.fabs(correlation_coefficient(wave[i], wave[j], 1666)),[i+1,j+1]])
    data2 = pd.DataFrame({'idcompare': idcompare, 'cor': cor})
    data2.sort_values(by='cor', axis=0, ascending=True, inplace=True)#按照相关系数大小排序
    print(data2)
>>>>>>> ee377eee7885028e693f39a8ebfaae505a983e6a
###################################################################################################################

#画图
###################################################################################################################
    fig1 = plt.figure()                             #创建画图对象，开始画图
<<<<<<< HEAD
    # ax1 = fig1.add_subplot(211)
    #                 #在一张figure里面生成多张子图，将画布分割成2行1列， 图像画在从左到右从上到下的第1块
    #                 #例如，fig1.add_subplot(349)  将画布分割成3行4列，图像画在从左到右从上到下的第9块
    #
    # plt.plot(s1,color='r')                          #在选定的画布位置上，画未经滤波的s1图像，设定颜色为红色
    # ax1.set_title('Denoised Signal')               #设定子图211的title为denoised signal
    # plt.ylabel('Amplitude')                         #设定子图211的Y轴lable为amplitude

    ax2 = fig1.add_subplot(111)
=======
    ax1 = fig1.add_subplot(211)
                    #在一张figure里面生成多张子图，将画布分割成2行1列， 图像画在从左到右从上到下的第1块
                    #例如，fig1.add_subplot(349)  将画布分割成3行4列，图像画在从左到右从上到下的第9块

    plt.plot(s1,color='r')                          #在选定的画布位置上，画未经滤波的s1图像，设定颜色为红色
    ax1.set_title('Denoised Signal')               #设定子图211的title为denoised signal
    plt.ylabel('Amplitude')                         #设定子图211的Y轴lable为amplitude

    ax2 = fig1.add_subplot(212)
>>>>>>> ee377eee7885028e693f39a8ebfaae505a983e6a
                    # 在一张figure里面生成多张子图，将画布分割成2行1列， 图像画在从左到右从上到下的第2块

    plt.plot(s1_filter1,color='r')                  #在选定的画布位置上，画经过滤波的s1_filter1图像，设定颜色为红色
    ax2.set_title('Denoised Signal')               #设定子图212的title为denoised signal
    plt.ylabel('Amplitude')                         #设定子图212的Y轴lable为amplitude
    plt.show()
    #plt.subplots_adjust(hspace=1)
    #plt.savefig(r'20151026_%d.png' % (e))  #保存图像，设定保存路径并统一命名，%d处，十进制替换为e值
    #plt.close('all')                                 #关闭绘图对象，释放绘图资源
    #print(e)
##################################################################################################################








































































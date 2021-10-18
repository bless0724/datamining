# -*- coding: utf-8 -*-     支持文件中出现中文字符
#####################################################################
import random

import decorator
import numpy as np
import pandas as pd
from scipy import signal
import math
import matplotlib
from matplotlib import pyplot as plt
import os
import gc   #gc模块提供一个接口给开发者设置垃圾回收的选项
import time

def  psfeatureTime(data):#计算特征,随机加label
    # 均值
    df_mean = data.mean()
    # 方差
    df_var = data.var()
    # 标准差
    df_std = data.std()
    # 均方根
    df_rms = np.sqrt(pow(df_mean, 2) + pow(df_std, 2))
    # 偏度
    df_skew = pd.Series(data).skew()
    # 峰度
    df_kurt = pd.Series(data).kurt()
    # sum = 0
    # for i in range(len(data)):
    #     sum += np.sqrt(abs(data[i]))
    # # 波形因子
    # df_boxing = df_rms / (abs(data).mean())
    # # 峰值因子
    # df_fengzhi = (max(data)) / df_rms
    # # 脉冲因子
    # df_maichong = (max(data)) / (abs(data).mean())
    # # 裕度因子
    # df_yudu = max(data) / pow(sum / (len(data)), 2)
    # # 峭度
    # df_qiaodu = (np.sum([x ** 4 for x in data]) / len(data)) / pow(df_rms, 4)
    df_label = random.randint(1, 3)
    featuretime_list = [df_mean, df_var, df_std, df_rms, df_skew, df_kurt, #df_boxing, df_fengzhi, df_maichong, df_yudu, df_qiaodu,
     df_label]
    return featuretime_list

def list_of_groups(init_list, childern_list_len):#设定滑动时间窗，每一个sharp wave为一个list
    list_of_groups = zip(*(iter(init_list),) *childern_list_len)
    end_list = [list(i) for i in list_of_groups]
    count = len(init_list) % childern_list_len
    end_list.append(init_list[-count:]) if count != 0 else end_list
    return end_list

def gini_Impurity(pos, label, length):
    count = [0,0,0]
    for i in range(pos):
        if label[i] == 1:
            count[0] += 1
        elif label[i] == 2:
            count[1] += 1
        else:
            count[2] += 1
    ginileft = 1-math.pow(count[0]/(pos+1), 2)-math.pow(count[1]/(pos+1), 2)-math.pow(count[2]/(pos+1), 2)
    count = [0, 0, 0]
    for i in range(pos, length):
        if label[i] == 1:
            count[0] += 1
        elif label[i] == 2:
            count[1] += 1
        else:count[2] += 1
    giniright = 1-math.pow(count[0]/(length-pos+1), 2)-math.pow(count[1]/(length-pos+1), 2)-math.pow(count[2]/(length-pos+1), 2)
    gini = ((pos+1)/length)*ginileft + (1-((pos+1)/length))*giniright
    return gini

def CART_Decision_Tree():

#读取文件第一列，保存在s1列表中
###########################################################################################################
start = 113 #从start开始做N个文件的图                    #设立变量start，作为循环读取文件的起始
N = 2                                                      #设立变量N，作为循环读取文件的增量
for e in range(start, start+N):                            #循环2次，读取113&114两个文件
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
    s1_filter1 = signal.lfilter(b, a, s1)                 #将s1带入滤波器，滤波结果保存在s1_filter1中
###################################################################################################################

#计算特征
########################################################################################################
    s1_feature = []
    s1_list = list_of_groups(s1_filter1, 150) #时间窗为150
    count = int(len(s1_filter1) / 150)  # 有300个采样点
    for i in range(0, count):
        s1_feature.append(psfeatureTime(np.array(s1_list[i])))#每一个采样点计算特征值
###################################################################################################################
    idx = pd.Index(np.arange(1, count + 1))  # 行索引
    df_feature = pd.DataFrame(s1_feature, index=idx,
                              columns=['均值', '方差', '标准差', '均方根', '偏度', '峰度',
                                       #'波形因子', '峰值因子', '脉冲因子', '裕度因子','峭度'
                                       'label'])  # dataframe格式保存，行为每一秒，列为特征值
    vals = np.around(df_feature.values, 5)  # 数值保留5位小数

    df_feature = df_feature.sort_values(by='均值', axis=0, ascending=True) #按照相关系数大小排序
    df_feature = df_feature.reset_index(drop=True) #重置data2的编号
    gini_array = np.zeros(count+1)
    for i in range(count+1):
        gini_array[i] = gini_Impurity(i,df_feature['label'],count)
    split_pos = np.argmin(gini_array)
    print(split_pos)
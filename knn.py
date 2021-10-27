# -*- coding: utf-8 -*-     支持文件中出现中文字符
#####################################################################
import operator
import random

import numpy
import numpy as np
import pandas as pd
from scipy import signal
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def  psfeatureTime(data):#计算特征
    # 均值
    df_mean = data.mean()
    # 标准差
    df_std = data.std()
    # 均方根
    df_rms = np.sqrt(pow(df_mean, 2) + pow(df_std, 2))
    # 偏度
    df_skew = pd.Series(data).skew()
    # 峰度
    df_kurt = pd.Series(data).kurt()
    sum = 0
    for i in range(len(data)):
        sum += np.sqrt(abs(data[i]))
    # 峰值因子
    df_fengzhi = (max(data)) / df_rms
    # 裕度因子
    df_yudu = max(data) / pow(sum / (len(data)), 2)
    # 峭度
    df_qiaodu = (np.sum([x ** 4 for x in data]) / len(data)) / pow(df_rms, 4)
    featuretime_list = [df_mean, df_skew, df_kurt, df_fengzhi, df_yudu, df_qiaodu]
    return featuretime_list

def list_of_groups(init_list, childern_list_len):#设定滑动时间窗，每一个sharp wave为一个list
    list_of_groups = zip(*(iter(init_list),) *childern_list_len)
    end_list = [list(i) for i in list_of_groups]
    count = len(init_list) % childern_list_len
    end_list.append(init_list[-count:]) if count != 0 else end_list
    return end_list


def knn(trainData, testData, labels, k):
    # 计算训练样本的行数
    rowSize = trainData.shape[0]
    # 计算训练样本和测试样本的差值
    diff = np.tile(testData, (rowSize, 1)) - trainData
    # 计算差值的平方和
    sqrDiff = diff ** 2
    sqrDiffSum = sqrDiff.sum(axis=1)
    # 计算距离
    distances = sqrDiffSum ** 0.5
    # 对所得的距离从低到高进行排序
    sortDistance = distances.argsort()

    count = {}
    # 投票
    for i in range(k):
        vote = labels[sortDistance[i]]
        count[vote] = count.get(vote, 0) + 1
    # 对类别出现的频数从高到低进行排序
    sortCount = sorted(count.items(), key=operator.itemgetter(1), reverse=True)

    # 返回出现频数最高的类别
    return sortCount[0][0]

# 混淆矩阵
def confusion_matrix(predict,real):
    matrix = numpy.zeros((3,3)).astype('int64')
    for i in range(len(predict)):
        x = int(predict[i])-1
        y = int(real[i])-1
        matrix[x][y] += 1
    return matrix

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

########################################################################################################
    s1_feature = []
    s1_list = list_of_groups(s1_filter1, 150) #时间窗为150
    count = int(len(s1_filter1) / 150)  # 有300个采样点
    for i in range(0, count):
        s1_feature.append(psfeatureTime(np.array(s1_list[i])))#每一个采样点计算特征值
    s1_label = []
    for i in range(count):
        s1_label.append((i%3)+1)#加label
    features = np.array(s1_feature)
    labels = np.array(s1_label)
    #print(labels)
    train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.33, random_state=0)#划分训练集和测试集
    test_predict = []
    for i in range(len(test_labels)):#测试集的结果
        X = knn(train_features, test_features[i], train_labels, 5)
        test_predict.append(X)
    confus_matri = confusion_matrix(test_predict, test_labels)
    print("混淆矩阵为：\n",confus_matri)#输出混淆矩阵
    acc=(confus_matri[0,0]+confus_matri[1,1]+confus_matri[2,2])/sum(map(sum,confus_matri))#计算ACC
    print("准确率为：%.4lf\n" %acc)
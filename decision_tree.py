# -*- coding: utf-8 -*-     支持文件中出现中文字符
#####################################################################
import random
import numpy as np
import pandas as pd
from scipy import signal
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
import graphviz

def  psfeatureTime(data):#计算特征,随机加label
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
    s1_label = []
    for i in range(count):
        s1_label.append((i+1)%3)
    features = np.array(s1_feature)
    labels = np.array(s1_label)
    #print(labels)
    train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.33, random_state=1)
    clf = DecisionTreeClassifier(criterion='gini')
    clf = clf.fit(train_features, train_labels)
    dot_data = tree.export_graphviz(clf, out_file=None,
                         feature_names=["均值","偏度","峰度","峰值因子","裕度因子","峭度"],
                         class_names=["1","2","3"],
                         filled=True, rounded=True,
                         special_characters=True)
    graph = graphviz.Source(dot_data)
    graph.render("decision tree")

    test_predict = clf.predict(test_features)
    score = accuracy_score(test_labels, test_predict)
    print("分类树准确率 %.4lf" % score)
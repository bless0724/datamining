# -*- coding: utf-8 -*-     支持文件中出现中文字符
#####################################################################
import numpy as np
import pandas as pd
from scipy import signal
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
class K_Means(object):
    #初始化kmeans
    def __init__(self, k=2, tolerance=0.0001, max_iter=300):
        self.k_ = k #簇的数量
        self.tolerance_ = tolerance #中心点误差
        self.max_iter_ = max_iter #最大迭代次数

    #训练数据
    def fit(self, data):
        self.centers_ = {}
        # 首先取前k个数据作为质心
        for i in range(self.k_):
            self.centers_[i] = data[i]
        # 迭代
        for i in range(self.max_iter_):
            self.clf_ = {}
            for i in range(self.k_):
                self.clf_[i] = []
            for feature in data:
                distances =[]
                for center in self.centers_:
                    # 分别计算到k个质心的欧式距离
                    distances.append(np.linalg.norm(feature - self.centers_[center]))
                #距离最近的质心作为结果
                classification = distances.index(min(distances))
                #聚类
                self.clf_[classification].append(feature)

            #print("分组情况：",self.clf_)
            #记录当前质心
            prev_centers = dict(self.centers_)
            #更新质心
            for c in self.clf_:
                self.centers_[c] = np.average(self.clf_[c], axis=0)

            optimized = True
            for center in self.centers_:
                org_centers = prev_centers[center]
                cur_centers = self.centers_[center]
                #判断更新前后质心是否在误差范围中
                if np.sum((cur_centers - org_centers) / org_centers * 100.0) > self.tolerance_:
                    optimized = False
            if optimized:
                break

    def predict(self, p_data):
        distances = [np.linalg.norm(p_data - self.centers_[center]) for center in self.centers_]
        index = distances.index(min(distances))
        return index

    def cost(self, data):
        sum = 0
        for center in range(len(self.centers_)):
            for c in range(len(self.clf_[center])):
                sum += math.pow(np.linalg.norm(self.clf_[center][c] - self.centers_[center]),2)
        sum /= len(data)
        return sum

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
    features = np.array(s1_feature)

if __name__ == '__main__':
    k_means = K_Means(k=3)
    k_means.fit(features)
    #print(k_means.centers_)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    c = ['r','b','g']
    for center in k_means.centers_:
        ax.scatter(k_means.centers_[center][0], k_means.centers_[center][1], k_means.centers_[center][2], c = c[center], marker='*')

    for cat in k_means.clf_:
        for point in k_means.clf_[cat]:
            ax.scatter(point[0], point[1], point[2], c=c[cat])
    cost = k_means.cost(features)
    print("代价为：",cost)
    plt.show()
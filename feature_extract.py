from scipy import signal
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

def list_of_groups(list_info, per_list_len):#划分数据
    '''
    :param list_info:   列表
    :param per_list_len:  每个小列表的长度
    :return:
    '''
    list_of_group = zip(*(iter(list_info),) *per_list_len)
    end_list = [list(i) for i in list_of_group] # i is a tuple
    count = len(list_info) % per_list_len
    end_list.append(list_info[-count:]) if count != 0 else end_list
    return end_list

def notch_filter(data):#陷波滤波器
    fs = 100.0#采样频率
    f0 = 50.0#要滤掉50hz频率
    Q = 30.0#质量因子
    w0 = f0/(fs/2)
    #设计notch filter
    b, a = signal.iirnotch(w0,Q)
    data_notch = signal.filtfilt(b,a,data)
    return data_notch

def band_filter(data):#带通滤波器
    fs = 100.0
    lowcut = 1.0
    highcut = 30.0
    order = 2
    low = lowcut/(fs/2)
    high = highcut/(fs/2)
    #设计band filter
    b, a = signal.butter(order, [low,high], btype='band')
    data_band = signal.filtfilt(b, a, data)
    return data_band

def zero_crossing(data_segment):
    zc = 0
    for i in range(len(data_segment)-1):
        if data_segment[i]*data_segment[i+1]<0:
            zc += 1
    return zc

def peak_to_peak(data_segment):
    max_peak = max(data_segment)
    min_peak = min(data_segment)
    p2p = max_peak-min_peak
    return p2p

def feature_extract(data_segment):#特征提取
    # Mean
    mean = data_segment.mean()
    # Variance
    std = data_segment.var()
    # Skewness
    skew = pd.Series(data_segment).skew()
    # Kurtosis
    kurt = pd.Series(data_segment).kurt()
    # Zero crossing
    zc = zero_crossing(data_segment)
    # Peak to Peak
    p2p = peak_to_peak(data_segment)
    feature_list = [mean, std, skew, kurt, zc, p2p]
    return feature_list

if __name__ == '__main__':
    #读取data文件
    raw_data = open('sc4002e0_data.txt').read()#设立raw_data列表变量，.read读文件
    raw_data = raw_data.split( )#用空格划分点
    raw_data = [float(s) for s in raw_data]#将列表raw_data中的数值强制转换为float类型
    raw_data = notch_filter(raw_data)#陷波滤波
    raw_data = band_filter(raw_data)#带通滤波
    data = list_of_groups(raw_data, 3000)#划分原数据，每3000个点作为一帧
    #提取特征
    f = open("sc4002e0_feature.txt", "w")
    for frame in data:
        feature = " ".join(str(i) for i in feature_extract(np.array(frame)))
        f.write(feature+'\n')
    f.close()

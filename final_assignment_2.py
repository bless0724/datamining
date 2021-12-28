import numpy as np
from sklearn import metrics
from sklearn.decomposition import PCA
import sklearn.cluster as skc
import pandas as pd
import matplotlib.pyplot as plt

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

if __name__ =="__main__":
    #读特征
    features = open("sc4002e0_feature.txt").read()
    features = features.split( )#用空格划分点
    features = [float(s) for s in features]
    features = np.array(list_of_groups(features, 6))

    #用PCA降维
    pca = PCA(n_components=4)
    new_features = pca.fit_transform(features)
    new_features = pd.DataFrame(new_features)

    # 用DBSCAN聚类
    #db = skc.DBSCAN(eps=10, min_samples=33).fit(new_features)  # DBSCAN聚类方法,eps为距离，min_samples为样本数阈值
    db = skc.KMeans(n_clusters=7, random_state=9).fit(features)
    labels = db.labels_
    print(labels)

    #可视化
    x = np.array(new_features.iloc[:, 0])
    y = np.array(new_features.iloc[:, 1])
    #预测数据
    plt.subplot(1,1,1)
    plt.scatter(x, y, c=np.array(labels))
    plt.show()

    # # label==-1的是噪声
    # ratio = len(labels[labels[:] == -1]) / len(labels)  # 计算噪声点个数占总数的比例
    # print('噪声比:', format(ratio, '.2%'))
    # # 得到簇数
    # n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)  # 获取分簇的数目
    # print('分簇的数目: %d' % n_clusters_)
    # print('Silhouette Coefficient: %0.3f' % metrics.silhouette_score(new_features, labels))
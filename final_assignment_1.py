import operator
import numpy as np
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

def knn(trainData, testData, labels, k):#train是训练数据，test是测试数据，labels
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
    matrix = np.zeros((7,7)).astype('int64')
    for i in range(len(predict)):
        x = int(predict[i])-1
        y = int(real[i])-1
        matrix[x][y] += 1
    return matrix

if __name__ =="__main__":
    #读特征
    features = open("sc4002e0_feature.txt").read()
    features = features.split( )#用空格划分点
    features = [float(s) for s in features]
    features = np.array(list_of_groups(features, 6))
    #读标签
    labels = open("sc4002e0_label.txt").read()
    labels = labels.split( )
    labels = [int(float(s)) for s in labels]
    labels = np.array(labels)
    #划分训练集测试集
    train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.33,
                                                                                random_state=0)
    test_predict = []
    for i in range(len(test_labels)):
        X = knn(train_features, test_features[i], train_labels, 5)
        test_predict.append(X)
    confus_matri = confusion_matrix(test_predict, test_labels)
    print("混淆矩阵为：\n", confus_matri)#输出混淆矩阵
    positive = 0
    for i in range(7):
        positive+=confus_matri[i,i]
    acc = positive/sum(map(sum,confus_matri))#计算ACC
    print("准确率为：%.4lf\n" %acc)
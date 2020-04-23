# -*- coding: utf-8 -*-
from sklearn import metrics
import numpy as np

'''
    测nmi
'''


def open_file(file):
    tWardp = []
    with open(file, 'r') as f:
        data = f.readlines()
        # 计算节点规模
        for row in data:
            # 初始化
            tWardp.extend(row.strip().split(' '))
        for index, row in enumerate(data):
            line = row.strip().split(' ')
            for i in line:
                j = int(i) - 1
                tWardp[int(j)] = index
    return np.array(tWardp)


def com_nmi(community_path, real_community_path):
    A = open_file(real_community_path)
    B = open_file(community_path)
    result_NMI = metrics.normalized_mutual_info_score(A, B)
    return result_NMI


if __name__ == '__main__':
    community_path = '../../data/artificial/lpaoml_am_network0.4_0.2k_community.txt'
    real_community_path = '../../data/artificial/real_community0.4_0.2k.txt'
    print(com_nmi(community_path, real_community_path))

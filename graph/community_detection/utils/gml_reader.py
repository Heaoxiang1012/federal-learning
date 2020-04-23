# -*- coding: utf-8 -*-
import networkx as nx
import copy


# 抽取txt中的数据
def read_txt(data):
    g = nx.read_edgelist("data", create_using=nx.DiGraph())
    print(g.edges())


# 抽取gml中的数据
# networkx可以直接通过函数从gml文件中读出数据
def read_gml(data):
    G = nx.read_gml(data)
    nodes = []
    edges = []
    nodes_id = dict()
    nodes_label = dict()
    edges_id = []
    for id, label in enumerate(G.nodes()):
        nodes_id[label] = id
        nodes_label[id] = label
        nodes.append(id)
    for (v0, v1) in G.edges():
        print(v1)
        temp = [nodes_id[v0], nodes_id[v1]]
        edges.append(temp)
    edges_id = copy.deepcopy(edges)
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G, nodes_id, edges_id, nodes_label


# 保存子图边集
def save(data, file_name):
    f = open(file_name, 'w')
    temp = ''
    for item in data:
        temp += str(item[0]) + ' ' + str(item[1])
        temp += '\n'
    f.write(temp)
    f.close()


if __name__ == "__main__":
    G, nodes_id, edges_id, nodes_label = read_gml('../../data/genuine/celegansneural.gml')
    print(edges_id)
    save(edges_id, '../../data/genuine/celegansneural.txt')

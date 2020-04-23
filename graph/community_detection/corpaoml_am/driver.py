'''
@Time    : 2020/03/30 21:00
@Author  : hax
'''

import networkx as nx
import time
import operator
import collections
import random

from graph.community_detection.corpaoml_am.coordinator import coordinator
from graph.community_detection.corpaoml_am.guest import guest
from graph.community_detection.corpaoml_am.host import host
from statistics.intersect.driver import Intersect

class driver:

    # create graph
    @staticmethod
    def read_graph(edge_path):
        G = nx.read_edgelist(edge_path)
        for node ,data in G.nodes(True):
            dict_list = []
            sub_dict = {'community':node , 'weight':1.0}
            dict_list.append(sub_dict)
            data['label'] = dict_list

        return G

    @staticmethod
    def get_intersect_ids(G1,G2):
        node1_list = G1.nodes()
        node2_list = G2.nodes()

        intersect = Intersect()
        intersect_ids = intersect.run(node1_list, node2_list)

        intersect_ids = [int(x) for x in intersect_ids]

        return intersect_ids



    def run(self,G1,G2,G3,G4,v,save_path):
        begin_time = time.time()
        all_list = []
        for item in G1,G2,G3,G4:
            each_list = []
            for g_item in G1,G2,G3,G4:
                intersect_ids = []
                if item != g_item :
                    intersect_ids = self.get_intersect_ids(item,g_item)
                each_list.append(intersect_ids)
            all_list.append(each_list)

        end_time = time.time()
        id_match_time = (end_time - begin_time)  # 获取交集顶点时间

        Com = []

        h = 0
        j = 0

        total_num = len(G1) + len(G2) + len(G3) + len(G4)

        encrypt_time = 0
        decrypt_time = 0
        update_time = 0
        update_num = 0

        for iitem in G1,G2,G3,G4:
            item = iitem
            for gg_item in G1,G2,G3,G4:
                g_item = gg_item
                if item == g_item :
                    j += 1
                    continue

                intersect_ids = all_list[h][j]

                node_num = total_num - len(intersect_ids) # 原图的顶点个数

                _host = host(node_num)
                _guest = guest(_host.get_paillier_public_key(), _host.get_paillier_private_key(),node_num)
                _coordinator = coordinator(node_num)

                forward = []  # 保存前向每个社区的节点数
                iterate_times = 0  # count of iterating

                while True: # 迭代更新标签
                    backward = [] # 保存后向每个社区的节点数
                    iterate_times += 1

                    _host_label_dict = _host.get_label_dict(item)
                    _guest_label_dict = _guest.get_label_dict(g_item)


                    _host_intersect_dict = _host.get_intersect_dict(_host_label_dict,intersect_ids)

                    _guest_intersect_dict = _guest.get_intersect_dict(_guest_label_dict,intersect_ids)


                    _host_intersect_dict, _host_encrypt_time = _host.send_intersect_dict(_host_intersect_dict)

                    _guest_intersect_dict, _guest_encrypt_time = _guest.send_intersect_dict(_guest_intersect_dict)


                    intersect_dict = _coordinator.send_intersect_dict(_host_intersect_dict, _guest_intersect_dict)

                    _host_decrypt_time, _host_intersect_up_time, _host_intersect_up_num = \
                        _host.update_intersect_nodes(item, intersect_dict,v)

                    _host_remain_up_time, _host_remain_up_num = \
                    _host.update_remain_nodes(item, _host_label_dict, intersect_ids, v)

                    _host_up_time = (_host_intersect_up_time + _host_remain_up_time)  # 累加更新时间
                    _host_up_num = (_host_intersect_up_num + _host_remain_up_num)  # 累加更新标签个数

                    _guest_decrypt_time, _guest_intersect_up_time, _guest_intersect_up_num = \
                        _guest.update_intersect_nodes(g_item, intersect_dict, v)
                    _guest_remain_up_time, _guest_remain_up_num = \
                        _guest.update_remain_nodes(g_item, _guest_label_dict, intersect_ids, v)
                    _guest_up_time = (_guest_intersect_up_time + _guest_remain_up_time)  # 更新时间
                    _guest_up_num = (_guest_intersect_up_num + _guest_remain_up_num)  # 更新标签个数

                    encrypt_time += (_host_encrypt_time + _guest_encrypt_time )  # 累加加密时间
                    decrypt_time += (_host_decrypt_time + _guest_decrypt_time )  # 累加解密时间
                    update_time += (_host_up_time + _guest_up_time )  # 累加标签更新时间
                    update_num += (_host_up_num + _guest_up_num )  # 累加更新标签数量

                    communities = _coordinator.get_communities(item, g_item)
                    for i in communities:
                        backward.append(len(i))
                    if operator.eq(backward, forward) or iterate_times > 30:
                        com = _coordinator.get_com_dict(item,g_item)
                        Com.append(com)
                        print('community_num ： ', len(backward))
                        break
                    else :
                        forward = backward.copy()
                #_coordinator.save_communities(communities,save_path)

                item = iitem
            h += 1

        backward = []
        communities = coordinator.get_final_communities(Com,v)

        for i in communities:
            backward.append(len(i))
        print('final community_num ： ', len(backward))

        #print('iterate_times ： ', iterate_times)
        print('id_match_time ：', id_match_time)
        print('encryption_time ：', encrypt_time)
        print('decryption_time ：', decrypt_time)
        print('update_time:', update_time)
        print('update_num:', update_num)

        coordinator.save_communities(communities,save_path)














'''
@Time    : 2020/03/30 21:00
@Author  : hax
'''
import collections
import random
class coordinator:

    def __init__(self, num):
        self.num = num  # 原图顶点数量

    #???
    def send_intersect_dict(self, intersect_host_dict, intersect_guest_dict):
        """
         # 分组求和
        :param num:
        :param intersect_host_dict:
        :param intersect_guest_dict:
        :return: 求和之后的交集字典
        """
        intersect_dict = []
        for host_item in intersect_host_dict[:]:
            host_item_node = host_item['node']
            host_item_label_weight = host_item['label_weight']
            for guest_item in intersect_guest_dict[:]:
                guest_item_node = guest_item['node']
                guest_item_label_weight = guest_item['label_weight']
                if host_item_node == guest_item_node:
                    intersect_item_label_weight = [guest_item_label_weight[i] + host_item_label_weight[i] for i in
                                                   range(0, self.num)]  # 同类标签数量相加
                    item_intersect_dict = {'node': host_item_node, 'label_weight': intersect_item_label_weight}
                    intersect_dict.append(item_intersect_dict)
                    break
        print("coordinator send message to host ...")
        print("coordinator send message to guest ...")
        return intersect_dict

    @staticmethod
    def get_communities(G1, G2):
        """
        合并社区
        :param G1:
        :param G2:
        :return:
        """
        ids = []
        communities = collections.defaultdict(lambda: list())
        for node in G1.nodes(True):
            label_dict = node[1]["label"]
            for item in label_dict:
                community = item['community']
                weight = item['weight']
                communities[community].append(node[0])
        for node in G2.nodes(True):
            label_dict = node[1]["label"]
            for item in label_dict:
                community = item['community']
                weight = item['weight']
                communities[community].append(node[0])
        #print('communities', communities)
        for i in communities.values():
            id = list(set(i))  # 去重是因为把交集算了一遍
            ids.append(id)
        return ids

    def get_com_dict(self,G1,G2):
        com = {}
        for node in G1.nodes(True):
            label = node[1]['label']
            com.update({node[0]:label})
        for node in G2.nodes(True):
            label = node[1]['label']
            com.update({node[0]: label})
        return com

    @staticmethod
    def get_final_communities(communities__dict, v):
        com = {}
        ids = []
        for communities in communities__dict:
            for node, label in communities.items():
                com[node] = {}
                if node in com:
                    for item in label:
                        l = item['community']
                        s = item['weight']
                        if l in com[node]:
                            com[node][l] += s
                        else:
                            com[node][l] = s
                else:
                    com[node] = label


        for node, label in com.items():
            sum_ = sum(label.values())
            for x,y in list(label.items()):
                label.update({x: y / sum_})
            maxc = max(label.values())

            a = 0
            for key in label:
                if maxc == label[key] :
                    a = key
            if maxc < 1 / float(v):
                label.clear()
                m = random.choice(a)
                label[m] = 1
            else:
                for x,y in list(label.items()):
                    if y < 1 / float(v):
                        label.pop(x)

        communities = collections.defaultdict(lambda: list())
        for node, label in com.items():
            for item in label:
                i = item
                communities[i].append(node)

        for i in communities.values():
            id = list(set(i))
            ids.append(id)
        print(ids)
        return ids


    @staticmethod
    def save_communities(communities, save_path):
        """
        保存社区
        :param communities:
        :param save_path:
        :return:
        """
        output_file = open(save_path, 'w')
        for cmu in communities:
            for member in cmu:
                output_file.write(member + " ")
            output_file.write("\n")
        output_file.close()
        return


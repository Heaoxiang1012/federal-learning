import collections
import random
import time

import networkx as nx

# t1 = datetime.datetime.now().microsecond
# t3 = time.mktime(datetime.datetime.now().timetuple())


'''
paper : <<Near linear time algorithm to detect community structures in large-scale networks>>
'''

begin_time = time.clock()


class LPA():

    def __init__(self, G, max_iter=20):
        self._G = G
        self._n = len(G.nodes)  # number of nodes
        self._max_iter = max_iter

    def can_stop(self):
        # all node has the label same with its most neighbor
        for i in list(self._G.nodes):
            node = self._G.nodes[i]
            label = node["label"]
            max_labels = self.get_max_neighbor_label(i)
            if (label not in max_labels):
                return False
        return True

    def get_max_neighbor_label(self, node_index):
        m = collections.defaultdict(int)
        for neighbor_index in self._G.neighbors(node_index):
            neighbor_label = self._G.nodes[neighbor_index]["label"]
            m[neighbor_label] += 1
        max_v = max(m.values())
        return [item[0] for item in m.items() if item[1] == max_v]

    '''asynchronous update'''

    def populate_label(self):
        # random visit
        visitSequence = random.sample(self._G.nodes(), len(self._G.nodes()))
        for i in visitSequence:
            node = self._G.nodes[i]
            label = node["label"]
            max_labels = self.get_max_neighbor_label(i)
            if (label not in max_labels):
                newLabel = random.choice(max_labels)
                node["label"] = newLabel

    def get_communities(self):
        communities = collections.defaultdict(lambda: list())
        for node in self._G.nodes(True):
            label = node[1]["label"]
            communities[label].append(node[0])
        # print(communities.values())
        return communities.values()

    def execute(self):
        iter_time = 0
        # populate label
        while (not self.can_stop() and iter_time < self._max_iter):
            self.populate_label()
            iter_time += 1
        return self.get_communities()


def read_graph_from_file(path):
    # read edge-list from file
    graph = nx.read_edgelist(path)

    # initial graph node's attribute 'label' with its id
    for node, data in graph.nodes(True):
        data['label'] = node

    return graph


def print_communities_to_file(communities, output_path):
    output_file = open(output_path, 'w')
    for cmu in communities:
        for member in cmu:
            output_file.write(member + " ")
        output_file.write("\n")
    output_file.close()
    return


paths = [
    ["../../data/genuine/jazz.txt",
     "../../data/genuine/std_lpa_jazz_community.txt"],
]

for path in paths:
    input_file_path, output_file_path = path

    G = read_graph_from_file(input_file_path)
    algorithm = LPA(G)
    communities = algorithm.execute()
    '''
    for community in communities:
        print (" ".join(str(i) for i in community))
    '''

    print_communities_to_file(communities, output_file_path)
    print(output_file_path + " done communities: " + str(len(communities)))
    # t2 = datetime.datetime.now().microsecond
    # t4 = time.mktime(datetime.datetime.now().timetuple())
    # strTime = 'funtion time use:%dms' % ((t4 - t3) * 1000 + (t2 - t1) / 1000)
    # print(strTime)
    end_time = time.clock()
    print(end_time - begin_time)


import unittest
import networkx as nx
import matplotlib.pyplot as plt
from graph.community_detection.corpaoml_am.driver import driver
from graph.community_detection.utils import overlapping_modularity

#path = '../../corpa/genuine/karate.txt'


class TestDriver(unittest.TestCase):
    def test(self):
        res = []
        app = driver()
        path = '../../../multiparty/artificial/n/4/network0.4_1k.txt'
        path0 = '../../../multiparty/artificial/n/4/network0.4_1k_0.txt'
        path1 = '../../../multiparty/artificial/n/4/network0.4_1k_1.txt'
        path2 = '../../../multiparty/artificial/n/4/network0.4_1k_2.txt'
        path3 = '../../../multiparty/artificial/n/4/network0.4_1k_3.txt'

        save_path = '../../../results.txt'

        v = 2 #比较权重
        G = nx.read_edgelist(path)
        G1 = app.read_graph(path0)
        G2 = app.read_graph(path1)
        G3 = app.read_graph(path2)
        G4 = app.read_graph(path3)

        app.run(G1,G2,G3,G4,v,save_path)


        com = overlapping_modularity.load_corpa(save_path)
        mod = overlapping_modularity.cal_EQ(com, G)
        res.append(mod)

        print(res)
        print(sum(res) / len(res))


if __name__ == '__main__':
    unittest.main()
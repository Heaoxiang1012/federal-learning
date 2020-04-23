import networkx as nx

'''
测非重叠社区模块度
'''
def cal_Q(partition, G):
    m = len(G.edges(None, False))
    a = []
    e = []

    for community in partition:
        t = 0.0
        for node in community:
            t += len(list(G.neighbors(node)))
        a.append(t / (2 * m))

    for community in partition:
        # print(community)
        community = list(community)
        t = 0.0
        for i in range(len(list(community))):
            for j in range(len(list(community))):
                if (G.has_edge(community[i], community[j])):
                    t += 1.0
        e.append(t / (2 * m))
    q = 0.0
    for ei, ai in zip(e, a):
        q += (ei - ai ** 2)
    return q


def load_data(path):
    com = []
    with open(path, "r") as f:
        for line in f.readlines():
            a = []
            j = 0
            line = line.strip('\n')
            arr = line.split(' ')
            for i in arr:
                if j == len(arr) - 1:
                    break
                j += 1
                a.append(i)
            com.append(a)
        f.close()
        return com


if __name__ == "__main__":
    G = nx.read_edgelist('../../data/genuine/karate.txt')
    com = load_data('../../data/genuine/lpaoml_am_karate_community.txt')
    mod = cal_Q(com, G)
    print(mod)

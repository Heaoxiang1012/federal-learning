# -*- encoding:utf-8 -*-
'''
社区格式化
'''
# path = "input/community_t1.txt"
path = "../../data/mu/community1k-mu0.5.txt"

fileContent = open(path, "rb")
community_sets = {}

with fileContent as f:
    for row in f:
        row = row.decode()
        n, c = row.split("\t", -1)

        c = c.split(" ", -1)
        for cn in c:
            if cn == "\r\n":
                break
            n, cn = int(n), int(cn)
            if cn not in community_sets.keys():
                community = []
                community.append(n)
                community_sets[cn] = community
            else:
                community_sets[cn].append(n)

outputFilePath = "../../data/mu/real_community1k-mu0.5.txt"

outFile = open(outputFilePath, "w")

for num, com in community_sets.items():
    line = " ".join(str(i) for i in sorted(com)) + "\n"
    outFile.write(line)

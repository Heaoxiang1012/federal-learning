import csv


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
    csv_file = csv.reader(open('../../data/genuine/Untitled.csv', 'r'))
    print(csv_file)  # 可以先输出看一下该文件是什么样的类型
    edges_id = []
    for item in csv_file:
        print(item)
        temp = [int(item[0]), int(item[1])]
        edges_id.append(temp)
    save(edges_id, '../../data/genuine/netscience.txt')

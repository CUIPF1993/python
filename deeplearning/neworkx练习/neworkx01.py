import networkx as nx       #导入networkx包
#1.0无向图
G = nx.Graph()      #创建一个空的无向图
G.add_node(1)       #添加节点1
G.add_edge(2,3)     #添加一条边2——3，
G.add_edge(3,2)     #添加一条边3——2，在无向图中，上下两处相同

print(G.nodes())        #[1, 2, 3]
print(G.edges())        #[(2, 3)]
print(G.number_of_nodes())      #3
print(G.number_of_edges())      #1

#2.0有向图
G = nx.DiGraph()        ##创建一个空的有向图向图
G.add_edge(2,3)     #添加一条边2——3，
G.add_edge(3,2)     #添加一条边3——2，在有向图中，上下两处不同  

#有向图图和无向图可以相互装换
G.to_undirected()       #将有向图装换为无向图
G.to_directed()         #将有向图装换为有向图

#3.0加权图（网络）
G.add_weighted_edges_from([(0,1,3.0),(1,2,7.5)])
#添加0-1和1-2两条边，权重分别是3.0和7.5。

print(G.get_edge_data(1,2))     #{'weight': 7.5}
print(G[1][2])      #{'weight': 7.5}
print(G[1])     #{2: {'weight': 7.5}}

#4.0调用图算法
path = nx.all_pairs_shortest_path(G)
#调用最短路径算法，计算图G中所有的节点的最小路径
print(path)     #路径以字典形式存储
'''
{0: {0: [0], 1: [0, 1], 2: [0, 1, 2], 3: [0, 1, 2, 3]}, 
 1: {1: [1], 2: [1, 2], 3: [1, 2, 3]}, 2: {2: [2], 3: [2, 3]},
 3: {2: [3, 2], 3: [3]}}
 '''
print(path[0][3])       #[0, 1, 2, 3]

path = nx.all_pairs_dijkstra_path(G)        #调用dijkstra算法
print(path)
'''
{0: {0: [0], 1: [0, 1], 2: [0, 1, 2], 3: [0, 1, 2, 3]}, 
 1: {1: [1], 2: [1, 2], 3: [1, 2, 3]}, 2: {2: [2], 3: [2, 3]},
 3: {2: [3, 2], 3: [3]}}
 '''




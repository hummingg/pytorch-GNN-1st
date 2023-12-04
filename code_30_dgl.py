import dgl
import matplotlib.pyplot as plt
import torch as th
import networkx as nx

g = dgl.DGLGraph(([0, 1, 1, 2], [1, 2, 3, 3]))
# g = dgl.DGLGraph()
# g.add_nodes(4)
# g.add_edges([0, 1, 1, 2], [1, 2, 3, 3])
g.ndata['x'] = th.tensor([[1.], [2.], [3.], [4.]])
print(g.ndata['x'])

plt.figure(figsize=(20, 6))
# plt.subplot(121)
plt.title('Networkx', fontsize=20)
nx.draw(g.to_networkx(), with_labels=True)
plt.show()

def send_source(edges):
    return {'m': edges.src['x']}

# g.update_all(send_source)

def simple_reduce(nodes):
    return {'x': nodes.mailbox['m'].sum(1)}

# [[0.], [1.], [2.], [5.]]
g.update_all(message_func=send_source, reduce_func=simple_reduce)
print(g.ndata['x'])

# 第一个参数是迭代器
# step1: [1, 2]中2个顶点同时收集邻居信息并更新自己
# step2: [3]中1个顶点收集邻居信息并更新自己，会收集到step1更新后的[1, 2]
# g.prop_nodes([[1, 2], [3]], message_func=send_source, reduce_func=simple_reduce)
# # [[1.], [1.], [2.], [3.]]
# print(g.ndata['x'])


# 多图：重复边或关系不同(异构图)
g_multi = dgl.DGLGraph(multigraph=True)
g_multi.add_nodes(4)
g_multi.add_edges(list(range(2)), 0)
# 重复边
g_multi.add_edge(1, 0)
# (tensor([0, 1, 1]), tensor([0, 0, 0]))
print(g_multi.edges())
# eid_1_0 = g_multi.edge_id(1, 0)
# 1
# print(eid_1_0)
eid_1_0 = g_multi.edge_ids(1, 0, return_uv=True)
# (tensor([1, 1]), tensor([0, 0]), tensor([1, 2])) = (eu, ev, eid)
# 1->0 = 1, 1->0 = 2
print(eid_1_0)



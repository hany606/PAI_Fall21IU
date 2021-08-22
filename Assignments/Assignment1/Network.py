# References: 
# https://www.datacamp.com/community/tutorials/networkx-python-graph-tutorial
# https://networkx.org/documentation/stable/auto_examples/drawing/plot_labels_and_colors.html

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
# from math import log10, ceil
# from copy import deepcopy

class Network:
    def __init__(self, width, height, node_size=None):
        self.G = nx.Graph()
        self.DGs = {"blue":nx.DiGraph(), "red":nx.DiGraph()}
        self.node_size = node_size if node_size is not None else min(width, height)//2
        self.width = width
        self.height = height
        plt.close("all")
        fig = plt.figure(figsize=(8,8))

    def create_grid(self):
        ax = plt.gca()
        
        ax.grid(True, which='both')
        ax.yaxis.tick_left()
        ax.tick_params(
            axis="both",
            which="both",
            bottom=False,
            left=False,
            labelbottom=True,
            labelleft=True,
        )
        ax.set_xticks([i for i in range(self.width)])
        ax.set_yticks([i for i in range(self.height)])



        # for i in range(self.width):
        #     ax.plot([i, i], [-1, self.height+1], 'k', linewidth=0.7)
        #     # self.add_node(i, -1, "boarders", "green")
        #     # self.add_node(i, self.height+1, "boarders", "green")
        #     # self.add_edge(i,-1, i, self.height+1, "green")
        # for i in range(self.height):
        #     ax.plot([-1, self.width+1], [i, i], 'k', linewidth=0.7)
        #     # self.add_node(-1, i, "boarders", "green")
        #     # self.add_node(self.width+1, i, "boarders", "green")
        #     # self.add_edge(-1, i, self.width+1, i, "green")
    
    def create_boarders(self):
        ax = plt.gca()
        ax.plot([-1, -1], [-1, self.height+1], 'k', linewidth=0.7)
        ax.plot([-1, self.height+1], [self.width+1, self.height+1], 'k', linewidth=0.7)
        ax.plot([self.width+1, self.height+1], [self.width+1, -1], 'k', linewidth=0.7)
        ax.plot([self.width+1, -1], [-1, -1], 'k', linewidth=0.7)
        

        # self.add_node(-1, -1, "boarders", "green")
        # self.add_node(-1, self.height+1, "boarders", "green")
        # self.add_node(self.width+1, self.height+1, "boarders", "green")
        # self.add_node(self.width+1, -1, "boarders", "green")

        # self.add_edge(-1,-1, -1, self.height+1, "green")
        # self.add_edge(self.width+1, self.height+1, -1, self.height+1, "green")
        # self.add_edge(self.width+1, self.height+1, self.width+1, -1, "green")
        # self.add_edge(self.width+1, -1, -1, -1, "green")

    def create_axis_text(self):
        pass

    def get_id(self, x, y):
        return f"{x},{y}" #(str(x)+str(y)) -> 11 2 == 1 12
        # print(x,y)
        # x += 1
        # y += 1
        # return (x*(10**ceil(log10(y)))+y)

    def add_node(self, x, y, agent, color):
        self.G.add_nodes_from([(self.get_id(x,y), {"color": color, "X":x, "Y":y, "agent": agent})])

    def add_edge(self, x1,y1, x2,y2, agent, color):
        node1_id = self.get_id(x1, y1)
        node2_id = self.get_id(x2, y2)
        self.G.add_edges_from([(node1_id, node2_id, {"color":color, "agent":agent})])
        self.DGs[agent].add_edges_from([(node1_id, node2_id)])

    def modify_node(self, x, y, agent, color):
        node_id = self.get_id(x,y)
        for node in self.G.nodes(data=True):
            if(node[0] == node_id):
                deleted_edges = []
                for edge in self.G.edges(data=True):
                    if(edge[0] == node_id or edge[1] == node_id):
                        deleted_edges.append(edge)
                self.G.remove_edges_from(deleted_edges)
                node[1]["agent"] = agent
                node[1]["color"] = color
                break

    def test_update(self):
        self.add_node(0,0, "red", "red")
        self.add_node(1,1, "red", "red")
        self.add_edge(0,0, 1,1, "red")

    def find_cycles(self, agent, node):
        # edges = []
        # for edge in self.G.edges(data=True):
        #     if(edge[2]["agent"] == agent):
        #         edges.append((edge[0], edge[1]))
        
        # print(node_positions)
        # edges = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 0), (2, 1), (2, 2)]#[(5, 5), (6, 5), (7, 5), (8, 5), (5, 9), (6, 9), (7, 9), (8, 9), (5, 6), (5, 7), (5, 8), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9)]
        # edges = node_positions
        # print(edges)
        # G = nx.DiGraph(edges)
        # copyG = self.G.copy()
        # copyG.remove_nodes_from([1])
        # copyG.remove_edges_from([(0, 1)])
        # len(list(nx.simple_cycles(copyG)))
        try:
            return list(nx.cycle_basis(self.DGs[agent].to_undirected()))
            # return list(nx.simple_cycles(G))
            # return list(nx.find_cycle(G, source=node, orientation="ignore"))
            # return list(nx.find_cycle(G, orientation="ignore"))
        except:
            return []
    
    def draw(self, timeout=0.0001):
        # for node in self.G.nodes(data=True):
        #     print(node)
        #     print(node[1]['X'])
        node_positions = {node[0]: (node[1]['X'], node[1]['Y']) for node in self.G.nodes(data=True)}
        node_colors = [f"tab:{node[1]['color']}" for node in self.G.nodes(data=True)]
        edge_colors = [f"tab:{edge[2]['color']}" for edge in self.G.edges(data=True)]
        nx.draw_networkx_nodes(self.G, pos=node_positions, node_color=node_colors, node_size=self.node_size)
        nx.draw_networkx_edges(self.G, pos=node_positions, edge_color=edge_colors, width=3)
        self.create_boarders()
        self.create_grid()

        # Source: https://stackoverflow.com/questions/4098131/how-to-update-a-plot-in-matplotlib
        if(timeout < 0):
            plt.show()
        else:
            plt.draw()
            plt.pause(timeout)
            plt.clf()



if __name__ == '__main__':
    n = Network()
    n.update()
    n.draw()

# import matplotlib.pyplot as plt
# import networkx as nx

# G = nx.cubical_graph()
# pos = nx.spring_layout(G, seed=3113794652)  # positions for all nodes
# print(pos)
# # nodes
# options = {"edgecolors": "tab:gray", "node_size": 800, "alpha": 0.9}
# nx.draw_networkx_nodes(G, pos, nodelist=[0, 1, 2, 3], node_color="tab:red", **options)
# nx.draw_networkx_nodes(G, pos, nodelist=[4, 5, 6, 7], node_color="tab:blue", **options)

# # edges
# nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
# nx.draw_networkx_edges(
#     G,
#     pos,
#     edgelist=[(0, 1), (1, 2), (2, 3), (3, 0)],
#     width=8,
#     alpha=0.5,
#     edge_color="tab:red",
# )
# nx.draw_networkx_edges(
#     G,
#     pos,
#     edgelist=[(4, 5), (5, 6), (6, 7), (7, 4)],
#     width=8,
#     alpha=0.5,
#     edge_color="tab:blue",
# )


# # some math labels
# labels = {}
# labels[0] = r"$a$"
# labels[1] = r"$b$"
# labels[2] = r"$c$"
# labels[3] = r"$d$"
# labels[4] = r"$\alpha$"
# labels[5] = r"$\beta$"
# labels[6] = r"$\gamma$"
# labels[7] = r"$\delta$"
# nx.draw_networkx_labels(G, pos, labels, font_size=22, font_color="whitesmoke")

# plt.tight_layout()
# plt.axis("off")
# plt.show()
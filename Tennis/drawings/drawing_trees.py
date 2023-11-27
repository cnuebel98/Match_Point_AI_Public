import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import pydot

T = nx.DiGraph()

T.add_node(0, weights=5, node_size=500, color='red')
T.add_node(1, weights=5, node_size=250, color='blue')
T.add_node(2, weights=5, node_size=250, color='blue')
T.add_node(3, weights=5, node_size=500, color='red')
T.add_node(4, weights=5, node_size=250, color='blue')
T.add_node(5, weights=5, node_size=250, color='blue')
T.add_node(6, weights=5, node_size=500, color='red')
T.add_node(7, weights=5, node_size=250, color='blue')
T.add_node(8, weights=5, node_size=250, color='blue')
T.add_node(9, weights=5, node_size=250, color='blue')
T.add_node(10, weights=5, node_size=500, color='red')
T.add_node(11, weights=5, node_size=250, color='blue')

T.add_edge(0, 1, color='black', weight=1.5, style='-')
T.add_edge(0, 2, color='black', weight=1.5, style='-')
T.add_edge(0, 3, color='red', weight=1.5, style='-')#
T.add_edge(1, 4, color='black', weight=1.5, style='-')
T.add_edge(1, 5, color='black', weight=1.5, style='-')
T.add_edge(3, 6, color='red', weight=1.5, style='-')#
T.add_edge(3, 7, color='black', weight=1.5, style='-')
T.add_edge(3, 8, color='black', weight=1.5, style='-')
T.add_edge(6, 9, color='black', weight=1.5, style='-')
T.add_edge(6, 10, color='red', weight=1.5, style='-')#
T.add_edge(0, 11, color='black', weight=1.5, style='-')

T.add_node(12, weights=5, node_size=500, color='red')
T.add_edge(10, 12, color='red', weight=1.5, style='-')

#T.add_node(13, weights=5, node_size=500, color=('red'))
#T.add_edge(12, 13, color='red', weight=2.5, style='dotted')

pos = graphviz_layout(T, prog="dot")
edges=T.edges()
nodes=T.nodes
colors = [T[u][v]['color'] for u,v in edges]
weights = [T[u][v]['weight'] for u,v in edges]
edge_style = [T[u][v]['style'] for u,v in edges]
node_sizes = list(nx.get_node_attributes(T,'node_size').values())
node_colors = list(nx.get_node_attributes(T, 'color').values())

nx.draw(T, pos, 
        edge_color=colors, 
        width=weights, 
        style=edge_style, 
        node_size=node_sizes,
        node_color=node_colors
        )
plt.show()
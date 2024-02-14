import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import pydot

T = nx.DiGraph()
node_size = 3000
T.add_node(0, weights=5, node_size=node_size, color='red', label="", label_color="black")
T.add_node(1, weights=5, node_size=node_size, color="#4B76FF", label="4", label_color="black")
T.add_node(4, weights=5, node_size=node_size, color='#48DB51', label="39e", label_color="black")
T.add_node(5, weights=5, node_size=node_size, color='#48DB51', label="18*", label_color="black")
T.add_node(3, weights=5, node_size=node_size, color='#4B76FF', label="5", label_color="black")
T.add_node(6, weights=5, node_size=node_size, color='#48DB51', label="18", label_color="black")
T.add_node(11, weights=5, node_size=node_size, color='#4B76FF', label="6e", label_color="black")
T.add_node(13, weights=5, node_size=node_size, color='#4B76FF', label="5", label_color="black")
T.add_node(14, weights=5, node_size=node_size, color='#48DB51', label="18*", label_color="black")
T.add_node(9, weights=5, node_size=node_size, color='#4B76FF', label="27*", label_color="black")
T.add_node(10, weights=5, node_size=node_size, color='#4B76FF', label="28", label_color="black")
T.add_node(12, weights=5, node_size=node_size, color='#48DB51', label="29*", label_color="black")
T.add_node(8, weights=5, node_size=4500, color='#48DB51', label="38", label_color="black")
T.add_node(15, weights=5, node_size=node_size, color='#4B76FF', label="37e", label_color="black")

T.add_node(16, weights=5, node_size=node_size, color='yellow', label="18", label_color="white")
T.add_node(17, weights=5, node_size=node_size, color='yellow', label="28", label_color="black")
T.add_node(18, weights=5, node_size=node_size, color='#BDFFC1', label="29", label_color="black")
T.add_node(19, weights=5, node_size=node_size, color='#BDFFC1', label="27", label_color="black")
T.add_node(20, weights=5, node_size=node_size, color='#BDFFC1', label="18", label_color="black")
T.add_node(21, weights=5, node_size=node_size, color='#BDFFC1', label="29e", label_color="black")
T.add_node(22, weights=5, node_size=node_size, color='lightskyblue', label="17", label_color="black")
T.add_node(23, weights=5, node_size=node_size, color='#BDFFC1', label="28", label_color="black")
T.add_node(24, weights=5, node_size=node_size, color='lightskyblue', label="19*", label_color="black")
T.add_node(25, weights=5, node_size=node_size, color='lightskyblue', label="28e", label_color="black")
T.add_node(26, weights=5, node_size=node_size, color='lightskyblue', label="38", label_color="black")
T.add_node(27, weights=5, node_size=node_size, color='#BDFFC1', label="27*", label_color="black")


weight = 5
T.add_edge(16, 18, color='black', weight=weight, style='-')
T.add_edge(16, 19, color='black', weight=weight, style='-')
T.add_edge(17, 20, color='black', weight=weight, style='-')
T.add_edge(17, 21, color='black', weight=weight, style='-')
T.add_edge(18, 22, color='black', weight=weight, style='-')
T.add_edge(19, 25, color='black', weight=weight, style='-')
T.add_edge(22, 23, color='black', weight=weight, style='-')
T.add_edge(23, 24, color='black', weight=weight, style='-')
T.add_edge(20, 26, color='black', weight=weight, style='-')
T.add_edge(26, 27, color='black', weight=weight, style='-')
T.add_edge(8, 17, color='black', weight=weight, style='-')
T.add_edge(6, 9, color='black', weight=weight, style='-')
T.add_edge(6, 10, color='black', weight=weight, style='-')
T.add_edge(0, 11, color='black', weight=weight, style='-')
T.add_edge(10, 12, color='black', weight=weight, style='-')
T.add_edge(13, 14, color='black', weight=weight, style='-')
T.add_edge(11, 13, color='black', weight=weight, style='-')
T.add_edge(8, 16, color='black', weight=weight, style='-')
T.add_edge(8, 15, color='black', weight=weight, style='-')
T.add_edge(3, 8, color='red', weight=weight, style='-')###########
T.add_edge(3, 6, color='black', weight=weight, style='-')
T.add_edge(0, 3, color='red', weight=weight, style='-')###########
T.add_edge(1, 5, color='black', weight=weight, style='-')
T.add_edge(1, 4, color='black', weight=weight, style='-')
T.add_edge(0, 1, color='black', weight=weight, style='-')

pos = graphviz_layout(T, prog="dot")
edges=T.edges()
nodes=T.nodes
colors = [T[u][v]['color'] for u,v in edges]
weights = [T[u][v]['weight'] for u,v in edges]
edge_style = [T[u][v]['style'] for u,v in edges]
node_sizes = list(nx.get_node_attributes(T,'node_size').values())
node_colors = list(nx.get_node_attributes(T, 'color').values())
labels=nx.get_node_attributes(T, 'label')

label_colors = list(nx.get_node_attributes(T,'label_color').values())



nx.draw(T, pos, 
        edge_color=colors, 
        width=weights, 
        style=edge_style, 
        node_size=node_sizes,
        node_color=node_colors,
        labels=labels,
        font_color="black",
        with_labels=True,
        font_size=25,
        font_weight='bold'
        )
plt.show()
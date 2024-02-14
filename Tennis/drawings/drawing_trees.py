import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout

def create_tree_1(title):
    T = nx.DiGraph()

    T.add_node(0, weights=5, node_size=3000, color='red', label="R")
    T.add_node(1, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(2, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(3, weights=5, node_size=3000, color='red', label="")
    T.add_node(4, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(5, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(6, weights=5, node_size=3000, color='red', label="")
    T.add_node(7, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(8, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(9, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(10, weights=5, node_size=3000, color='red', label="L")
    T.add_node(11, weights=5, node_size=3000, color='lightskyblue', label="")

    T.add_edge(0, 1, color='black', weight=5, style='-')
    T.add_edge(0, 2, color='black', weight=5, style='-')
    T.add_edge(0, 3, color='red', weight=5, style='-')#
    T.add_edge(1, 4, color='black', weight=5, style='-')
    T.add_edge(1, 5, color='black', weight=5, style='-')
    T.add_edge(3, 6, color='red', weight=5, style='-')#
    T.add_edge(3, 7, color='black', weight=5, style='-')
    T.add_edge(3, 8, color='black', weight=5, style='-')
    T.add_edge(6, 9, color='black', weight=5, style='-')
    T.add_edge(6, 10, color='red', weight=5, style='-')#
    T.add_edge(0, 11, color='black', weight=5, style='-')

    
    return T, title

def create_tree_2(title):
    T = nx.DiGraph()

    # Customize Tree 2 as needed
    T.add_node(0, weights=5, node_size=3000, color='lightskyblue', label="R")
    T.add_node(1, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(2, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(3, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(4, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(5, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(6, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(7, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(8, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(9, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(10, weights=5, node_size=3000, color='lightskyblue', label="L")
    T.add_node(11, weights=5, node_size=3000, color='lightskyblue', label="")

    T.add_edge(0, 1, color='black', weight=5, style='-')
    T.add_edge(0, 2, color='black', weight=5, style='-')
    T.add_edge(0, 3, color='red', weight=5, style='-')#
    T.add_edge(1, 4, color='black', weight=5, style='-')
    T.add_edge(1, 5, color='black', weight=5, style='-')
    T.add_edge(3, 6, color='red', weight=5, style='-')#
    T.add_edge(3, 7, color='black', weight=5, style='-')
    T.add_edge(3, 8, color='black', weight=5, style='-')
    T.add_edge(6, 9, color='black', weight=5, style='-')
    T.add_edge(6, 10, color='red', weight=5, style='-')#
    T.add_edge(0, 11, color='black', weight=5, style='-')

    T.add_node(12, weights=5, node_size=3000, color='red', label="E")
    T.add_edge(10, 12, color='red', weight=5, style='-')

    return T, title

def create_tree_3(title):
    T = nx.DiGraph()

    # Customize Tree 2 as needed
    T.add_node(0, weights=5, node_size=3000, color='lightskyblue', label="R")
    T.add_node(1, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(2, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(3, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(4, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(5, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(6, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(7, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(8, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(9, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(10, weights=5, node_size=3000, color='lightskyblue', label="L")
    T.add_node(11, weights=5, node_size=3000, color='lightskyblue', label="")

    T.add_edge(0, 1, color='black', weight=5, style='-')
    T.add_edge(0, 2, color='black', weight=5, style='-')
    T.add_edge(0, 3, color='red', weight=5, style='-')#
    T.add_edge(1, 4, color='black', weight=5, style='-')
    T.add_edge(1, 5, color='black', weight=5, style='-')
    T.add_edge(3, 6, color='red', weight=5, style='-')#
    T.add_edge(3, 7, color='black', weight=5, style='-')
    T.add_edge(3, 8, color='black', weight=5, style='-')
    T.add_edge(6, 9, color='black', weight=5, style='-')
    T.add_edge(6, 10, color='red', weight=5, style='-')#
    T.add_edge(0, 11, color='black', weight=5, style='-')

    T.add_node(12, weights=5, node_size=3000, color='lightskyblue', label="E")
    T.add_edge(10, 12, color='red', weight=5, style='-')

    T.add_node(13, weights=5, node_size=3000, color=('red'), label="T")
    T.add_edge(12, 13, color='red', weight=5, style='dotted')

    T.add_node(14, weights=5, node_size=3000, color=('red'), label="T")
    T.add_edge(12, 14, color='red', weight=5, style='dotted')

    return T, title

def create_tree_4(title):
    T = nx.DiGraph()

    # Customize Tree 2 as needed
    T.add_node(0, weights=5, node_size=3000, color='red', label="R")
    T.add_node(1, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(2, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(3, weights=5, node_size=3000, color='red', label="")
    T.add_node(4, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(5, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(6, weights=5, node_size=3000, color='red', label="")
    T.add_node(7, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(8, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(9, weights=5, node_size=3000, color='lightskyblue', label="")
    T.add_node(10, weights=5, node_size=3000, color='red', label="L")
    T.add_node(11, weights=5, node_size=3000, color='lightskyblue', label="")

    T.add_edge(0, 1, color='black', weight=5, style='-')
    T.add_edge(0, 2, color='black', weight=5, style='-')
    T.add_edge(0, 3, color='red', weight=5, style='-')#
    T.add_edge(1, 4, color='black', weight=5, style='-')
    T.add_edge(1, 5, color='black', weight=5, style='-')
    T.add_edge(3, 6, color='red', weight=5, style='-')#
    T.add_edge(3, 7, color='black', weight=5, style='-')
    T.add_edge(3, 8, color='black', weight=5, style='-')
    T.add_edge(6, 9, color='black', weight=5, style='-')
    T.add_edge(6, 10, color='red', weight=5, style='-')#
    T.add_edge(0, 11, color='black', weight=5, style='-')

    T.add_node(12, weights=5, node_size=3000, color='red', label="E")
    T.add_edge(10, 12, color='red', weight=5, style='-')

    return T, title

# Create four trees with titles
tree_1, title_1 = create_tree_1("1. Selection")
tree_2, title_2 = create_tree_2("2. Expansion")
tree_3, title_3 = create_tree_3("3. Simulation")
tree_4, title_4 = create_tree_4("4. Backpropagation")

trees = [(tree_1, title_1), (tree_2, title_2), (tree_3, title_3), (tree_4, title_4)]


fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Draw each tree in a subplot
for i, ((tree, title), ax) in enumerate(zip(trees, axes.flatten())):
    pos = graphviz_layout(tree, prog="dot")
    edges = tree.edges()
    node_sizes = list(nx.get_node_attributes(tree, 'node_size').values())
    node_colors = list(nx.get_node_attributes(tree, 'color').values())
    labels = nx.get_node_attributes(tree, 'label')
    colors = [tree[u][v]['color'] for u, v in edges]
    weights = [tree[u][v]['weight'] for u, v in edges]
    edge_style = [tree[u][v]['style'] for u, v in edges]
    
    ax.set_title(title, fontsize=40)
    nx.draw(tree, pos, 
            edge_color=colors, 
            width=weights, 
            style=edge_style, 
            node_size=node_sizes,
            node_color=node_colors,
            labels=labels,
            with_labels=True,
            font_size=40,
            font_weight='bold',
            ax=ax
            )


plt.tight_layout()
plt.show()

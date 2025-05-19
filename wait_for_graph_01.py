# wait_for_graph.py
import networkx as nx
import matplotlib.pyplot as plt

def build_wait_for_graph(allocation, request):
    """
    Builds a wait-for graph from Allocation and Request matrices.
    Returns a NetworkX DiGraph object.
    """
    n = len(allocation)  # Number of processes
    m = len(allocation[0])  # Number of resource types

    G = nx.DiGraph()

    for i in range(n):
        for j in range(m):
            if request[i][j] > 0:
                # Process i is requesting resource j
                for k in range(n):
                    if allocation[k][j] > 0:
                        G.add_edge(f"P{i}", f"P{k}")

    return G

def detect_cycle(graph):
    try:
        cycle = nx.find_cycle(graph, orientation='original')
        return True, cycle
    except nx.NetworkXNoCycle:
        return False, []

def visualize_graph(G, highlight_cycle=[]):
    pos = nx.circular_layout(G)
    plt.figure(figsize=(6, 6))
    edge_colors = ['red' if (u, v) in highlight_cycle else 'black' for u, v in G.edges()]
    
    nx.draw(G, pos, with_labels=True, node_color='lightblue',
            node_size=1500, font_weight='bold', edge_color=edge_colors)
    plt.title("Wait-For Graph")
    plt.show()

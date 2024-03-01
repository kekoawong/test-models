import networkx as nx
import random

def calculate_posterior(pH: float, pEH: float):
    pE = pEH * pH + (1 - pEH) * (1 - pH)
    return (pEH * pH) / pE

def initialize_graph(graphType: str, numNodes: int = 10):
    graph = nx.Graph()
    if graphType == 'circle':
        for index in range(numNodes):
            initial_data = {'group': index % 4, 'beliefProb': random.random(), 'pEH': None}
            graph.add_node(f"scientist-{index}", **initial_data)
            if index > 0:
                graph.add_edge(f"scientist-{index - 1}", f"scientist-{index}")
        graph.add_edge(f"scientist-{numNodes - 1}", "scientist-0")
    elif graphType == 'wheel':
        for index in range(numNodes - 1):
            initial_data = {'group': index % 4, 'beliefProb': random.random(), 'pEH': None}
            graph.add_node(f"scientist-{index}", **initial_data)
            if index > 0:
                graph.add_edge(f"scientist-{index - 1}", f"scientist-{index}")
        graph.add_edge(f"scientist-{numNodes - 2}", "scientist-0")
        graph.add_node(f"scientist-{numNodes - 1}", group=1, beliefProb=random.random(), pEH=None)
        for node in graph.nodes:
            if node != f"scientist-{numNodes - 1}":
                graph.add_edge(node, f"scientist-{numNodes - 1}")
    else:
        for index in range(numNodes):
            initial_data = {'group': index % 4, 'beliefProb': random.random(), 'pEH': None}
            graph.add_node(f"scientist-{index}", **initial_data)
        for i in range(numNodes):
            for j in range(i + 1, numNodes):
                if i != j:
                    graph.add_edge(f"scientist-{i}", f"scientist-{j}")
    return graph
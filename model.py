import networkx as nx
import matplotlib.pyplot as plt
import random
import statistics
from typing import Literal, Callable

def calculate_posterior(pH: float, pEH: float):
    pE = pEH * pH + (1 - pEH) * (1 - pH)
    return (pEH * pH) / pE

def initialize_graph(graphType: Literal['cycle', 'wheel', 'complete'], numNodes: int = 10):
    graph = nx.Graph()
    if graphType == 'cycle':
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

def run_experiment(worldState: Literal['new', 'old']):
    return random.uniform(0.3, 0.8) if worldState == 'new' else random.uniform(0.2, 0.7)

def timestep(graph: nx.Graph):
    # Get node data
    world = 'new'
    nodes = graph.nodes(data=True)
    for node, data in nodes:
        # run a new experiment if the scientist has a greater than 50% belief that the hypothesis is true
        data['pEH'] = run_experiment(worldState=world) if data['beliefProb'] > 0.5 else None
        data['beliefProb'] = calculate_posterior(data['beliefProb'], data['pEH']) if data['pEH'] is not None else data['beliefProb']

    # update the scientists belief probability based on the observed evidence from their neighbors
    for node, data in nodes:
        neighbors = graph.neighbors(node)
        for neighbor in neighbors:
            neighbor_data = graph.nodes[neighbor]
            if neighbor_data['pEH'] is not None:
                data['beliefProb'] = calculate_posterior(data['beliefProb'], neighbor_data['pEH'])
        data['group'] = sum(data['beliefProb'] > x for x in [0, 0.4, 0.6, 1])
    return graph
import networkx as nx
import matplotlib.pyplot as plt
import random
import statistics
from typing import Literal, Callable

# Define a scientist node
class ScientistNode:
    def __init__(self, beliefProb, pEH=None):
        # the probability that the scientist believes the current hypothesis is true
        self.beliefProb = beliefProb
        # the observational likelihood of the hypothesis
        self.pEH = pEH

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

class Results:
    def __init__(self, graph: nx.Graph):
        self.graph = graph
        self.median_posteriors = []
    def update_graph(self, graph: nx.Graph):
        self.graph = graph
    def add_posterior(self, num: float):
        self.median_posteriors.append(num)
        return self.median_posteriors
    def get_median_posterior(self):
        nodes = self.graph.nodes(data=True)
        posteriors = []
        for _, data in nodes:
            posteriors.append(data['beliefProb'])
        return statistics.median(posteriors)
    
    def plot(self):
        # Define axis and subplots
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15))

        # Plot network visualization
        nx.draw(self.graph, ax=ax1, with_labels=True)
        ax1.set_title('Network Visualization')

        # print the histogram of all the belief probabilities
        belief_probs = [self.graph.nodes[node]['beliefProb'] * 100 for node in self.graph.nodes]
        ax2.bar(range(len(belief_probs)), belief_probs)
        ax2.set_xlabel('Scientist')
        ax2.set_ylabel('Belief Probability (%)')
        ax2.set_title('Current Node Belief Probability Distribution')
        ax2.set_xticks(range(len(belief_probs)))  # Set x-axis ticks to show a number for every bar
        ax2.set_ylim(min(belief_probs) - 1, max(belief_probs) + 1)  # Set y-axis limits based on data

        # Plot line chart of median posteriors
        ax3.plot(self.median_posteriors)
        ax3.set_xlabel('Time Step')
        ax3.set_ylabel('Median Posteriors')
        ax3.set_title('Median Posteriors Over Time')
        ax3.grid(True)  # Add grid to the plot
        ax3.tick_params(axis='x', labelrotation=45)  # Rotate x-axis labels for better readability

        # Show plot
        plt.tight_layout()
        plt.show()

def run_simulation(graph: nx.Graph, timestep_func: Callable[[nx.Graph], nx.Graph], num_timesteps=1):
    results = Results(graph)
    for _ in range(num_timesteps):
        updated_graph = timestep_func(graph)
        results.update_graph(updated_graph)
        # collect metrics
        # display the median posteriors plotted over time 
        # display the current distribution of author beliefs
        results.add_posterior(results.get_median_posterior())

    return results


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
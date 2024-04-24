import networkx as nx
import numpy as np
import random

# Inherit class from modelpy
# https://docs.python.org/3/tutorial/classes.html#inheritance
class ZollmanBandit:
    def __init__(self):
        # Define Parameters
        self.num_nodes = 3
        self.graph_type = 'complete' # complete, wheel, or cycle
        # set the objective values of bandit arms that are unknown to agents
        self.a_objective = 0.49
        self.b_objective = 0.51
        # number of trials per agent
        self.num_trials = 1
        
        # NOTE: This graph variable will not be loaded into the 
        # modelpy interface since it is not a string or number
        self.graph: nx.Graph = None

    def initialize_graph(self):
        if self.graph_type == 'complete':
            self.graph = nx.complete_graph(self.num_nodes)
        elif self.graph_type == 'cycle':
            self.graph = nx.cycle_graph(self.num_nodes)
        else:
            self.graph = nx.wheel_graph(self.num_nodes)
        
        # Initialize all the node data for a bandit model
        for node in self.graph.nodes():
            initial_data = {
                # bandit arm A alpha and beta initialization
                'a_alpha': random.randint(1, 4),
                'a_beta': random.randint(1, 4),
                # bandit arm b learned parameters
                'b_alpha': random.randint(1, 4),
                'b_beta': random.randint(1, 4),
            }
            expectations = {
                'a_expectation': initial_data['a_alpha'] / (initial_data['a_alpha'] + initial_data['a_beta']),
                'b_expectation': initial_data['b_alpha'] / (initial_data['b_alpha'] + initial_data['b_beta'])
            }
            initial_data.update(expectations)
            self.graph.nodes[node].update(initial_data)

    def timestep(self):
        # run the experiments in all the nodes
        for _node, node_data in self.graph.nodes(data=True):
            # agent pulls the "a" bandit arm
            if node_data['a_expectation'] > node_data['b_expectation']:
                node_data['a_alpha'] += int(np.random.binomial(self.num_trials, self.a_objective, size=None))
                node_data['a_beta'] += self.num_trials
                node_data['a_expectation'] = node_data['a_alpha'] / (node_data['a_alpha'] + node_data['a_beta'])

            # agent pulls the "b" bandit arm
            else:
                node_data['b_alpha'] += int(np.random.binomial(self.num_trials, self.b_objective, size=None))
                node_data['b_beta'] += self.num_trials
                node_data['b_expectation'] = node_data['b_alpha'] / (node_data['b_alpha'] + node_data['b_beta'])

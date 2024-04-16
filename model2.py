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
            self.graph.nodes[node].update(initial_data)

    def timestep(self):
        # run the experiments in all the nodes
        for _node, node_data in self.graph.nodes(data=True):
            # agent pulls the "a" bandit arm
            if node_data['a_success_rate'] > node_data['b__learned_success_rate']:
                # agent won't have any new evidence gathered for b
                node_data['b_evidence'] = None

            # agent pulls the "b" bandit arm
            else:
                # agent collects evidence
                node_data['b_evidence'] = int(np.random.binomial(1, self.objective_b, size=None))

        # define function to update posterior
        def calculate_posterior(prior_belief: float, num_evidence: float) -> float:
            # Calculate likelihood, will be either the success rate
            pEH_likelihood = (self.objective_b ** num_evidence) * ((1 - self.objective_b) ** (self.num_pulls - num_evidence))
            
            # Calculate normalization constant
            pE_evidence = (pEH_likelihood * prior_belief) + ((1 - self.objective_b)**num_evidence) * (self.objective_b ** (self.num_pulls - num_evidence)) * (1 - prior_belief)

            # Calculate posterior belief using Bayes' theorem
            posterior = (pEH_likelihood * prior_belief) / pE_evidence
            
            return posterior
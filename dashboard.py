import ipywidgets as widgets
from typing import List, Callable, TypeVar
import networkx as nx
import plotly.graph_objects as go

def plot_network(graph):
    # Convert NetworkX graph to Plotly graph object
    pos = nx.spring_layout(graph)  # positions for all nodes

    # Create edges
    edge_x = []
    edge_y = []
    for edge in graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    # Create nodes
    node_x = []
    node_y = []
    node_text = []
    for node in graph.nodes(data=True):
        x, y = pos[node[0]]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node[0])

    # Create node trace
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        marker=dict(
            size=10,
            color=[],
        ),
        textposition="top center"
    )

    # Create edge trace
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        mode='lines',
        line=dict(width=0.5, color='#888'),
        hoverinfo='none'
    )

    # Create figure
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Interactive Network Visualization',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(
                            text="",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    # Display the interactive graph directly in the notebook
    fig.show()

inputType = TypeVar("inputType")
def create_dashboard(parameters: List[widgets.Widget], timestepFunction: Callable[[inputType], List[float]], functionInputs: inputType):
    widgets.interact_manual(timestepFunction, functionInputs, *parameters)
    return
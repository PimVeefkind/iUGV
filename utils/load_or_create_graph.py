
import os
import pickle

import time

import numpy as np
import networkx as nx

from typing import Callable

from .load_or_create_landscape import Landscape

def load_or_create_graph(terrain: Landscape, cost_function: Callable, args: dict, file: str) -> nx.DiGraph:

    gc_args = args['GRAPH_CONSTRUCTION'] #gc arguments
    gc_params = gc_args['PARAMETERS']

    directory = f"/graphs/{args['ENVIRONMENT']['NAME']}/"
    filename = f"{file}_{cost_function.__name__}_asc={gc_params['ASCENDING']}_desc={gc_params['DESCENDING']}" + \
                f"_perp={gc_params['PERPENDICULAR']}_conn={gc_args['CONNECTION_DEGREE']}.pickle"

    try:
        graph = pickle.load(open(repr(os.getcwd()+directory+filename),'rb'))
    except:
        graph = create_graph(terrain, cost_function, args, filename)

    return graph

    

def create_graph(terrain: Landscape, cost_function: Callable, args: dict, filename: str):

    print('Could not find pickled graph file with specified parameters, creating one instead...')

    pixel_size = args['ENVIRONMENT']['PIXEL_SIZE']
    connection_degree_to_distance = {1: pixel_size+1e-5,
                                     2: np.sqrt(2)*pixel_size+1e-5, 
                                     3: np.sqrt(5)*pixel_size+1e-5}
    t= time.time()
    # First initiate graph.
    graph = nx.DiGraph()

    # Then populate it with nodes and associate with each graph lattice point a physical location
    x_of_nodes, y_of_nodes = np.meshgrid(np.arange(terrain.x_coords.shape[0]),np.arange(terrain.x_coords.shape[0]))
    nodes = list(zip(x_of_nodes.flatten(),y_of_nodes.flatten()))
    pos_of_nodes = list(zip(terrain.x_coords.flatten(),terrain.y_coords.flatten()))
    graph.add_nodes_from(list((node, {"pos": pos_of_node}) for node, pos_of_node in zip(nodes, pos_of_nodes)))

    #Then connect points that are closer than de connection radius
    edges = nx.geometric_edges(graph, radius = connection_degree_to_distance[args['GRAPH_CONSTRUCTION']['CONNECTION_DEGREE']])
    # because we work with directed graph, edges also need to be inverted:
    reverse_edges = list((target,source) for source,target in edges)
    edges.extend(reverse_edges)
    print(f'constructing graph took {t-time.time()}s')

    #compute weights for edges
    params = args['GRAPH_CONSTRUCTION']['PARAMETERS']

    t = time.time()
    weights = cost_function(terrain.z_coords, edges, args['ENVIRONMENT']['PIXEL_SIZE'], params['ASCENDING'],params['DESCENDING'],params['PERPENDICULAR'])
    print(f'calculating weights took {t-time.time()}s')

    #Then connect points that are closer than de connection radius
    graph.add_weighted_edges_from(list((*edge, weight) for edge, weight in zip(edges,weights)))

    pickle.dump(graph, open(os.getcwd()+f"/graphs/{args['ENVIRONMENT']['NAME']}/{filename}.pickle",'wb'))
    
    print('finished creating graph.')

    return graph
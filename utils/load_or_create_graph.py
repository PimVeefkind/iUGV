
import os
import pickle

import time

import numpy as np
import networkx as nx

from typing import Callable

from .load_or_create_landscape import Landscape

def load_or_create_graph(terrain: Landscape, obstacle_map: np.ndarray, cost_function: Callable, args: dict, file: str) -> nx.DiGraph:
    """Load stored graph or calls graph creator function."""

    #Extract some arguments from args to avoid very long variable names when creating filename string.
    gc_args = args['GRAPH_CONSTRUCTION'] #gc arguments
    gc_params = gc_args['PARAMETERS']

    directory = f"/graphs/{args['ENVIRONMENT']['NAME']}/"
    filename = f"{file}_{cost_function.__name__}_asc={gc_params['ASCENDING']}_desc={gc_params['DESCENDING']}" + \
                f"_perp={gc_params['PERPENDICULAR']}_conn={gc_args['CONNECTION_DEGREE']}_pcc={gc_args['PRECOMPUTE_WEIGHTS']}.pickle"

    try:
        graph = pickle.load(open(repr(os.getcwd()+directory+filename),'rb'))
    except:
        graph = create_graph(terrain, obstacle_map, cost_function, args, filename)

    return graph

def create_graph(terrain: Landscape, obstacle_map: np.ndarray, cost_function: Callable, args: dict, filename: str):
    """Create a graph based on terrain,cost_function,args and obstacle map and store it afterwards.
    
    Graph is constructed in several consecetive steps:
    1) Initiate a bidirectional graph (bidirectional because ascend is more diffecult than descend.)
    2) Add nodes on the graph and assign a location to those nodes at every point where the obstace
        map is 0 (no obstacle).
    3) Construct edges between all nodes that are closer than some distance to each other.
    4) (optional) Compute weight of each edge using the cost_function. Optional because it can also be done
       on the fly during shortest path finding but this appears to be more computationally demanding. Hence,
       it is RECOMMENDED to compute weights here."""

    print('Could not find pickled graph file with specified parameters, creating one instead...')

    construct_begin = time.time()

    pixel_size = args['ENVIRONMENT']['PIXEL_SIZE']
    connection_degree_to_distance = {1: pixel_size+1e-5,
                                     2: np.sqrt(2)*pixel_size+1e-5, 
                                     3: np.sqrt(5)*pixel_size+1e-5}
    t= time.time()

    #Step 1
    graph = nx.DiGraph()

    #Step 2
    x_of_nodes, y_of_nodes = np.where(obstacle_map == 0)
    nodes = list(zip(x_of_nodes,y_of_nodes))
    pos_of_nodes = list(zip(terrain.x_coords[x_of_nodes,y_of_nodes].flatten(),terrain.y_coords[x_of_nodes,y_of_nodes].flatten()))
    graph.add_nodes_from(list((node, {"pos": pos_of_node}) for node, pos_of_node in zip(nodes, pos_of_nodes)))

    #Step 3
    edges = nx.geometric_edges(graph, radius = connection_degree_to_distance[args['GRAPH_CONSTRUCTION']['CONNECTION_DEGREE']])
    # Because we work with directed graph, edges also need to be inverted (not performed by default):
    reverse_edges = list((target,source) for source,target in edges)
    edges.extend(reverse_edges)
    print(f'constructing graph took {time.time()-t}s')

    #Step 4
    if args['GRAPH_CONSTRUCTION']['PRECOMPUTE_WEIGHTS']:
        
        params = args['GRAPH_CONSTRUCTION']['PARAMETERS']

        t = time.time()
        weights = cost_function(terrain.z_coords, edges, args['ENVIRONMENT']['PIXEL_SIZE'], params['ASCENDING'],params['DESCENDING'],params['PERPENDICULAR'])
        print(f'calculating weights took {time.time()-t}s')

        #Then connect points that are closer than de connection radius
        graph.add_weighted_edges_from(list((*edge, weight) for edge, weight in zip(edges,weights)))

    else:
        graph.add_edges_from(edges)


    #Store the created graph.
    #pickle.dump(graph, open(os.getcwd()+f"/graphs/{args['ENVIRONMENT']['NAME']}/{filename}.pickle",'wb'))
    
    print('finished creating graph.')

    return graph, time.time() - construct_begin
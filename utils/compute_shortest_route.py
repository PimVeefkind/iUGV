
import time

import numpy as np
import networkx as nx

from utils.load_or_create_landscape import Landscape
from .cost_functions.single_edge.linear_steepness import linear_steepness_cost_function_single


def a_star_heuristic(curr: tuple, target:tuple):

    return np.sqrt(np.square(curr[0]-target[0]) + np.square(curr[1]-target[1]))

def compute_shortest_route(graph: nx.DiGraph, terrain: Landscape, source_idx: int , target_idx: int, args: dict) -> dict:

    routes = {}
    exec_times = {}

    methods = args['PATH_FINDING']['METHODS']
    precomputed_weights = args['GRAPH_CONSTRUCTION']['PRECOMPUTE_WEIGHTS']
    penalties = args['GRAPH_CONSTRUCTION']['PARAMETERS']
    pixel_size = args['ENVIRONMENT']['PIXEL_SIZE']
    z_coords = terrain.z_coords

    if 'dijkstra' in methods:

        start_time = time.time()

        if precomputed_weights:
            routes['dijkstra'] = nx.dijkstra_path(graph, source_idx, target_idx, weight='weight')
        else:
            routes['dijkstra'] = nx.dijkstra_path(graph, source_idx, target_idx, 
                weight= lambda s,t,attrs: linear_steepness_cost_function_single(s,t, penalties, pixel_size,z_coords))
        exec_times['dijkstra'] = time.time() - start_time

    if 'a_star' in methods:

        start_time = time.time()

        if precomputed_weights:
            routes['a_star'] = nx.astar_path(graph, source_idx, target_idx, weight='weight')
        else:
            routes['a_star'] = nx.astar_path(graph, source_idx, target_idx, heuristic= a_star_heuristic, \
                weight= lambda s,t,attrs: linear_steepness_cost_function_single(s,t, penalties, pixel_size,z_coords))
        exec_times['a_star'] = time.time() - start_time

    return routes, exec_times
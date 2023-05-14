
import time

import numpy as np
import networkx as nx

def a_star_heuristic(curr: tuple, target:tuple):

    return np.sqrt(np.square(curr[0]-target[0]) + np.square(curr[1]-target[1]))

def compute_shortest_route(graph: nx.DiGraph, source_idx: int , target_idx: int, methods) -> dict:

    routes = {}
    exec_times = {}

    if 'dijkstra' in methods:

        start_time = time.time()
        routes['dijkstra'] = nx.dijkstra_path(graph, source_idx, target_idx, weight='weight')
        exec_times['dijkstra'] = time.time() - start_time

    if 'a_star' in methods:

        start_time = time.time()
        routes['a_star'] = nx.astar_path(graph, source_idx, target_idx, heuristic= a_star_heuristic)
        exec_times['a_star'] = time.time() - start_time

    return routes, exec_times
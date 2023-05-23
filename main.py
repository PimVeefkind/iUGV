
import os
import yaml
import pickle

import numpy as np

from copy import deepcopy

from utils.load_or_create_graph import load_or_create_graph
from utils.load_or_create_landscape import load_or_create_landscape
from utils.plot_optimal_route import plot_optimal_route
from utils.compute_shortest_route import compute_shortest_route
from utils.create_obstacle_map import create_obstacle_map

from utils.cost_functions.full_graph.linear_steepness import linear_steepness_cost_function


def main(experiment_name: str):

    exec_times = {'construction':{}, 'planning': {}}

    with open(os.getcwd() + f'/experiments/{experiment_name}/{experiment_name}.yaml') as file:
        config_vars = yaml.safe_load(file)

    args = deepcopy(config_vars)

    for size in config_vars['ENVIRONMENT']['SIZE']:

        args['ENVIRONMENT']['SIZE'] = size

        source_idx = (int(args['ENVIRONMENT']['SIZE']*args['PATH_FINDING']['SOURCE_X']), int(args['ENVIRONMENT']['SIZE']*args['PATH_FINDING']['SOURCE_Y']))
        target_idx = (int(args['ENVIRONMENT']['SIZE']*args['PATH_FINDING']['TARGET_X']), int(args['ENVIRONMENT']['SIZE']*args['PATH_FINDING']['TARGET_Y']))

        terrain, landscape_file = load_or_create_landscape(args['ENVIRONMENT'])

        obstacle_map = create_obstacle_map(terrain=terrain, obstacle_args=args['ENVIRONMENT']['OBSTACLE'])
    
        graph, exec_times['construction'][size] = \
            load_or_create_graph(terrain= terrain, obstacle_map=obstacle_map,cost_function= linear_steepness_cost_function, args= args, file = landscape_file)

        routes, exec_times['planning'][size] = compute_shortest_route(graph,terrain, source_idx, target_idx, args)

        plot_optimal_route(terrain=terrain, obstacle_map= obstacle_map, routes = routes, endpoints = (source_idx,target_idx))

    if experiment_name == 'time_complexity':
        pickle.dump(exec_times, open(os.getcwd()+f'/experiments/{experiment_name}/execution_times_aonly.pickle','wb'))

if __name__ == '__main__':

    experiment_name = 'playground'

    main(experiment_name)
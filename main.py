import os
import yaml
import pickle

from copy import deepcopy

from utils.plot_optimal_route import plot_optimal_route
from utils.create_obstacle_map import create_obstacle_map
from utils.load_or_create_graph import load_or_create_graph
from utils.compute_shortest_route import compute_shortest_route
from utils.load_or_create_landscape import load_or_create_landscape
from utils.cost_functions.full_graph.linear_steepness import linear_steepness_cost_function


def main(experiment_name: str) -> None:
    '''Function orchestrating the complete navigation procedure for different system sizes. 
    
    For every size, the following steps are repeated:
        1: Create or load the landscape on which we will navigate.
        2: Define regions in the landscape that are not penetrable.
        3: Create a graph of the penetrable landscape.
        4: Compute the shortest route from the source to the target node.
        5 (optional): Plot the shortest route.'''

    exec_times = {'construction':{}, 'planning': {}}

    #Load in the configuration/parameter settings
    with open(os.getcwd() + f'/experiments/{experiment_name}/{experiment_name}.yaml') as file:
        config_vars = yaml.safe_load(file)

    args = deepcopy(config_vars)

    for size in config_vars['ENVIRONMENT']['SIZE']:

        args['ENVIRONMENT']['SIZE'] = size

        #Define the beginning and end locations of the path we need to find.
        source_idx = (int(args['ENVIRONMENT']['SIZE']*args['PATH_FINDING']['SOURCE_X']), int(args['ENVIRONMENT']['SIZE']*args['PATH_FINDING']['SOURCE_Y']))
        target_idx = (int(args['ENVIRONMENT']['SIZE']*args['PATH_FINDING']['TARGET_X']), int(args['ENVIRONMENT']['SIZE']*args['PATH_FINDING']['TARGET_Y']))

        #Step 1
        terrain, landscape_file = load_or_create_landscape(args['ENVIRONMENT'])

        #Step 2
        obstacle_map = create_obstacle_map(terrain=terrain, obstacle_args=args['ENVIRONMENT']['OBSTACLE'])
    
        #Step 3
        graph, exec_times['construction'][size] = \
            load_or_create_graph(terrain= terrain, obstacle_map=obstacle_map,cost_function= linear_steepness_cost_function, args= args, file = landscape_file)

        #Step 4
        routes, exec_times['planning'][size] = compute_shortest_route(graph,terrain, source_idx, target_idx, args)

        #Step 5 (can be commented if not required/wanted)
        plot_optimal_route(terrain=terrain, obstacle_map= obstacle_map, routes = routes, endpoints = (source_idx,target_idx))

    if experiment_name == 'time_complexity':
        pickle.dump(exec_times, open(os.getcwd()+f'/experiments/{experiment_name}/execution_times_aonly.pickle','wb'))

if __name__ == '__main__':

    #Define name of configuration file to use.
    experiment_name = 'playground'

    main(experiment_name)
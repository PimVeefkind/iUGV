
import numpy as np

from .load_or_create_graph import Landscape

def create_obstacle_map(terrain: Landscape, obstacle_args: dict) -> np.ndarray:

    assert obstacle_args['NAME'] in ['open', 'square'], 'Only no obstacle (open) and square obstacles are implemented.'

    obstacle_map = np.zeros_like(terrain.x_coords)

    if obstacle_args['NAME'] == 'open':
        return obstacle_map
    
    elif obstacle_args['NAME'] == 'square':

        size = terrain.x_coords.shape[0]
        params = obstacle_args['PARAMS']

        obstacle_map[int(params['FRACS_X'][0]*size):int(params['FRACS_X'][1]*size),
                     int(params['FRACS_Y'][0]*size):int(params['FRACS_Y'][1]*size)] = 1
        
        return obstacle_map

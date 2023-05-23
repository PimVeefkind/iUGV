
import numpy as np

from .load_or_create_graph import Landscape

def create_obstacle_map(terrain: Landscape, obstacle_args: dict) -> np.ndarray:
    """Create obstacle map with size of the terrain.
    
    When obstacle map has value 1 at some location this indicates a location is an obstacle.
    0 Means it is not an object (penetrable). Currently two kinds of obstacles are supported:
        - open: No obstacle whatsoever.
        - square: Rectangular obstacle defined as a fraction of the total size."""

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

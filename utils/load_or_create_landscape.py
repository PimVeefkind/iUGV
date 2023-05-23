
import os
import pickle

import numpy as np

from dataclasses import dataclass

@dataclass
class Landscape():
    '''Class describing the terrain.'''

    x_coords: np.ndarray
    y_coords: np.ndarray
    z_coords: np.ndarray

def load_or_create_landscape(envs_params: dict) -> tuple[Landscape,str]:
    """Attempt load saved landscape else calls landscape create function.
    
    Currently, only 'gaussian' landscape is supported. Landscapes
    are saved in 'experiments/. '"""

    assert envs_params['NAME'] in ['gaussian'], 'Please choose existing parametrized terrain type.'

    size = envs_params['SIZE']
    pixel_size = envs_params['PIXEL_SIZE']

    directory = f"/landscapes/{envs_params['NAME']}/"
    filename = f"size={size}-pixel_size={pixel_size}.pickle"

    try:
        terrain = pickle.load(open(os.getcwd()+directory+filename,'rb'))
    except:
        if envs_params['NAME'] == 'gaussian':
            terrain = create_gaussian_landscape(size, pixel_size, max_height= size/10)

    return terrain, f"size={size}-pixel_size={pixel_size}"

def create_gaussian_landscape(size: int, pixel_size: float, scale: float = 0.15, max_height: float = 100.)\
      -> tuple[Landscape, str]:
    '''Create 2D-Gaussian Landscape dataclass.
    
    Height is computed as A*exp(-((x-c_x)^2+(y-c_y)^2)/(2s^2)) where c_x,c_y the center coordinates of the landscape.
    s (standard deviation) controls the width of the gaussian hill in relation to the terrain size. A can be
    used to tune the hills absolute steepness. Currently, it is linear in the number of pixels such that the
    the steepness is constant as a function of the landscape size for given s. Afterwards, landscape is saved with pickle.'''
    
    print('Could not find pickled landscape file with specified parameters, creating one instead...')
    
    x_coords, y_coords = np.meshgrid(np.arange(0,size,pixel_size),
                                     np.arange(0,size,pixel_size))
    
    center = size/2

    scale *= size
    
    z_coords = max_height*np.exp(-((x_coords-center)**2+(y_coords-center)**2)/(2*scale**2))

    terrain = Landscape(x_coords=x_coords,y_coords=y_coords,z_coords=z_coords)

    # Save created terrain
    filename = f"size={size}-pixel_size={pixel_size}.pickle"

    pickle.dump(terrain, open(os.getcwd()+f'/landscapes/gaussian/{filename}','wb'))

    print('finished creating landscape.')

    return terrain
    




import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import axes3d

from .load_or_create_landscape import Landscape


def plot_optimal_route(terrain: Landscape, routes: dict, endpoints = tuple):

    ax = plt.figure().add_subplot(projection='3d')

    linestyles = ['solid', 'dashed']

    ax.plot_surface(terrain.x_coords, terrain.y_coords, terrain.z_coords, 
                    edgecolor='blue', lw=0.5, rstride=10, cstride=10,
                    alpha=0.3)
    
    ax.scatter(terrain.x_coords[endpoints[0]],terrain.y_coords[endpoints[0]],\
               terrain.z_coords[endpoints[0]], label = 'start', color = 'red')
    ax.scatter(terrain.x_coords[endpoints[1]],terrain.y_coords[endpoints[1]],\
               terrain.z_coords[endpoints[1]], label = 'finish', color = 'darkgreen')
    
    for algorithm, route, linestyle in zip(routes.keys(),routes.values(),linestyles):

        x_elements = np.array(list(tple[0] for tple in route))
        y_elements = np.array(list(tple[1] for tple in route))

        ax.plot(xs = terrain.x_coords[x_elements,y_elements].flatten(),
                ys = terrain.y_coords[x_elements,y_elements].flatten(),
                zs = terrain.z_coords[x_elements,y_elements].flatten(),
                label = algorithm, color = 'black', linestyle = linestyle)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('height')
    ax.legend()

    plt.savefig('output.pdf')
    plt.show()
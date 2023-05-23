
import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import axes3d

from .load_or_create_landscape import Landscape


def plot_optimal_route(terrain: Landscape, obstacle_map: np.ndarray, routes: dict, endpoints: tuple):
    """Make plot of the landscape, obstacle regions and the shortest routes found.
    
    Plotting occurs in three steps.
    1) A terrain surface is plotted. The color of the terrain is determined by its penetrainability.
    2) The end and source nodes are plotted.
    3) The different routes are plotted."""

    ax = plt.figure().add_subplot(projection='3d')

    linestyles = ['solid', 'dashed']

    #Make custom ScalarMappable to color surface based on penetrenability.
    mappable = plt.cm.ScalarMappable(cmap = 'jet')
    mappable.set_array([])
    face_colors = mappable.to_rgba(obstacle_map)

    # Step 1: Plot Landscape and obstacles through color
    ax.plot_surface(terrain.x_coords, terrain.y_coords, terrain.z_coords, 
                    facecolors = face_colors, lw=0.5, rstride=10, cstride=10,
                    alpha=0.6)
    
    #Step 2
    ax.scatter(terrain.x_coords[endpoints[0]],terrain.y_coords[endpoints[0]],\
               terrain.z_coords[endpoints[0]], label = 'start', color = 'red')
    ax.scatter(terrain.x_coords[endpoints[1]],terrain.y_coords[endpoints[1]],\
               terrain.z_coords[endpoints[1]], label = 'finish', color = 'darkgreen')
    
    #Step 3
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

    #Failsafe to ensure result is always available also if screen is not correctly defined (WSL or via SSH).
    plt.savefig('output.pdf')
    plt.show()
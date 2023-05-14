
import numpy as np

from numba import jit

#@jit(nopython = True)
def linear_steepness_cost_function(z_coords: np.ndarray, edges: list[tuple],  pixel_size: float, pen_asc: float,
                                    pen_desc: float, pen_perp: float)\
     -> list[float]:

    dist_conn_2 = np.sqrt(2)*pixel_size
    gl = z_coords.shape[0] #grid_length
    weights = np.empty(shape=(len(edges)))
    
    for e,edge in enumerate(edges):
        # define surrounding sur
        x_s, y_s = edge[0]
        x_t, y_t = edge[1]

        #conn degree 1, edge in x-direction
        if x_s == x_t:
            par_slope = (z_coords[x_t,y_t] - z_coords[x_s,y_s]) / pixel_size
            perp_slope = 1/2* np.abs((z_coords[x_t,np.mod(y_t+1,gl)]-2*z_coords[x_t,y_t]+z_coords[x_t,np.mod(y_t-1,gl)])+\
                                  ((z_coords[x_s,np.mod(y_s+1,gl)]-2*z_coords[x_s,y_s]+z_coords[x_s,np.mod(y_s-1,gl)])))/ pixel_size
            weights[e] = pen_asc*max(0,par_slope) + pen_desc*min(0,par_slope) + pen_perp * perp_slope + pixel_size

        # conn degree 1, edge in y-direction
        elif y_s == y_t:
            par_slope = (z_coords[x_t,y_t] - z_coords[x_s,y_s]) / pixel_size
            perp_slope = 1/2* np.abs((z_coords[np.mod(x_t+1,gl),y_t]-2*z_coords[x_t,y_t]+z_coords[np.mod(x_t-1,gl),y_t])+\
                                  ((z_coords[np.mod(x_s+1,gl),y_s]-2*z_coords[x_s,y_s]+z_coords[np.mod(x_s-1,gl),y_s])))/ pixel_size 
            weights[e] = pen_asc*max(0,par_slope) + np.abs(pen_desc*min(0,par_slope)) + pen_perp * perp_slope + pixel_size
        # conn degree 2 
        else:
            
            if x_s < x_t:
                par_slope = (z_coords[x_t,y_t] - z_coords[x_s,y_s]) / (dist_conn_2)
                perp_slope = np.abs(z_coords[np.mod(x_s+1,gl),y_s] - z_coords[x_s,np.mod(y_s-1,gl)]) / (dist_conn_2)

            elif x_t < x_s:
                par_slope = (z_coords[x_t,y_t] - z_coords[x_s,y_s]) / (dist_conn_2)
                perp_slope = np.abs(z_coords[np.mod(x_s-1,gl),y_s] - z_coords[x_s,np.mod(y_s+1,gl)]) / (dist_conn_2)

            weights[e] = pen_asc*max(0,par_slope) + np.abs(pen_desc*min(0,par_slope)) + pen_perp * perp_slope + dist_conn_2

    return weights
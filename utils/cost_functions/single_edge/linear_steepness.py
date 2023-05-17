
import numpy as np

def linear_steepness_cost_function_single(source: tuple, target: tuple , pens: dict, pixel_size: float, z_coords:np.ndarray):

    gl = z_coords.shape[0]
    dist_conn_2 = np.sqrt(2)*pixel_size

    x_s, y_s = source
    x_t, y_t = target
    
    if x_s == x_t:

        par_slope = (z_coords[x_t,y_t] - z_coords[x_s,y_s]) / pixel_size
        perp_slope = 1/2* np.abs((z_coords[x_t,np.mod(y_t+1,gl)]-2*z_coords[x_t,y_t]+z_coords[x_t,np.mod(y_t-1,gl)])+\
                                  ((z_coords[x_s,np.mod(y_s+1,gl)]-2*z_coords[x_s,y_s]+z_coords[x_s,np.mod(y_s-1,gl)])))/ pixel_size
        
        return pens['ASCENDING']*max(0,par_slope) + pens['DESCENDING']*min(0,par_slope) + pens['PERPENDICULAR'] * perp_slope + pixel_size
    
    elif y_s == y_t:
        par_slope = (z_coords[x_t,y_t] - z_coords[x_s,y_s]) / pixel_size
        perp_slope = 1/2* np.abs((z_coords[np.mod(x_t+1,gl),y_t]-2*z_coords[x_t,y_t]+z_coords[np.mod(x_t-1,gl),y_t])+\
                                  ((z_coords[np.mod(x_s+1,gl),y_s]-2*z_coords[x_s,y_s]+z_coords[np.mod(x_s-1,gl),y_s])))/ pixel_size 
        return pens['ASCENDING']*max(0,par_slope) + np.abs(pens['DESCENDING']*min(0,par_slope)) + pens['PERPENDICULAR'] * perp_slope + pixel_size
    
    else:
            
        if x_s < x_t:
            par_slope = (z_coords[x_t,y_t] - z_coords[x_s,y_s]) / (dist_conn_2)
            perp_slope = np.abs(z_coords[np.mod(x_s+1,gl),y_s] - z_coords[x_s,np.mod(y_s-1,gl)]) / (dist_conn_2)

        elif x_t < x_s:
            par_slope = (z_coords[x_t,y_t] - z_coords[x_s,y_s]) / (dist_conn_2)
            perp_slope = np.abs(z_coords[np.mod(x_s-1,gl),y_s] - z_coords[x_s,np.mod(y_s+1,gl)]) / (dist_conn_2)

        return pens['ASCENDING']*max(0,par_slope) + np.abs(pens['DESCENDING']*min(0,par_slope)) + pens['PERPENDICULAR'] * perp_slope + pixel_size
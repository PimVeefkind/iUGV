
import os
import pickle

import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit

def lin_fit(x,a,b):
    return a*x+b

def main():

    exec_times_dict = pickle.load(open(os.getcwd()+'/experiments/time_complexity/execution_times.pickle','rb'))
    exec_times_dict_aonly = pickle.load(open(os.getcwd()+'/experiments/time_complexity/execution_times_aonly.pickle','rb'))

    sizes = np.array(list(exec_times_dict['construction'].keys()))
    sizes_aonly = np.array(list(exec_times_dict_aonly['construction'].keys()))
    construct_times = np.array(list(exec_times_dict_aonly['construction'].values()))
    dijkstra_times = np.array(list(exec_times_dict['planning'][size]['dijkstra'] for size in sizes))
    astar_times = np.array(list(exec_times_dict_aonly['planning'][size]['a_star'] for size in sizes_aonly))


    log_sizes = np.log(sizes)
    log_sizes_aonly = np.log(sizes_aonly)
    log_construct_times = np.log(construct_times)
    log_dijkstra_times = np.log(dijkstra_times)
    log_astar_times = np.log(astar_times)

    par_construct, _ = curve_fit(lin_fit, log_sizes_aonly, log_construct_times)
    par_dijkstra, _ = curve_fit(lin_fit, log_sizes, log_dijkstra_times)
    par_astar, _ = curve_fit(lin_fit, log_sizes_aonly, log_astar_times)

    fig, (ax1,ax2) = plt.subplots(1,2,figsize = (9,4))

    ax1.plot(sizes_aonly, construct_times, color = 'navy', marker = 'x', label = 'Construction', linewidth = 1)
    ax1.plot(sizes, dijkstra_times, color = 'darkred', marker = 'x', label = 'Dijkstra Search', linewidth = 1)
    ax1.plot(sizes_aonly, astar_times, color = 'darkgreen', marker = 'x', label = 'A* Search', linewidth = 1)

    min_and_max = np.array((np.min(log_sizes),np.max(log_sizes)))

    ax2.scatter(log_sizes_aonly, log_construct_times, color = 'navy', marker = 'x', label = 'Construction')
    ax2.plot(min_and_max,lin_fit(min_and_max, par_construct[0],par_construct[1]), color = 'navy',\
        label = f'y={par_construct[0]:.1f}x+{par_construct[1]:.1f}', linewidth =1)
    
    ax2.scatter(log_sizes, log_dijkstra_times, color = 'darkred', marker = 'x', label = 'Dijkstra Search')
    ax2.plot(min_and_max,lin_fit(min_and_max, par_dijkstra[0],par_dijkstra[1]), color = 'darkred',\
        label = f'y={par_dijkstra[0]:.1f}x+{par_dijkstra[1]:.1f}', linewidth =1)

    ax2.scatter(log_sizes_aonly, log_astar_times, color = 'darkgreen', marker = 'x', label = 'A* Search')
    ax2.plot(min_and_max,lin_fit(min_and_max, par_astar[0],par_astar[1]), color = 'darkgreen',\
        label = f'y={par_astar[0]:.1f}x+{par_astar[1]:.1f}', linewidth =1)

    ax1.set_title('Execution time as a function environment \n size with constant resolution')
    ax2.set_title('Logarithmic plot of execution time as a function of \n environment size with constant resolution')

    ax1.set_ylabel('Time in (s)')
    ax2.set_ylabel('Time in log(s)')
    ax1.set_xlabel('Size of Environment in (#pixels)')
    ax2.set_xlabel('Size of Environment in log(#pixels)')

    for ax in (ax1,ax2):

        ax.legend(fontsize = 9)
        ax.grid()

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':

    main()
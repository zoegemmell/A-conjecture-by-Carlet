import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from tqdm import tqdm

c1_components = np.zeros(1000000 - 2)
c2_components = np.zeros(1000000 - 2)
c3_components = np.zeros(1000000 - 2)
c4_components = np.zeros(1000000 - 2)
r_floor = np.zeros(1000000-2)

bound_optimal = np.zeros(1000000 - 2)
r_optimal = np.zeros(1000000 - 2)

def create_ci_components():
    i=0
    for j in range(2,1000000):
        c1_components[i] = 1/j**3 - 1/(8*j**4)
        c2_components[i] = 1/j**2 - 1/(4*j**3)
        c3_components[i] = 2/j - 11/(8*j**2)
        c4_components[i] = 1/j
        r_floor[i] = j-1
        i+=1

def find_optimal_r_floor_and_bound(delta_max):
    r = 1
    delta = 3

    c1_value = np.zeros(1)
    c1_value[0] = c1_components[delta-3]
    c2_value = np.zeros(1)
    c2_value[0] = c2_components[delta-3]
    c3_value = np.zeros(1)
    c3_value[0] = c3_components[delta-3]
    c4_value = np.zeros(1)
    c4_value[0] = c4_components[delta-3]

    bound_a = 3/2*delta**4 - 2*delta**3 + 5/2*delta**2
    bounds = np.zeros(delta - 2)
    bounds = (r+0.01)*bound_a + (delta**5 * c1_value + 3* delta ** 4 * c2_value + delta ** 3 *c3_value - 3/4 * delta ** 2 * c4_value + 2 * delta ** 2)
    bound_optimal[delta-3] = bounds[0]
    r_optimal[delta-3] = 1

    delta += 1

    for delta in tqdm(range(4, delta_max + 1)):
        #print("delta:", delta)
        r = r_floor[:delta-2] # doesn't include the end value so need -2
        bound_a = 3/2*delta**4 - 2*delta**3 + 5/2*delta**2
        #old_bound[delta-3] = 
        bounds = np.zeros(delta - 2)

        c1_value = c1_value + c1_components[delta-3]
        c1_value = np.append(c1_value, c1_components[delta-3])
        c2_value = c2_value + c2_components[delta-3]
        c2_value = np.append(c2_value, c2_components[delta-3])
        c3_value = c3_value + c3_components[delta-3]
        c3_value = np.append(c3_value, c3_components[delta-3])
        c4_value = c4_value + c4_components[delta-3]
        c4_value = np.append(c4_value, c4_components[delta-3])
        
        # need to deal with (r) in the case of as this cannot be 1 since r in (1,delta-1)
        bounds = (r+0.01)*bound_a + (delta**5 * c1_value + 3* delta ** 4 * c2_value + delta ** 3 *c3_value - 3/4 * delta ** 2 * c4_value + 2 * delta ** 2)

        bound_optimal[delta-3] = bounds[0]
        for i in range(len(bounds)):
            if bounds[i] < bound_optimal[delta-3]:
                r_optimal[delta-3] = i+1
                bound_optimal[delta-3] = bounds[i]

        #print(f"The optimal r floor is {r_optimal[delta-3]} which produces the optimal bound {bound_optimal[delta-3]}")
        #print()

    return r_optimal

def plot_r_floor():
    # Plot the graph
    plt.plot(r_floor[:size-2] + 2, r_optimal[:size-2], marker='o', linestyle='-', label = r'$\lfloor r \rfloor (\frac{3}{2} \delta^4 - 2 \delta ^3 + \frac{5}{2} \delta^2) + (\delta^5 c_1 +3 \delta^4 c_2 +\delta^3 c_3 - \frac{3}{4} \delta^2 c_4 +2 \delta^2)$') 

    # Add labels and title for clarity
    plt.xlabel("Delta")
    plt.ylabel("Optimal r floor value")
    plt.title("Plot of Optimal r floor vs. Delta")

    # Display the plot
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_bound():
    # Plot the graph
    plt.plot(r_floor[:size-2] + 2, bound_optimal[:size-2], marker='o', linestyle='-', label = r'$\lfloor r \rfloor (\frac{3}{2} \delta^4 - 2 \delta ^3 + \frac{5}{2} \delta^2) + (\delta^5 c_1 +3 \delta^4 c_2 +\delta^3 c_3 - \frac{3}{4} \delta^2 c_4 +2 \delta^2)$') 
    plt.plot(r_floor[:size-2] + 2,2*(r_floor[2:size])**(13/3) + 3*(r_floor[2:size])**(11/3), marker='o', linestyle='-', label = r'$2 \delta^{\frac{13}{3}} + 3 \delta^{\frac{11}{3}}$')

    # Add labels and title for clarity
    plt.xlabel("Delta")
    plt.ylabel("Bound value")
    plt.title("Plot of Bound vs. Delta")

    # Display the plot
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_difference():
    # Plot the graph
    plt.plot(r_floor[:size-2] + 2, 2*(r_floor[2:size])**(13/3) + 3*(r_floor[2:size])**(11/3) - bound_optimal[:size-2] , marker='o')

    # Add labels and title for clarity
    plt.xlabel("Delta")
    plt.ylabel("Bound value")
    plt.title("Plot of Bound vs. Delta")

    # Display the plot
    plt.grid(True)
    plt.legend()
    plt.show()

size = 10**6
start_time = datetime.now()
create_ci_components()
end_time = datetime.now()
time_elapsed = end_time - start_time
print("Time elapsed: ", time_elapsed)
start_time = datetime.now()
find_optimal_r_floor_and_bound(size)
end_time = datetime.now()
time_elapsed = end_time - start_time
print("Time elapsed: ", time_elapsed)
plot_r_floor()
plot_bound()
plot_difference()
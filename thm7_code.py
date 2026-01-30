import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from tqdm import tqdm
import csv
import os

size = 3*10**5+3
c1_components = np.zeros(size - 2)
c2_components = np.zeros(size - 2)
c3_components = np.zeros(size - 2)
c4_components = np.zeros(size - 2)
r_floor = np.zeros(size-2)
zgtt_bound = np.zeros(size-2)
first_cross = 0
second_cross = 0

bound_optimal = np.zeros(size - 2)
r_optimal = np.zeros(size - 2)

def create_ci_components():
    i=0
    for j in range(2,size):
        c1_components[i] = 1/j**3 - 1/(8*j**4)
        c2_components[i] = 1/j**2 - 1/(4*j**3)
        c3_components[i] = 2/j - 11/(8*j**2)
        c4_components[i] = 1/j
        r_floor[i] = j-1
        zgtt_bound[i] = 1.99*(j+1)**(13/3)
        i+=1

def find_optimal_r_floor_and_bound(delta_max):
    is_smaller = 0
    isNOT_smaller = 0
    first_cross = 0
    second_cross = 0

    # TODO: change file location 
    with open('C:/Users/z5653374/OneDrive - UNSW\Documents/Playing around/bound_optimisation.csv', mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['delta', 'r', 'bound','our_bound'])
        
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
        bounds = (r)*bound_a + (delta**5 * c1_value + 3* delta ** 4 * c2_value + delta ** 3 *c3_value - 3/4 * delta ** 2 * c4_value + 2 * delta ** 2)
        bound_optimal[delta-3] = bounds[0]
        r_optimal[delta-3] = 1

        #Write value for delta = 3 to file
        writer.writerow([delta, r_optimal[delta-3], bound_optimal[delta-3], zgtt_bound[delta-3]])

        delta += 1

        for delta in tqdm(range(4, delta_max + 1)):
            #print("delta:", delta)
            r = r_floor[:delta-2] # range doesn't include the end value (i.e. delta-1) so need -2
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
            bounds = (r)*bound_a + (delta**5 * c1_value + 3* delta ** 4 * c2_value + delta ** 3 *c3_value - 3/4 * delta ** 2 * c4_value + 2 * delta ** 2)

            bound_optimal[delta-3] = bounds[0]
            for i in range(len(bounds)):
                if bounds[i] < bound_optimal[delta-3]:
                    r_optimal[delta-3] = i+1
                    bound_optimal[delta-3] = bounds[i]
            
            if bound_optimal[delta-3] <= zgtt_bound[delta-3]:
                #print("For delta =", delta)
                #print("optimal bound:", bound_optimal[delta-3], "IS less than our bound:", zgtt_bound[delta-3])
                #print()
                is_smaller += 1
            else:
                if first_cross == 0:
                    first_cross = delta
                    print("First cross:", first_cross)
                else:
                    second_cross = delta
                    print("Second cross:", second_cross)
                print("For delta =", delta)
                print("optimal bound:", bound_optimal[delta-3], "is NOT less than our bound:", zgtt_bound[delta-3])
                print()
                isNOT_smaller += 1

            #print(f"The optimal r floor is {r_optimal[delta-3]} which produces the optimal bound {bound_optimal[delta-3]}")
            #print()

            #Write values to file
            writer.writerow([delta, r_optimal[delta-3], bound_optimal[delta-3], zgtt_bound[delta-3]])

    print(is_smaller, "deltas are bounded by our new bound")
    print(isNOT_smaller, "deltas are NOT bounded by our bound")

    plot_bound(first_cross, second_cross)

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

def plot_bound(first_cross, second_cross):
    # Plot the graph
    plt.plot(r_floor[:size-2] + 2, bound_optimal[:size-2], marker='o', linestyle='-', label = r'$\lfloor r \rfloor (\frac{3}{2} \delta^4 - 2 \delta ^3 + \frac{5}{2} \delta^2) + (\delta^5 c_1 +3 \delta^4 c_2 +\delta^3 c_3 - \frac{3}{4} \delta^2 c_4 +2 \delta^2)$') 
    #plt.plot(r_floor[:size-2] + 2,2*(r_floor[:size-2]+2)**(13/3) + 3*(r_floor[:size-2]+2)**(11/3), marker='o', linestyle='-', label = r'$2 \delta^{\frac{13}{3}} + 3 \delta^{\frac{11}{3}}$')
    plt.plot(r_floor[:size-2] + 2,zgtt_bound[:size-2], marker='o', linestyle='-', label = 'our new bound')

    # Add vertical lines for the 
    plt.axvline(x = first_cross, color = 'b', label = 'first crossover')
    plt.axvline(x = second_cross, color = 'b', label = 'second crossover')

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

start_time = datetime.now()
create_ci_components()
find_optimal_r_floor_and_bound(size)
end_time = datetime.now()
time_elapsed = end_time - start_time
print("Time elapsed: ", time_elapsed)
#plot_r_floor()
#plot_bound()
#plot_difference()

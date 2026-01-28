# The following code was used in the proof of Theorem 3 for 4 ≤ k ≤ 100

size = 101 # the upper limit of k
# a list of primes
primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461,463,467,479,487,491,499]

# TODO: description of method
def calculate_n_bound_per_k(k_max):
    worst_case = []
    j_is_2point6 = []
    j_same_as_kgeq100 = []
    j_is_more_than_3 = []
    for k in range(4, k_max):
        n = 1
        q = 2**n
        current_prime = primes[0]
        location = 0
        if k < 7:
            G = 2.924
        else:
            G = 2.86
        temp_bound = q-(2**(k-1)-1)*(2**(k-1)-2)*q**(1/2) - (G*2**((13*(k-1))/3) + 2**(2*k))
        while temp_bound < 0:
            n += 1
            q = 2**n
            temp_bound = q-(2**(k-1)-1)*(2**(k-1)-2)*q**(1/2) - (G*2**((13*(k-1))/3) + 2**(2*k))

        while current_prime < n:
            location += 1
            current_prime = primes[location]
        
        # Optional outputs demonstrating the process of classifying the remainder
        #print("For k =", k, "the minimum n is where the expr is +ve is n=", n)
        #print("So the prime that sets the lower boundary for all other primes is:", primes[location-1])
        #print("The (13/3)*k part:", (13/3)*k)
        #print("Chosen prime:", primes[location-1])
        #print("the remainder part is:", primes[location-1] - (13/3)*k)
        #print()

        # Sorting the k's by 
        if primes[location-1] - (13/3)*k < -3:
            j_is_more_than_3.append(k)
        elif primes[location-1] - (13/3)*k <= -2.817:
            j_same_as_kgeq100.append(k)
        elif primes[location-1] - (13/3)*k < -2.6:
            j_is_2point6.append(k)
        else:
            worst_case.append(k)

    # Final output for 
    print("k's for which j is small and negative:", worst_case)
    print("k's for which j = -2.6:", j_is_2point6)
    print("k's for which j = -2.817:", j_same_as_kgeq100)
    print("k's for which j < -3:", j_is_more_than_3)

# run the above function with the maximum size of k
calculate_n_bound_per_k(size)
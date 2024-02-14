import numpy as np
import math
import copy
import random
import pickle
import os
from tqdm import tqdm
import matplotlib.pyplot as plt

def modify_relations():
    """
    Prompts the user to enter the names of two persons and their new relationship level.
    Updates the relationship level between the two persons in the 'relation' dictionary.
    Persists the updated 'relation' dictionary in a file named 'relation_data.pkl'.

    :return: None
    """
    person1 = input("Enter first person's name: ")
    person2 = input("Enter second person's name: ")
    if person1 in guests and person2 in guests:
        new_relationship = int(input(f"Enter new relationship level (1-5) for {person1} and {person2}: "))
        relation[(person1, person2)] = new_relationship
        with open('relation_data.pkl', 'wb') as f:
            pickle.dump(relation, f)

def display_arrangement_in_circle(arrangement):
    """
    Display the arrangement in a circular way as a seating chart.

    :param arrangement: A list of guest's names
    :return: None
    """
    n = len(arrangement)
    x_values = []
    y_values = []
    labels = []

    angle = 2 * math.pi / n
    for i in range(n):
        x = 10 * math.cos(i * angle)
        y = 10 * math.sin(i * angle)
        x_values.append(x)
        y_values.append(y)
        labels.append(arrangement[i])

    plt.figure(figsize=(10,10))
    plt.scatter(x_values, y_values)
    for i, name in enumerate(labels):
        plt.annotate(name, (x_values[i], y_values[i]), fontsize=20)
    plt.title("Guest Seating Arrangement")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()



def get_total_familiarity(arrangement):
    """
    Calculate the total familiarity of a given arrangement.

    :param arrangement: A list representing the seating arrangement of guests.
    :type arrangement: list
    :return: The total familiarity score of the arrangement.
    :rtype: int
    """
    total = 0
    for i in range(len(arrangement)):
        total += familiarity[guests.index(arrangement[i]), guests.index(arrangement[(i + 1) % len(arrangement)])]
    return total


def simulated_annealing(arrangement, optimize='min', T=5000, T_min=0.01, alpha=0.9):
    """
    Simulated Annealing

    :param arrangement: The initial arrangement of elements.
    :param optimize: The optimization criteria. Possible values are 'min' (default) and 'max'.
    :param T: The initial temperature. Default value is 5000.
    :param T_min: The minimum temperature. Default value is 0.01.
    :param alpha: The temperature reduction factor. Default value is 0.9.
    :return: The optimized arrangement.

    Simulated annealing is a probabilistic optimization algorithm that is used to find the minimum or maximum of a
    function by gradually reducing the temperature. It is based on the concept * of simulated annealing in
    metallurgy, where a material is cooled slowly to reduce defects and improve overall structure.

    The `simulated_annealing` method takes an initial arrangement and performs simulated annealing to optimize the
    arrangement based on a given optimization criteria. During the annealing process, two elements in the
    arrangement are randomly swapped and the total familiarity of the arrangement is calculated. The arrangement is
    updated if the total familiarity increases (for maximizing) or decreases (for minimizing), or based on a
    probability determined by the temperature and the change in familiarity. The temperature is reduced over time
    using a temperature reduction factor.

    The method runs until the temperature reaches the minimum temperature. The final optimized arrangement is returned.

    Example usage:
    ```
    initial_arrangement = [1, 2, 3, 4, 5]
    optimized_arrangement = simulated_annealing(initial_arrangement)
    print(optimized_arrangement)
    ```
    """
    while T > T_min:
        new_arrangement = copy.deepcopy(arrangement)
        i, j = random.sample(range(len(arrangement)), 2)
        new_arrangement[i], new_arrangement[j] = new_arrangement[j], new_arrangement[i]

        current_familiarity = get_total_familiarity(arrangement)
        new_familiarity = get_total_familiarity(new_arrangement)

        delta = new_familiarity - current_familiarity
        try:
            accept_probability = math.exp(-delta / T)
        except OverflowError:
            accept_probability = 0

        if (delta < 0 and optimize == 'min') or (delta > 0 and optimize == 'max') or random.random() < accept_probability:
            arrangement = new_arrangement
        T = T * alpha
    return arrangement



if __name__ == '__main__':
    # If you want to modify relations, uncomment the following line:
    what_you_want_to_get = 'max'

    # guests list
    guests = ["Alex", "Aidan", "Luke", "Rees", "Marcus", "Pres", "Roisin", "Rory", "Ginge", "Neasa", "Jenn", "Colm",
              "Morgan", "Conner", "Abi"]

    """
    RELATIONSHIP RATINGS
    1 - Never Met
    2 - Met Once or Twice
    3 - Solid Acquaintances 
    4 - Good Mates
    5 - Soul Mates truly Connected 
    """

    relation = {}
    if os.path.exists('relation_data.pkl'):
        with open('relation_data.pkl', 'rb') as f:
            relation = pickle.load(f)
    else:
        for i in range(len(guests)):
            for j in range(i + 1, len(guests)):
                relation[(guests[i], guests[j])] = int(
                    input(f"Enter relationship from 1-5 for {guests[i]} and {guests[j]}: "))
        with open('relation_data.pkl', 'wb') as f:
            pickle.dump(relation, f)

    familiarity = np.ones((15, 15)) * 5
    for i in range(len(guests)):
        for j in range(i + 1, len(guests)):
            familiarity[i][j] = relation[(guests[i], guests[j])]
            familiarity[j][i] = familiarity[i][j]

    initial_arrangement = guests

    # Use 'max' for maximizing and 'min' for minimizing total familiarity
    best_arrangement = initial_arrangement
    best_familiarity = get_total_familiarity(best_arrangement)
    for _ in tqdm(range(1000)):
        optimal_arrangement = simulated_annealing(initial_arrangement, what_you_want_to_get)
        if (what_you_want_to_get == 'min' and get_total_familiarity(optimal_arrangement) < best_familiarity) or (what_you_want_to_get == 'max' and get_total_familiarity(optimal_arrangement) > best_familiarity):
            best_arrangement = optimal_arrangement
            best_familiarity = get_total_familiarity(best_arrangement)

    print('Optimal arrangement:', best_arrangement)
    print('Total familiarity:', best_familiarity)
    display_arrangement_in_circle(best_arrangement)

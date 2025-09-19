# %% [markdown]
# ## import libraries

# %%
import numpy as np
import matplotlib.pyplot as plt

# %%
# set random seed for reproducibility
np.random.seed(42)

# %% [markdown]
# ## Define the graph (distance matrix)

# %%
cities = ["A", "B", "C", "D"]
n = len(cities)

distances = np.array([
    [0, 1, 6, 5],
    [1, 0, 3, 8],
    [6, 3, 0, 4],
    [5, 8, 4, 0]
])

# %% [markdown]
# ### Heuristic information (1 / distance)

# %%
heuristic = 1 / (distances + 1e-10)
np.fill_diagonal(heuristic, 0)
pheromone = np.ones_like(distances, dtype=float)
np.fill_diagonal(pheromone, 0)


# %% [markdown]
# ## Set Parameters

# %%
n_ants = 4
alpha = 1
beta = 2
ro = 0.1
Q = 100

# %% [markdown]
# ## Defining a function to calculate the tour length

# %%


def tour_length(tour):
    return sum(distances[tour[i], tour[(i+1) % n]] for i in range(n))


# %% [markdown]
# ## Construct one tour

# %%
def construct_solution(pheromone, heuristic, alpha, beta):
    tour = []
    unvisited = list(range(n))
    current = np.random.choice(unvisited)
    tour.append(current)
    unvisited.remove(current)

    while unvisited:
        probabilities = []
        for city in unvisited:
            tau = pheromone[current][city] ** alpha
            eta = heuristic[current][city] ** beta
            probabilities.append(tau * eta)

        probabilities = np.array(probabilities)
        probabilities /= probabilities.sum()  # normalize

        next_city = np.random.choice(unvisited, p=probabilities)
        tour.append(next_city)
        unvisited.remove(next_city)
        current = next_city

    return tour

# %% [markdown]
# ## Update pheromone matrix

# %%


def update_pheromone(pheromone, tours, lengths, Q, ro):
    # Evaporation
    pheromone *= (1 - ro)

    # Deposit
    for tour, length in zip(tours, lengths):
        for i in range(n):
            from_city = tour[i]
            to_city = tour[(i + 1) % n]  # wrap around
            pheromone[from_city][to_city] += Q / length
            pheromone[to_city][from_city] += Q / length  # symmetric update

# %% [markdown]
# ## Run one ACO iteration


# %%
tours = [construct_solution(pheromone, heuristic, alpha, beta)
         for _ in range(n_ants)]
lengths = [tour_length(t) for t in tours]
update_pheromone(pheromone, tours, lengths, Q, ro)

best_idx = np.argmin(lengths)
print("Best tour:", [cities[i] for i in tours[best_idx]])
print("Tour length:", lengths[best_idx])

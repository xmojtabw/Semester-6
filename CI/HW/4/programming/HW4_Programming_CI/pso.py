# %% [markdown]
# ## Import libraries

# %%
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# %% [markdown]
# ## Set random seed

# %%
np.random.seed(42)

# %% [markdown]
# ## Define graph (distance matrix)

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
# ## 2D coordinates for visualization

# %%
positions = np.array([
    [0, 0],
    [1, 0],
    [1, 1],
    [0, 1]
])

# %% [markdown]
# ## Heuristic and pheromone initialization

# %%
heuristic = 1 / (distances + 1e-10)
np.fill_diagonal(heuristic, 0)
pheromone = np.ones_like(distances, dtype=float)
np.fill_diagonal(pheromone, 0)

# %% [markdown]
# ## ACO parameters

# %%
n_ants = 4
alpha = 1
beta = 2
ro = 0.1
Q = 100
n_iterations = 20

# %% [markdown]
# ## Tour length function

# %%


def tour_length(tour):
    return sum(distances[tour[i], tour[(i+1) % n]] for i in range(n))

# %% [markdown]
# ## Construct solution (one tour)

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
# ## Pheromone update function

# %%


def update_pheromone(pheromone, tours, lengths, Q, ro):
    pheromone *= (1 - ro)  # evaporation
    for tour, length in zip(tours, lengths):
        for i in range(n):
            a = tour[i]
            b = tour[(i+1) % n]
            pheromone[a][b] += Q / length
            pheromone[b][a] += Q / length  # symmetric

# %% [markdown]
# ## Run ACO iterations and store data


# %%
all_tours = []
all_lengths = []
all_pheromones = []

for iteration in range(n_iterations):
    tours = [construct_solution(pheromone, heuristic, alpha, beta)
             for _ in range(n_ants)]
    lengths = [tour_length(t) for t in tours]
    update_pheromone(pheromone, tours, lengths, Q, ro)

    best_idx = np.argmin(lengths)
    best_tour = tours[best_idx]
    all_tours.append(best_tour)
    all_lengths.append(lengths[best_idx])
    all_pheromones.append(pheromone.copy())

print("Best final tour:", [cities[i] for i in all_tours[-1]])
print("Length:", all_lengths[-1])

# %% [markdown]
# ## Animate the ACO process

# %%
fig, ax = plt.subplots(figsize=(6, 6))


def init():
    ax.clear()
    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_title("ACO - Ant Movement")
    for i, (x, y) in enumerate(positions):
        ax.plot(x, y, 'ko')
        ax.text(x + 0.02, y + 0.02, cities[i], fontsize=12)
    return []


def update(frame):
    ax.clear()
    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_title(
        f"Iteration {frame+1} - Best Tour Length: {all_lengths[frame]:.2f}")

    # Draw cities
    for i, (x, y) in enumerate(positions):
        ax.plot(x, y, 'ko')
        ax.text(x + 0.02, y + 0.02, cities[i], fontsize=12)

    # Draw tour
    tour = all_tours[frame]
    for i in range(n):
        a = positions[tour[i]]
        b = positions[tour[(i+1) % n]]
        ax.plot([a[0], b[0]], [a[1], b[1]], 'b-', lw=2)

    return []


ani = FuncAnimation(fig, update, frames=n_iterations, init_func=init,
                    interval=800, blit=False, repeat=False)
plt.show()

# %% [markdown]
# ## Import libraries

# %%
import numpy as np
import matplotlib.pyplot as plt

# set the seed for np
np.random.seed(42)

# %% [markdown]
# ## Define the objective function

# %%


def objective_function(x):
    return x**2

# %% [markdown]
# ## Set PSO hyperparameters


# %%
num_particles = 10
num_iterations = 30

w = 0.5
c1 = 1.5
c2 = 1.5

lower_bound = -10
upper_bound = 10

# %% [markdown]
# ## Initialize positions and velocities

# %%
positions = np.random.uniform(lower_bound, upper_bound, num_particles)
velocities = np.zeros((num_particles))

# %% [markdown]
# ## Initialize personal bests

# %%
pbest = positions.copy()
pbest_fitness = objective_function(pbest)

# %% [markdown]
# ## Initialize global best

# %%
gbest_index = np.argmin(pbest_fitness)
gbest = pbest[gbest_index]
gbest_fitness = pbest_fitness[gbest_index]

# %% [markdown]
# ## Main PSO loop

# %%
history = []

for iter in range(num_iterations):
    for i in range(num_particles):
        r1 = np.random.rand()
        r2 = np.random.rand()

        # TODO: Update velocity
        velocities[i] = (w * velocities[i] +
                         c1 * r1 * (pbest[i] - positions[i]) +
                         c2 * r2 * (gbest - positions[i]))

        # TODO: Update position
        positions[i] = positions[i] + velocities[i]

        # Clip position to bounds
        positions[i] = np.clip(positions[i], lower_bound, upper_bound)
        # Evaluate fitness
        fitness = objective_function(positions[i])

        # TODO: Update personal best (p_best and p_best_scores) if new position is better
        if fitness < pbest_fitness[i]:
            pbest[i] = positions[i]
            pbest_fitness[i] = fitness
        # TODO: Update global best (g_best and g_best_score) if new p_best is better than g_best
            if fitness < gbest_fitness:
                gbest = pbest[i]
                gbest_fitness = fitness
    history.append(gbest_fitness)

# %%
# Final results
print(f"\nBest solution found: {gbest}")
print(f"Minimum value: f(x)= {gbest_fitness}")

# %%
# Convergence plot
plt.plot(history)
plt.title("Convergence Curve")
plt.xlabel("Iteration")
plt.ylabel("Best fitness")
plt.grid(True)
plt.show()

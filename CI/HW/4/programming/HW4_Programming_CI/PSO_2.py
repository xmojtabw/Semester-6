# %% [markdown]
# ## import package and libraries

# %%
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# %% [markdown]
# ## Load MNIST and preprocess

# %%
(X_train_full, y_train_full), _ = tf.keras.datasets.mnist.load_data()
X = X_train_full.reshape(-1, 28*28) / 255.0
y = to_categorical(y_train_full)

# Use only 3000 samples for speed
X_small, y_small = X[:3000], y[:3000]
X_train, X_val, y_train, y_val = train_test_split(
    X_small, y_small, test_size=0.2, random_state=42)

# %%


def decode_particle(p):
    neurons = [int(p[0]), int(p[1]), int(p[2])]
    activation = ['relu', 'tanh', 'sigmoid'][int(p[3]) % 3]
    dropout = float(p[4])
    return neurons, activation, dropout

# %% [markdown]
# ## Define the fitness function for PSO

# %%


def fitness(particle):
    neurons, activation, dropout = decode_particle(particle)

    model = Sequential()
    model.add(Dense(neurons[0], activation=activation, input_shape=(784,)))
    model.add(Dropout(dropout))
    model.add(Dense(neurons[1], activation=activation))
    model.add(Dropout(dropout))
    model.add(Dense(neurons[2], activation=activation))
    model.add(Dropout(dropout))
    model.add(Dense(10, activation='softmax'))

    model.compile(optimizer='adam',
                  loss='categorical_crossentropy', metrics=['accuracy'])

    history = model.fit(X_train, y_train, epochs=3, batch_size=32,
                        verbose=0, validation_data=(X_val, y_val))

    val_acc = history.history['val_accuracy'][-1]
    return -val_acc  # because we want to maximize accuracy

# %% [markdown]
# ## Set PSO hyperparameters


# %%
n_particles = 10
n_iterations = 10
w, c1, c2 = 0.5, 1.5, 1.5

bounds = np.array([
    [32, 256],     # neurons layer 1
    [32, 256],     # neurons layer 2
    [16, 128],     # neurons layer 3
    [0, 2.9999],   # activation function (0=relu,1=tanh,2=sigmoid)
    [0.0, 0.5]     # dropout
])

dim = bounds.shape[0]
positions = np.random.uniform(
    bounds[:, 0], bounds[:, 1], size=(n_particles, dim))
velocities = np.zeros_like(positions)

pbest = positions.copy()
pbest_fitness = np.array([fitness(p) for p in pbest])

gbest_index = np.argmin(pbest_fitness)
gbest = pbest[gbest_index].copy()
gbest_fitness = pbest_fitness[gbest_index]

history = [gbest_fitness]

# %% [markdown]
# ## PSO main loop

# %%
for t in range(n_iterations):
    for i in range(n_particles):
        r1 = np.random.rand(dim)
        r2 = np.random.rand(dim)

        velocities[i] = (w * velocities[i] +
                         c1 * r1 * (pbest[i] - positions[i]) +
                         c2 * r2 * (gbest - positions[i]))

        positions[i] += velocities[i]

        # Clip to bounds
        positions[i] = np.clip(positions[i], bounds[:, 0], bounds[:, 1])

        fit = fitness(positions[i])

        if fit < pbest_fitness[i]:
            pbest[i] = positions[i].copy()
            pbest_fitness[i] = fit

            if fit < gbest_fitness:
                gbest = pbest[i].copy()
                gbest_fitness = fit

    history.append(gbest_fitness)
    print(
        f"Iteration {t+1}/{n_iterations} - Best Accuracy: {-gbest_fitness:.4f}")

# %% [markdown]
# ## Show best result

# %%
neurons, activation, dropout = decode_particle(gbest)
print("Best Architecture Found:")
print("Neurons per layer:", neurons)
print("Activation:", activation)
print("Dropout:", dropout)
print("Validation Accuracy:", -gbest_fitness)

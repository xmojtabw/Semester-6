import random
import math

# --------------------------- Read TSP file ---------------------------
def read_tsp(filename):
    coords = []
    with open(filename) as f:
        for line in f:
            if line.strip() == 'EOF':
                break
            parts = line.strip().split()
            if len(parts) == 3 and parts[0].isdigit():
                x, y = float(parts[1]), float(parts[2])
                coords.append((x, y))
    return coords

# --------------------------- Distance Calculation ---------------------------
def euclidean(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def total_distance(tour, coords):
    dist = sum(euclidean(coords[tour[i]], coords[tour[(i+1) % len(tour)]]) for i in range(len(tour)))
    return dist

# --------------------------- Population Initialization ---------------------------
def create_population(size, n):
    return [random.sample(range(n), n) for _ in range(size)]

# --------------------------- Fitness Function ---------------------------
def fitness(tour, coords):
    return 1 / total_distance(tour, coords)

# --------------------------- Selection ---------------------------
def tournament_selection(pop, fitnesses, k):
    selected = random.sample(list(zip(pop, fitnesses)), k)
    return max(selected, key=lambda x: x[1])[0]

# --------------------------- Crossover Operators ---------------------------
def order_crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [-1] * size
    child[start:end] = parent1[start:end]
    pointer = end
    for gene in parent2:
        if gene not in child:
            if pointer == size:
                pointer = 0
            child[pointer] = gene
            pointer += 1
    return child

def pmx_crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = parent1[:]
    mapping = {}
    for i in range(start, end):
        child[i] = parent2[i]
        mapping[parent2[i]] = parent1[i]
    for i in range(size):
        if i >= start and i < end:
            continue
        while child[i] in mapping:
            child[i] = mapping[child[i]]
    return child

def cycle_crossover(p1, p2):
    size = len(p1)
    child = [-1] * size
    index = 0
    while -1 in child:
        start = index
        val = p1[start]
        while True:
            child[start] = p1[start]
            val = p2[start]
            start = p1.index(val)
            if child[start] != -1:
                break
        index = child.index(-1)
    return child

# --------------------------- Mutation Operators ---------------------------
def swap_mutation(tour):
    a, b = random.sample(range(len(tour)), 2)
    tour[a], tour[b] = tour[b], tour[a]
    return tour

def inversion_mutation(tour):
    a, b = sorted(random.sample(range(len(tour)), 2))
    tour[a:b] = reversed(tour[a:b])
    return tour

def scramble_mutation(tour):
    a, b = sorted(random.sample(range(len(tour)), 2))
    temp = tour[a:b]
    random.shuffle(temp)
    tour[a:b] = temp
    return tour

# --------------------------- Genetic Algorithm ---------------------------
def genetic_algorithm(filename, pop_size=100, generations=500, crossover_rate=0.9, mutation_rate=0.2, tournament_k=5):
    coords = read_tsp(filename)
    n = len(coords)
    population = create_population(pop_size, n)
    best_tour = min(population, key=lambda t: total_distance(t, coords))

    for gen in range(generations):
        fitnesses = [fitness(t, coords) for t in population]
        new_population = []

        while len(new_population) < pop_size:
            parent1 = tournament_selection(population, fitnesses, tournament_k)
            parent2 = tournament_selection(population, fitnesses, tournament_k)

            if random.random() < crossover_rate:
                child = order_crossover(parent1, parent2)
            else:
                child = parent1[:]

            if random.random() < mutation_rate:
                child = random.choice([swap_mutation, inversion_mutation, scramble_mutation])(child)

            new_population.append(child)

        population = new_population
        current_best = min(population, key=lambda t: total_distance(t, coords))
        if total_distance(current_best, coords) < total_distance(best_tour, coords):
            best_tour = current_best

        print(f"Generation {gen+1}: Best distance = {total_distance(best_tour, coords):.2f}")

    return best_tour, total_distance(best_tour, coords)

# --------------------------- Run Example ---------------------------
if __name__ == "__main__":
    best, dist = genetic_algorithm("city2.tsp")
    print("Best tour:", best)
    print("Distance:", dist)


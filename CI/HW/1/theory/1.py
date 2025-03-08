import numpy as np

# Define a 1x3 matrix (row vector)
matrix_1x3 = np.array([[0.23, 0.45, 0.67]])

# Define a 3x4 matrix
matrix_3x4 = np.array([
    [0.45, -0.12, 0.78, 0.72],
    [0.05, 0.35,-0.22 -0.85],
    [-0.55,0.11, 0.67,0.45]
])

# Perform matrix multiplication
result = np.dot(matrix_1x3, matrix_3x4)

# Print the result
print("Result of multiplication:")
print(result)


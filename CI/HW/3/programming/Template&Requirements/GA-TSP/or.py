from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import math

def create_data_model(coords):
    def euclidean(a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])
    n = len(coords)
    dist = [[int(euclidean(coords[i], coords[j])) for j in range(n)] for i in range(n)]
    return {"distance_matrix": dist, "num_vehicles": 1, "depot": 0}

def solve_tsp(coords):
    data = create_data_model(coords)
    manager = pywrapcp.RoutingIndexManager(len(data["distance_matrix"]), data["num_vehicles"], data["depot"])
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(i, j):
        return data["distance_matrix"][manager.IndexToNode(i)][manager.IndexToNode(j)]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    solution = routing.SolveWithParameters(search_parameters)
    if solution:
        index = routing.Start(0)
        route = []
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        return route


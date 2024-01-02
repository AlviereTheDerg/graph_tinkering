
import networkx as nx
import matplotlib.pyplot as plt
from coordinates.coordinates import *
from heapq import nsmallest
from tqdm import tqdm

#KNN search things
class ball_tree:
    center = None
    radius = 0
    data = []
    left = None
    right = None

    def __init__(self, data):
        self.data = data
        self.center = scale_coord(sum_coords(*data), 1 / len(data))
        furthest_point = max(data, key = lambda point: distance_between(point, self.center))
        self.radius = distance_between(furthest_point, self.center)

        if len(data) == 1:
            return
        
        self.left = ball_tree([coord for coord in data if cosine_of(self.center, furthest_point, coord) <= 0])
        self.right = ball_tree([coord for coord in data if cosine_of(self.center, furthest_point, coord) > 0])

def knn_search(ball, point, k, founds, no_self_edges=True):
    if no_self_edges and len(ball.data) == 1 and ball.data[0] == point:
        pass # ball is a leaf node representing point
    elif len(founds) == k and distance_between(point, ball.center) - ball.radius > distance_between(point, founds[-1]):
        pass # found k neighbours and the ball can't represent a node better than the worst found one so far
    elif len(ball.data) == 1: # ball is a leaf node
        founds = nsmallest(k, founds + [ball.center], key=lambda coord: distance_between(point, coord))
    else:
        first,second = (ball.left, ball.right) if distance_between(point, ball.left.center) - ball.left.radius < distance_between(point, ball.right.center) - ball.right.radius else (ball.right, ball.left)
        founds = knn_search(first, point, k, founds, no_self_edges)
        founds = knn_search(second, point, k, founds, no_self_edges)
    return founds

def create_knn_graph(data, k, no_self_edges=True):
    ball = ball_tree(data)
    graph = nx.Graph()
    for entry in tqdm(data):
        for neighbour in knn_search(ball, entry, k, [], no_self_edges):
            graph.add_edge(entry, neighbour)
    return graph

def create_random_2d_knn_graph(data_points, k, seed=None, no_self_edges=True):
    return create_knn_graph(n_random_coords(data_points, seed=seed), k, no_self_edges)

if __name__ == '__main__':
    graph = create_random_2d_knn_graph(64, 4, 4)
    nx.draw(graph, {coord:coord for coord in graph})
    plt.show()
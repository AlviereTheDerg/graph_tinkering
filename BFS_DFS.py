
import networkx as nx
from collections import deque
from graph_drawer import do_animation

def underlying_process(graph_space, graph: nx.Graph, pos, source, destination, flag: bool):
    def search() -> any:
        parents = {source:None}
        search = deque()
        search.append(source)
        while search:
            node = search.popleft() if flag else search.pop()
            for neighbour in graph[node]:
                if neighbour == destination:
                    path = [destination, node]
                    while parents[path[-1]] != None:
                        path.append(parents[path[-1]])
                    for _ in range(2): # hold for an extra frame
                        yield (parents, search, destination, path)
                    return
                if neighbour not in parents:
                    parents[neighbour] = node
                    search.append(neighbour)
            yield (parents, search, node, [])
        yield (parents, {}, destination, [])
    
    node_list = [node for node in graph]
    def draw(graph_data):
        visited, deque_data, current_investigation, path = graph_data
        colours = {item:'#000077' for item in visited}
        colours.update({item:'#0000FF' for item in deque_data})
        colours.update({item:'#AAAA00' for item in path})
        colours[current_investigation] = '#00FF00'
        colours[source] = '#FF0000'
        colours[destination] = '#AA3300'

        if flag:
            queue_positions = {item:pos+1 for pos,item in enumerate(deque_data)}
        else:
            queue_positions = {item:len(deque_data)-pos for pos,item in enumerate(deque_data)}

        nx.draw_networkx_nodes(graph, pos, node_color=list(map(lambda item:colours.get(item, "#222222"), node_list)))
        nx.draw_networkx_edges(graph, pos)
        nx.draw_networkx_labels(graph, pos, queue_positions)
    do_animation(graph_space, 400, draw, search)

def BFS_animation(graph_space, graph: nx.Graph, pos, source, destination=None):
    underlying_process(graph_space, graph, pos, source, destination, True)

def DFS_animation(graph_space, graph: nx.Graph, pos, source, destination=None):
    underlying_process(graph_space, graph, pos, source, destination, False)

if __name__ == '__main__':
    from KNN_graph_generator import create_random_2d_knn_graph
    from random import choice
    maze = create_random_2d_knn_graph(64, 4, 4)
    BFS_animation((8,8), maze, {coord:coord for coord in maze}, choice(list(maze.nodes())))
    DFS_animation((8,8), maze, {coord:coord for coord in maze}, choice(list(maze.nodes())))

    from maze_generator import generate_maze
    maze = generate_maze((4,4),5)
    BFS_animation((4,4), maze, {coord:coord for coord in maze}, (0,0), (3,3))
    DFS_animation((4,4), maze, {coord:coord for coord in maze}, (0,0), (3,3))

    maze = generate_maze((8,8),5)
    BFS_animation((8,8), maze, {coord:coord for coord in maze}, (4,4), (1,5))
    DFS_animation((8,8), maze, {coord:coord for coord in maze}, (4,4), (1,5))
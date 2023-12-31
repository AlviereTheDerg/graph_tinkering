
import networkx as nx
from collections import deque
from graph_drawer import do_animation
from maze_generator import generate_maze

def underlying_process(graph_space, graph: nx.Graph, pos, source, destination, flag: bool):
    def search() -> any:
        visited = set()
        parents = {source:None}
        search = deque()
        search.append(source)
        while search:
            node = search.popleft() if flag else search.pop()
            visited.add(node)
            for neighbour in graph[node]:
                if neighbour == destination:
                    path = [destination, node]
                    while parents[path[-1]] != None:
                        path.append(parents[path[-1]])
                    for _ in range(2): # hold for an extra frame
                        yield (visited, search, destination, path)
                    return
                if neighbour not in visited:
                    parents[neighbour] = node
                    search.append(neighbour)
            yield (visited, search, node, [])
        yield (visited, {}, destination, [])
    
    node_list = [node for node in graph]
    def draw(graph_data):
        visited, deque_data, current_investigation, path = graph_data
        colours = {item:'#000077' for item in visited}
        colours.update({item:'#0000FF' for item in deque_data})
        colours.update({item:'#AAAA00' for item in path})
        colours[source] = '#FF0000'
        colours[destination] = '#AA3300'
        colours[current_investigation] = '#00FF00'

        if flag:
            queue_positions = {item:pos+1 for pos,item in enumerate(deque_data)}
        else:
            queue_positions = {item:len(deque_data)-pos for pos,item in enumerate(deque_data)}

        nx.draw_networkx_nodes(graph, pos, node_color=list(map(lambda item:colours.get(item, "#222222"), node_list)))
        nx.draw_networkx_edges(graph, pos)
        nx.draw_networkx_labels(graph, pos, queue_positions)
    do_animation(graph_space, 400, draw, search)

def BFS_animation(graph_space, graph: nx.Graph, pos, source, destination):
    underlying_process(graph_space, graph, pos, source, destination, True)

def DFS_animation(graph_space, graph: nx.Graph, pos, source, destination):
    underlying_process(graph_space, graph, pos, source, destination, False)

if __name__ == '__main__':
    maze = generate_maze((4,4),5)
    BFS_animation((4,4), maze, {coord:coord for coord in maze}, (0,0), (3,3))
    DFS_animation((4,4), maze, {coord:coord for coord in maze}, (0,0), (3,3))
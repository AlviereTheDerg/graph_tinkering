
import networkx as nx
from heapq import nsmallest
from graph_drawer import do_animation
from coordinates.coordinates import distance_from

def underlying_process(graph_space, graph: nx.Graph, buffers_handler, pos, source, destination):
    def search() -> any:
        parents = {source:None}
        this_search = [source]
        reserves = list()
        while this_search:
            next_search = set()
            for node in this_search:
                for neighbour in graph[node]:
                    if neighbour == destination:
                        path = [destination, node]
                        while parents[path[-1]] != None:
                            path.append(parents[path[-1]])
                        print(path)
                        for _ in range(2): # hold for an extra frame
                            yield (parents, this_search, [], reserves, path)
                        return
                    if neighbour not in parents:
                        parents[neighbour] = node
                        next_search.add(neighbour)
            yield (parents, this_search, next_search, reserves, [])
            this_search,reserves = buffers_handler(next_search,reserves)
        return None

    node_list = [node for node in graph]
    def draw(graph_data):
        visited, this_search, next_search, reserves, path = graph_data
        colours = {item:'#000077' for item in visited}
        colours.update({item:'#00AAAA' for item in reserves})
        colours.update({item:'#0000FF' for item in next_search})
        colours.update({item:'#00FF00' for item in this_search})
        colours.update({item:'#AAAA00' for item in path})
        colours[source] = '#FF0000'
        colours[destination] = '#AA3300'

        nx.draw_networkx_nodes(graph, pos, node_size=90, node_color=list(map(lambda item:colours.get(item, "#222222"), node_list)))
        nx.draw_networkx_edges(graph, pos)
    do_animation(graph_space, 800, draw, search)


def beam_search_animation(graph_space, graph: nx.Graph, beam_width, pos, source, destination):
    def pure_beam(next_search, _):
        return nsmallest(beam_width, next_search, key=distance_from(destination)),[]
    underlying_process(graph_space, graph, pure_beam, pos, source, destination)

def beam_stack_search_animation(graph_space, graph: nx.Graph, beam_width, pos, source, destination):
    def beam_stack(next_search, reserves):
        next_search = sorted(next_search, key=distance_from(destination))
        reserves = sorted(reserves, key=distance_from(destination))

        diff = beam_width - len(next_search)
        if diff > 0:
            next_search += reserves[0:diff]
            reserves = reserves[diff:]
        elif diff < 0:
            reserves += next_search[diff:]
            next_search = next_search[0:diff]
        return next_search, reserves
    underlying_process(graph_space, graph, beam_stack, pos, source, destination)

if __name__ == '__main__':
    from KNN_graph_generator import create_knn_graph
    from coordinates.coordinates import n_random_coords
    data = n_random_coords(250, max_distance=10, seed=4)
    source = min(data, key=distance_from(tuple()))
    destination = max(data, key=distance_from(tuple()))

    graph = create_knn_graph(data, 5)
    beam_search_animation((6,6), graph, 5, {coord:coord for coord in graph}, source, destination)
    beam_stack_search_animation((6,6), graph, 5, {coord:coord for coord in graph}, source, destination)
    
    graph = create_knn_graph(data, 3)
    beam_search_animation((6,6), graph, 5, {coord:coord for coord in graph}, source, destination)
    beam_stack_search_animation((6,6), graph, 5, {coord:coord for coord in graph}, source, destination)
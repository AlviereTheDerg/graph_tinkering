
import matplotlib.pyplot as plt
import matplotlib.animation

def do_animation(graph_space, interval, graph_drawer, graph_generator):
    fig, ax = plt.subplots(figsize=graph_space)
    ax.set_xticks([])
    ax.set_yticks([])

    def on_close(event):
        plt.close()
    fig.canvas.mpl_connect('close_event', on_close)
    
    def update(graph_data):
        ax.clear()
        if type(title_data := graph_drawer(graph_data)) != type(None):
            ax.set_title(*title_data)

    ani = matplotlib.animation.FuncAnimation(fig, func=update, frames=graph_generator, interval=interval, repeat=True, cache_frame_data=False)
    plt.show()

if __name__ == '__main__':
    import networkx as nx
    import maze_generator
    from collections import deque

    graph = maze_generator.generate_maze((4,4),4)
    node_list = [node for node in graph]
    print(node_list)
    pos = {node:node for node in graph}
    source = (0,0)
    destination = (3,3)

    # hand over: visited list, items in search queue and their positions, what node is currently being investigated
    def graph_generator() -> any:
        visited = set()
        search_queue = deque()
        search_queue.append(source)
        while search_queue:
            node = search_queue.popleft()
            visited.add(node)
            for neighbour in graph[node]:
                if neighbour == destination:
                    for _ in range(2): # hold for an extra frame
                        yield (visited, {item:pos for pos,item in enumerate(search_queue)},node)
                    return
                if neighbour not in visited:
                    search_queue.append(neighbour)
            yield (visited, {item:pos for pos,item in enumerate(search_queue)},node)
        yield (visited, {}, destination)

    def graph_drawer(graph_data):
        visited, queue_positions, current_investigation = graph_data
        colours = {item:'#000077' for item in visited}
        colours.update({item:'#0000FF' for item in queue_positions})
        colours[source] = '#FF0000'
        colours[destination] = '#AA3300'
        colours[current_investigation] = '#00FF00'

        nx.draw_networkx_nodes(graph, pos, node_color=list(map(lambda item:colours.get(item, "#222222"), node_list)))
        nx.draw_networkx_edges(graph, pos)
        nx.draw_networkx_labels(graph, pos, queue_positions)
    do_animation((4,4), 400, graph_drawer, graph_generator)

import networkx as nx
import matplotlib.pyplot as plt
import random

def generate_maze(dimensions, seed=None) -> nx.Graph:
    graph = nx.grid_graph(dimensions)
    random.seed(seed)

    in_group = {random.choice(list(graph.nodes))}
    out_group = set(graph.nodes) - in_group

    output = nx.Graph()
    while len(out_group) > 0:
        this_walk = [random.choice(list(out_group))]
        this_walk_visits = {this_walk[-1]}
        while this_walk[-1] not in in_group:
            next_steps = [node for node in graph[this_walk[-1]] if node not in this_walk_visits]
            if len(next_steps) > 0:
                this_walk.append(random.choice(next_steps))
                this_walk_visits.add(this_walk[-1])
            else:
                this_walk.pop()
        
        output.add_edges_from([(this_walk[i], this_walk[i+1]) for i in range(len(this_walk) - 1)])
        in_group.update(this_walk)
        out_group -= in_group
    return output

if __name__ == '__main__':
    print("Basic showcase")
    G = generate_maze((12,12), 4) # chosen by random dice roll
    pos = {v:v for v in G.nodes}
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_nodes(G, pos, node_size=30)
    plt.axis("off")
    plt.savefig("result.png")
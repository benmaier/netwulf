from netwulf.tools import bind_positions_to_network
import networkx as nx

if __name__ == "__main__":
    import pprint 
    pp = pprint.PrettyPrinter(indent=4)

    G = nx.Graph()
    G.add_nodes_from(range(10))
    G.add_nodes_from("abcde")
    G.add_edges_from([("a","b")])

    from netwulf import visualize
    props, config = visualize(G)

    pp.pprint(props)
    pp.pprint(config)
    bind_positions_to_network(G, props)
    visualize(G, config=config)

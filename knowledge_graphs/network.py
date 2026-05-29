try:
    import networkx as nx
except ImportError:
    print("Error: networkx is not installed.")
    print("Please run: pip install networkx")
    import sys
    sys.exit(1)

# Initialize directed graph
G = nx.DiGraph()

# Add edges
G.add_edge("Kyoto", "Buddhist Kaiseki", relation="offers_dish")
G.add_edge("Buddhist Kaiseki", "Green Tea", relation="pairs_with")
G.add_edge("Kyoto", "Kinkaku-ji Temple", relation="has_attraction")

print("Kyoto connections:")
for target in G.successors("Kyoto"):
    rel = G.get_edge_data("Kyoto", target)["relation"]
    print("-", target, f"({rel})")

print("\nPath exists from Kyoto to Green Tea:")
path_exists = nx.has_path(G, "Kyoto", "Green Tea")
print(path_exists)

if path_exists:
    print("\nShortest path:")
    path = nx.shortest_path(G, "Kyoto", "Green Tea")
    print(path)

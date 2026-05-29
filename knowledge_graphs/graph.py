class SimpleKnowledgeGraph:
    def __init__(self):
        # List of triples
        self.triples = []

    def add_fact(self, subject, predicate, obj):
        # Add a triple
        self.triples.append((subject, predicate, obj))

    def find_facts(self, s=None, p=None, o=None):
        # Query matching triples
        results = []
        for subject, predicate, obj in self.triples:
            if s is not None and subject != s:
                continue
            if p is not None and predicate != p:
                continue
            if o is not None and obj != o:
                continue
            results.append((subject, predicate, obj))
        return results

    def find_path(self, start, end, visited=None):
        # Find connection path
        if visited is None:
            visited = set()
        if start == end:
            return [start]
        visited.add(start)
        for s, p, o in self.find_facts(s=start):
            if o not in visited:
                path = self.find_path(o, end, visited)
                if path:
                    return [start] + path
        return None

    def get_neighbors(self, node):
        # Get direct connections
        neighbors = set()
        for s, p, o in self.triples:
            if s == node:
                neighbors.add(o)
            elif o == node:
                neighbors.add(s)
        return list(neighbors)

    def get_all_nodes(self):
        # Get all unique nodes
        nodes = set()
        for s, p, o in self.triples:
            nodes.add(s)
            nodes.add(o)
        return list(nodes)

if __name__ == "__main__":
    kg = SimpleKnowledgeGraph()

    # Load facts
    kg.add_fact("Kyoto", "offers_dish", "Buddhist Kaiseki")
    kg.add_fact("Buddhist Kaiseki", "is_suitable_for", "Vegetarian")
    kg.add_fact("Buddhist Kaiseki", "pairs_with", "Green Tea")
    kg.add_fact("Kyoto", "has_attraction", "Kinkaku-ji Temple")
    kg.add_fact("Kinkaku-ji Temple", "belongs_to", "Culture")

    # Run queries
    print("Dishes in Kyoto:")
    for s, p, o in kg.find_facts(s="Kyoto", p="offers_dish"):
        print("-", o)
        
    print("\nPairings for Buddhist Kaiseki:")
    for s, p, o in kg.find_facts(s="Buddhist Kaiseki", p="pairs_with"):
        print("-", o)

    print("\nConnection from Kyoto to Green Tea:")
    path = kg.find_path("Kyoto", "Green Tea")
    print(path)

    print("\nNeighbors of Buddhist Kaiseki:")
    print(kg.get_neighbors("Buddhist Kaiseki"))

    print("\nAll nodes in graph:")
    print(kg.get_all_nodes())

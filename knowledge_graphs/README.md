# Knowledge Graph 

## Overview

This project introduces the fundamentals of **Knowledge Graphs (KGs)** using Python. A Knowledge Graph represents information as connected entities and relationships, allowing systems to discover and reason about connections between concepts.

The project includes two implementations:

* A simple Knowledge Graph built with pure Python
* A graph-based implementation using NetworkX

## Project Structure

### `graph.py`

A basic Knowledge Graph implementation using Python data structures.

Features:

* Store information as triples
* Add and query facts
* Explore relationships between entities

### `network.py`

A Knowledge Graph implementation using the NetworkX library.

Features:

* Node and edge creation
* Path discovery
* Graph traversal
* Connectivity analysis

## Key Concepts

* **Entities**: Objects or concepts such as cities, foods, or attractions.
* **Relationships**: Connections between entities.
* **Triples**: Information stored as `(Subject, Predicate, Object)`.
* **Graph Traversal**: Discovering related concepts by following connections in the graph.

Example:

```text
(Kyoto, offers_dish, Kaiseki)
(Kaiseki, pairs_with, Green Tea)
```

## Features

* Triple-based knowledge representation
* Relationship modeling
* Graph traversal and path discovery
* Semantic querying
* Pure Python implementation
* NetworkX-based graph implementation

## Running the Project

Run the Pure Python version:

```bash
python simple.py
```

Run the NetworkX version:

```bash
python network.py
```

Install NetworkX if needed:

```bash
pip install networkx
```

## Conclusion

This project demonstrates how Knowledge Graphs can represent connected information and support intelligent reasoning. It provides both a beginner-friendly Python implementation and a more advanced graph-based approach using NetworkX.

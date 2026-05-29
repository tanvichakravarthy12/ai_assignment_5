# Adversarial Game Search Algorithms

This project executes and compares four AI search algorithms used for decision-making in games:

- Minimax Search
- Alpha-Beta Pruning
- Heuristic Alpha-Beta Search
- Monte Carlo Tree Search 

The algorithms are evaluated on two classic games:

- Tic-Tac-Toe
- Connect 4

## Structure

### search_algos_games.py
Contains the game logic, including board representation, legal moves, move execution, win and draw detection and terminal state checking

### search_algos.py
Implements the 4 search algorithms mentioned above.

### search_algos_testcases.py
Provides automated tests for the game mechanism and search algorithm correctness


## Algorithms Implemented

### Minimax
A complete game-tree search algorithm that guarantees optimal play by exploring all possible future states.

### Alpha-Beta Pruning
An optimized version of Minimax that eliminates branches that cannot influence the final decision, reducing computation time.

### Heuristic Alpha-Beta Search
Uses depth-limited search and a heuristic evaluation function to estimate board quality, making larger games such as Connect Four practical.

### Monte Carlo Tree Search 
A simulation-based algorithm that evaluates moves through repeated random playouts and statistical analysis.

## Testing

The project includes **10 test cases** covering:

- Legal move generation
- Win detection
- Draw detection
- Terminal state recognition
- Offensive move selection
- Defensive move blocking
- Game-specific mechanics

| Category | Tests |
|----------|-------|
| Tic-Tac-Toe | 5 |
| Connect 4 | 5 |
| Total | 10 |


## Running the Project

### Run All Tests

```bash
python search_algos_testcases.py
```

### Run Interactive Mode

```bash
python search_algos_testcases.py play
```

## Conclusion

This project demonstrates four fundamental AI search techniques for adversarial games. The implementation highlights the trade-offs between optimality, efficiency, and scalability:

- **Minimax** provides optimal decisions but is computationally expensive.
- **Alpha-Beta Pruning** improves efficiency while preserving optimality.
- **Heuristic Alpha-Beta** enables practical search in larger games.
- **MCTS** offers a flexible simulation-based approach for complex search spaces.

Together, these algorithms showcase key techniques used in modern game-playing AI systems.

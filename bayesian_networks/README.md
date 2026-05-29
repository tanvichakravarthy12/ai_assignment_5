# Bayesian Network for Student Performance

## Overview

This project demonstrates the basics of **Bayesian Networks** using Python. Bayesian Networks are probabilistic graphical models that represent relationships between variables and allow reasoning under uncertainty.

The project models student academic performance and performs probability-based inference using observed evidence.

## Project Structure

### `example.py`

Implements the Bayesian Network, including:

* Random variables
* Conditional Probability Tables 
* Probabilistic inference

## Network Model

The network contains the following variables:

* Difficulty
* Intelligence
* Grade
* SAT Score
* Recommendation Letter

Relationships:

```text
Difficulty → Grade
Intelligence → Grade
Intelligence → SAT
Grade → Letter
```

## Features

* Bayesian Network representation
* Directed Acyclic Graph (DAG) structure
* Conditional Probability Tables (CPTs)
* Probabilistic reasoning
* Exact inference
* Student performance prediction example

## How It Works

1. Define variables and their dependencies.
2. Create conditional probability tables.
3. Provide evidence to the network.
4. Perform Bayesian inference.
5. Display the resulting probabilities.

## Running the Project

```bash
python example.py
```

## Example Query

Given a student's grade or recommendation letter, the network can estimate the probability of related variables such as intelligence or course difficulty.

## Conclusion

This project provides a simple introduction to Bayesian Networks and probabilistic reasoning, showing how uncertainty can be modeled and analyzed using graph-based representations.

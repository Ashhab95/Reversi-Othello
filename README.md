# Reversi Othello

<p align="center">
  <img src="https://t4.ftcdn.net/jpg/00/90/53/03/240_F_90530312_4Mg3HCsCMW91NVHKWNlBaRo8F5pHhN3c.jpg?w=690&h=388&c=crop" alt="Reversi Othello Image">
</p>

## Introduction

This project involves the development of an AI agent for Reversi Othello, a strategic two-player game played on an M×M board. The goal of the project was to create a competitive AI capable of making intelligent moves using advanced algorithms and heuristics. The core algorithm implemented is Minimax, enhanced with Alpha-Beta Pruning and Iterative Deepening Search (IDS) to balance computational efficiency and depth exploration.

## Setup

To set up the game, clone this repository and install the dependencies:

```bash
pip install -r requirements.txt
```

## Playing a Game

To start playing a game, run the simulator and specify the agents:

```bash
python simulator.py --player_1 random_agent --player_2 random_agent
```

This will initiate a random game board of size NxN and run two agents of the `RandomAgent` class.

## Visualizing a Game

To visualize game moves, use the `--display` flag and adjust the delay using `--display_delay`:

```bash
python simulator.py --player_1 random_agent --player_2 random_agent --display
```

## Play on Your Own

You can take control of one side by using the `human_agent`:

```bash
python simulator.py --player_1 human_agent --player_2 random_agent --display
```

## Autoplaying Multiple Games

To evaluate agents fairly, you can autoplay multiple games by using the `--autoplay` flag and specifying the number of games with `--autoplay_runs`:

```bash
python simulator.py --player_1 random_agent --player_2 random_agent --autoplay --autoplay_runs 100
```

## Creating and Testing Custom Agents

You can create your own agents and test them against existing ones:

1. Copy the `student_agent.py` file to create a new agent.
2. Change the decorator and class name appropriately.
3. Import the new agent in the `__init__.py` file in the `agents/` directory.
4. Run the simulator with your new agents to test them.

```bash
python simulator.py --player_1 student_agent --player_2 custom_agent --display
```

---

## Agent Design

The AI agent uses Minimax with Alpha-Beta Pruning and Iterative Deepening Search (IDS). Below is an overview of the design and heuristics:

### 1. Minimax Algorithm
The Minimax algorithm systematically evaluates all possible moves, alternating between maximizing the agent’s advantage and minimizing the opponent’s.

### 2. Alpha-Beta Pruning
Alpha-Beta Pruning reduces the number of nodes evaluated by eliminating branches that cannot influence the final decision, allowing deeper exploration within the time limit.

### 3. Iterative Deepening Search (IDS)
IDS incrementally increases the search depth while adhering to a strict time limit of 1.9 seconds per move. If the time limit is reached, the best move from the last completed depth is selected.

---

## Heuristics

### Corner Control
Corners are stable positions that, once captured, cannot be flipped. This heuristic assigns a weight of +10 for each corner controlled by the agent and -10 for each corner controlled by the opponent.

### Mobility
Mobility measures the difference in the number of valid moves available to the agent and the opponent. Greater mobility ensures flexibility and better control over the game.

### Blocking
Blocking involves restricting the opponent’s access to critical areas like corners and edges. This heuristic penalizes moves that allow the opponent to gain positional advantage.

### Dynamic Weight Assignment
The importance of each heuristic changes based on the game stage:

- **Early Game:** Emphasizes mobility and blocking.
- **Mid-Game:** Focuses on corner control and maintaining flexibility.
- **Late Game:** Prioritizes corner control and maximizing the final disc count.

---

## Quantitative Performance Analysis

### Win Rate
The agent achieved:
- **95-100% win rate** against random agents.
- **80-90% win rate** against average human players.
- **70-80% win rate** against competitive agents using simpler strategies.

### Depth and Breadth Analysis
- In early stages, the agent reaches depths of 3-7, while in mid-to-late stages, it explores depths of 2-5 due to increased branching.
- Breadth varies throughout the game, peaking in the mid-game with up to 500 moves evaluated.

### Board Size
As board size increases, the agent’s search depth decreases due to the increased number of possible positions. The agent maintains efficiency by prioritizing moves using Alpha-Beta Pruning and ordering moves based on heuristics.

---

## Future Improvements

1. **Transposition Table:** Implementing a hash table to store previously evaluated game states could reduce recomputation and improve pruning efficiency.
2. **Parallelization:** Distributing computations across multiple processors could significantly speed up the search process.
3. **Advanced Heuristics:** Adding new heuristics such as Parity, Stability, and Edge Stability.
4. **Reinforcement Learning:** Exploring Q-Learning or Deep Neural Networks to replace manual heuristics with learned evaluation functions.

---

## Full API

```bash
python simulator.py -h
usage: simulator.py [-h] [--player_1 PLAYER_1] [--player_2 PLAYER_2]
                    [--board_size BOARD_SIZE] [--display]
                    [--display_delay DISPLAY_DELAY]

optional arguments:
  -h, --help            show this help message and exit
  --player_1 PLAYER_1
  --player_2 PLAYER_2
  --board_size BOARD_SIZE
  --display
  --display_delay DISPLAY_DELAY
  --autoplay
  --autoplay_runs AUTOPLAY_RUNS
```

---

## About

Developed by Kazi Ashhab Rahman [kazi.a.rahman@mail.mcgill.ca].

---

## License

[MIT](LICENSE)

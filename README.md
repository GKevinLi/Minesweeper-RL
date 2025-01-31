# Minesweeper-RL
A Minesweeper Reinforcement Learning project

# Overview
This Minesweeper agent was trained on a 10x10 grid with 10 random mines (Google Minesweeper Easy Mode). In this gamemode, it achieved a winrate of 70.9% after training for 15000 games. The code for my custom Minesweeper environment and for the training of the model are both included. Some of it is a bit scuffed as of right now, but I'm hoping to make some improvements soon. The files contained in this repository include:
- Image Files: Images for rendering the Minesweeper game board for manual play and the evaluation mode
- Models: Saved PyTorch models of the agent at various stages of its training, with a 5000 game model, 10000 game model, and 15000 game model. The 15000 game model achieved the best results in testing.
- Gym: The Gymnasium Environment for the Minesweeper game. It is imported locally with import minesweeper_env.
- eval.py: Code for evaluation of the model. Default evaluation is set to 100 games.
- main.py: Code for training the model. Defualt training episodes is set to 20,000 games. This takes several hours, so training episode number can be adjusted in the code.
- minesweeper.py: Main code for rendering and simulating Minesweeper.
- OldMinesweeperCode.py: Code for playing Minesweeper in manual mode. This mode includes flag and chording functionalities.

# Agent Architecture
The agent I used is a Deep Q-Learning (DQN) agent with a convolutional neural network determining the Q-values. The input for the model is a 10x10 tensor, representing all possible states of the Minesweeper board. To represent states, 0-8 were used for tiles with num of adjacent mines, -5 was used for uncleared tiles, and -10 was used for mines.
Outputs are represented as one 10x10 matrix, representing the Q-value for each tile. 

The neural network is comprised of 5 Conv2d layers with 64 3x3 kernels each (to represent all adjacent squares). All Conv2d layers are padded to ensure that each layer is the same size.

# Training

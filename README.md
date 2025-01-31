# Minesweeper-RL
A Minesweeper Reinforcement Learning project

## Overview
This Minesweeper agent was trained on a 10x10 grid with 10 random mines (Google Minesweeper Easy Mode). In this gamemode, it achieved a winrate of 70.9% after training for 15000 games. The code for my custom Minesweeper environment and for the training of the model are both included. Some of it is a bit scuffed as of right now, but I'm hoping to make some improvements soon. The files contained in this repository include:
- Image Files: Images for rendering the Minesweeper game board for manual play and the evaluation mode
- Models: Saved PyTorch models of the agent at various stages of its training, with a 5000 game model, 10000 game model, and 15000 game model. The 15000 game model achieved the best results in testing.
- Gym: The Gymnasium Environment for the Minesweeper game. It is imported locally with import minesweeper_env.
- eval.py: Code for evaluation of the model. Default evaluation is set to 100 games.
- main.py: Code for training the model. Defualt training episodes is set to 20,000 games. This takes several hours, so training episode number can be adjusted in the code.
- minesweeper.py: Main code for rendering and simulating Minesweeper.
- OldMinesweeperCode.py: Code for playing Minesweeper in manual mode. This mode includes flag and chording functionalities.

## Agent Architecture
The agent I used is a Deep Q-Learning (DQN) agent with a convolutional neural network determining the Q-values. The input for the model is a 10x10 tensor, representing all possible states of the Minesweeper board. To represent states, 0-8 were used for tiles with num of adjacent mines, -5 was used for uncleared tiles, and -10 was used for mines.
Outputs are represented as one 10x10 matrix, representing the Q-value for each tile. 

The neural network is comprised of 5 Conv2d layers with 64 3x3 kernels each (to represent all adjacent squares). All Conv2d layers are padded to ensure that each layer is the same size. I also used two different models, a policy model and a target model, to improve training. Experience replay with a batch size of 128 was used to optimize the model with the Smooth L1 Loss function.

## Minesweeper Environment Implementation
I implemented the Minesweeper environment to as closely match real Minesweeper as possible. In the manual play version, all functionalities are implemented, such as flagging and chording, while these were removed from the Minesweeper version the agent trained on due to complexity issues. In this version, the only action the agent can take is uncovering tiles. Mines are dispersed randomly throughout the map, with the [5][5] position in the game representation array intentionally left clear of a mine so the agent won't die on the first click due to bad luck. 

## Training and Reward Structure
For the models provided, the agent was trained on 15000 games over around 6 hours on my slow-ass computer. The hyperparameters I used are in the code, I am not putting them here (i'm too lazy). If you really care about that kind of stuff, go find it yourself.

I stole the reward structure off of this repository (https://github.com/AlexMGitHub/Minesweeper-DDQN/tree/master). A reward of 1 is given for a win, 0.3 is given for making progress (uncovering an undiscovered tile), -0.3 is given for clicking on an already discovered tile, -0.3 is given for guessing (clicking on a tile with no adjacent revealed tiles), and -1 is given for a loss (clicking on a mine). The game ends when the agent wins, loses, or exceeds the 50 move turn limit.

## Issues and Future Improvements
I'm not gonna lie, this code is barely functional. A lot of general code organization is needed. The trained models also have some issues with repeating the same moves over and over again even though they aren't making progress, although I think this may be corrected with more training time. Apart from these, though, I'm quite happy with how this turned out.

There are many possible improvements to be made for my approach. First of all, I did minimal hyperparameter tuning, as I used many of the same hyperparameters from the repository I stole the reward structure off of. As my task is easier than their project, changing the hyperparameters would likely lead to increased performance. Other improvements such as longer training and even modifying the model structure are also possible in the future.

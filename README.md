# Minesweeper-RL
A Minesweeper Reinforcement Learning project

# Overview
This Minesweeper agent was trained on a 10x10 grid with 10 random mines (Google Minesweeper Easy Mode). In this gamemode, it achieved a winrate of ~75% after training for 15000 games. The code for my custom Minesweeper environment and for the training of the model are both included. Some of it is a bit scuffed as of right now, but I'm hoping to make some improvements soon. The files contained in this repository include:
- Image Files: Images for rendering the Minesweeper game board for manual play and the evaluation mode
- Models: Saved PyTorch models of the agent at various stages of its training, with a 5000 game model, 10000 game model, and 15000 game model. The 15000 game model achieved the best results in testing.
- Gym: The Gymnasium Environment for the Minesweeper game. It is imported locally

# Agent Architecture
The agent I used is a Deep Q-Learning (DQN) agent with a convolutional neural network determining the Q-values. 

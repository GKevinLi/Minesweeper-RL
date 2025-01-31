import gymnasium as gym
import math
import pygame
import random
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple, deque
from itertools import count

import numpy
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import minesweeper_env

from minesweeper import clear
from minesweeper import setup
from minesweeper import getObs
from minesweeper import evalAction
from minesweeper import isGameFinished
from minesweeper import renderAuto
from minesweeper import renderStepAuto
from minesweeper import getClickedArr
from minesweeper import getArr

device = torch.device(
    "cuda" if torch.cuda.is_available() else
    "mps" if torch.backends.mps.is_available() else
    "cpu"
)
running = True
class DQN(nn.Module):

    def __init__(self, n_observations, n_actions):
        super(DQN, self).__init__()
        # self.layer1 = nn.Linear(n_observations, 128)
        self.layer1 = nn.Conv2d(1, 64, 3, padding='same')
        self.layer2 = nn.Conv2d(64, 64, 3, padding='same')
        self.layer3 = nn.Conv2d(64, 64, 3, padding='same')
        self.layer4 = nn.Conv2d(64, 64, 3, padding='same')
        self.layer5 = nn.Conv2d(64, 1, 1)
        # self.layer2 = nn.Linear(128, 128)
        # self.layer3 = nn.Linear(128, n_actions)

    # Called with either one element to determine next action, or a batch
    # during optimization. Returns tensor([[left0exp,right0exp]...]).
    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        x = F.relu(self.layer3(x))
        x = F.relu(self.layer4(x))
        return self.layer5(x)
env = gym.make('minesweeper_env/Minesweeper-v0')



obs_space_dims = gym.spaces.utils.flatdim(env.observation_space)

action_space_dims = gym.spaces.utils.flatdim(env.action_space)    

model = DQN(obs_space_dims, action_space_dims).to(device)
model.load_state_dict(torch.load("Models/15000.pt"))
model.eval()
winNum = 0


for i in range(100):


    setup()
    result = (renderAuto(model))
    if(result == True):
        winNum += 1
    print(winNum, i)    
        
print(winNum)
# for i in range(1000):

#     renderStepAuto()
# board = getObs()
# board = numpy.array(board, dtype="float32")
# board = torch.tensor(board)
# board = board.reshape(1, 10, 10)
# coordX = 0
# coordY = 0
# # print(board)
# temp = model(board)
# temp = temp.flatten()
# # print(temp)
# # print(temp.max(0))

# for i in range(100):
    
#         if temp[i].item() == temp.max(0).values:
#             coordX = i % 10
#             coordY = int(i / 10)
            
# print(coordX, coordY)
# evalAction(coordX, coordY, 0)
# print(getObs())
# print(temp)
# for i in range(1000):

#     renderStepAuto()

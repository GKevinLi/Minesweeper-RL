import gymnasium as gym
import math
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


# set up matplotlib
is_ipython = 'inline' in matplotlib.get_backend()
if is_ipython:
    from IPython import display

plt.ion()

# if GPU is to be used
device = torch.device(
    "cuda" if torch.cuda.is_available() else
    "mps" if torch.backends.mps.is_available() else
    "cpu"
)

Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))


class ReplayMemory(object):

    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)

    def push(self, *args):
        """Save a transition"""
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

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

def standardize(tensor):
    mean = tensor.mean()
    std = tensor.std()
    return (tensor - mean) / std   
BATCH_SIZE = 128
GAMMA = 0.90
EPS_START = 0.9
EPS_END = 0.005
EPS_DECAY = 1000
TAU = 0.005
LR = 0.001   
    
env = gym.make('minesweeper_env/Minesweeper-v0')



obs_space_dims = gym.spaces.utils.flatdim(env.observation_space)
state, info = env.reset()
action_space_dims = gym.spaces.utils.flatdim(env.action_space)

policy_net = DQN(obs_space_dims, action_space_dims).to(device)
target_net = DQN(obs_space_dims, action_space_dims).to(device)
target_net.load_state_dict(policy_net.state_dict())

optimizer = optim.AdamW(policy_net.parameters(), lr=LR, amsgrad=True)
memory = ReplayMemory(10000)

steps_done = 0
# state = env.observation_space.sample()
# # state = state.flatten()
# state = numpy.array(state, dtype="float32")
# state = torch.tensor(state)
# state = state.reshape(1, 10, 10)
# # state = state.float()
# # state = state.flatten()
# print(state)

# temp = policy_net(state)
# print(temp)
# # temp = torch.clamp(temp, min=0.01, max=0.99)
# # temp = standardize(temp) * 1
# # print(temp)
# # temp = torch.sigmoid(temp)
# # print(temp)
# # tempArr = [temp[0].item(), temp[1].item(), temp[2].item()]
# # print(tempArr)
# # tempArr[0] = tempArr[0] * 10
# # tempArr[1] = tempArr[1] * 10
# # tempArr[2] = tempArr[2] * 2
# # temp = torch.tensor(tempArr, dtype=torch.int32)

# # print(temp)
# print(torch.tensor(env.action_space.sample(), device=device, dtype=torch.float))

def select_action(state):
    state = state.flatten()
    state = numpy.array(state, dtype="float32")
    state = torch.tensor(state)
    global steps_done
    sample = random.random()
    eps_threshold = EPS_END + (EPS_START - EPS_END) * \
        math.exp(-1. * steps_done / EPS_DECAY)
    steps_done += 1
    if sample > eps_threshold:
        with torch.no_grad():
            # t.max(1) will return the largest column value of each row.
            # second column on max result is index of where max element was
            # found, so we pick action with the larger expected reward.
            state = state.reshape(1, 10, 10)
            temp = policy_net(state)
            # print(temp)
            # temp = torch.clamp(temp, min=0.01, max=0.99)
            # temp = standardize(temp)
            # temp = torch.sigmoid(temp)
            
            # tempArr = [temp[0].item(), temp[1].item(), temp[2].item()]
            
            
            # tempArr[0] = tempArr[0] * 10
            # tempArr[1] = tempArr[1] * 10
            # tempArr[2] = tempArr[2] * 2
            # temp = torch.tensor(tempArr, dtype=torch.int32)
            return temp
    else:
        tempArr = [random.randint(0, 9), random.randint(0, 9), random.randint(0, 1)]
        return torch.tensor(env.action_space.sample(), device=device, dtype=torch.float)


episode_durations = []


def plot_durations(show_result=False):
    plt.figure(1)
    durations_t = torch.tensor(episode_durations, dtype=torch.float)
    if show_result:
        plt.title('Result')
    else:
        plt.clf()
        plt.title('Training...')
    plt.xlabel('Episode')
    plt.ylabel('Duration')
    # plt.plot(durations_t.numpy())
    # # Take 100 episode averages and plot them too
    # if len(durations_t) >= 100:
    #     means = durations_t.unfold(0, 100, 1).mean(1).view(-1)
    #     means = torch.cat((torch.zeros(99), means))
    #     plt.plot(means.numpy())

    # plt.pause(0.001)  # pause a bit so that plots are updated
    # if is_ipython:
    #     if not show_result:
    #         display.display(plt.gcf())
    #         display.clear_output(wait=True)
    #     else:
    #         display.display(plt.gcf())
            
            
            
def optimize_model():
    if len(memory) < BATCH_SIZE:
        return
    transitions = memory.sample(BATCH_SIZE)
    # Transpose the batch (see https://stackoverflow.com/a/19343/3343043 for
    # detailed explanation). This converts batch-array of Transitions
    # to Transition of batch-arrays.
    batch = Transition(*zip(*transitions))
    # print(batch)
    # Compute a mask of non-final states and concatenate the batch elements
    # (a final state would've been the one after which simulation ended)
    non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                          batch.next_state)), device=device, dtype=torch.bool)
    non_final_next_states = torch.cat([s for s in batch.next_state
                                                if s is not None])
   
    # print(non_final_next_states)
    state_batch = torch.cat(batch.state)
    
    
    action_batch = torch.cat(batch.action)
    
    reward_batch = torch.cat(batch.reward)
    # print(reward_batch)
    
    state_batch = state_batch.reshape(128, 1, 10, 10)
    action_batch = action_batch.reshape(128, 100)
    # reward_batch = action_batch.reshape(128, 100)
    new_action_batch = action_batch.max(1).indices
    new_action_batch = new_action_batch.reshape(128, 1)
    # print(new_action_batch.size())
    # print(policy_net(state_batch).size())
    # print(state_batch)
    # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
    # columns of actions taken. These are the actions which would've been taken
    # for each batch state according to policy_net
    # state_action_values = policy_net(state_batch).gather(0, action_batch)
    
    
    state_action_values = policy_net(state_batch)
    state_action_values = state_action_values.reshape(128, 100)
    state_action_values = state_action_values.gather(1, new_action_batch)
    # Compute V(s_{t+1}) for all next states.
    # Expected values of actions for non_final_next_states are computed based
    # on the "older" target_net; selecting their best reward with max(1).values
    # This is merged based on the mask, such that we'll have either the expected
    # state value or 0 in case the state was final.
    
    next_state_values = torch.zeros(BATCH_SIZE, device=device)
    
    with torch.no_grad():
        # print(non_final_next_states.size()[0])
        non_final_next_states = non_final_next_states.reshape(non_final_next_states.size()[0], 1, 10, 10)
        # print(target_net(non_final_next_states).size())
        next_state_values[non_final_mask] = target_net(non_final_next_states).reshape(non_final_next_states.size()[0], 100).max(1).values
        # print(next_state_values)
        # print(reward_batch)
    # Compute the expected Q values
    
    expected_state_action_values = (next_state_values * GAMMA) + reward_batch
    # print(reward_batch.flatten())
    # print(state_action_values.flatten())
    # print(expected_state_action_values.flatten())
    # Compute Huber loss
    # print(state_action_values)
    # print(expected_state_action_values.unsqueeze(1))
    criterion = nn.SmoothL1Loss()
    loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))
    # print(loss)
    # Optimize the model
    optimizer.zero_grad()
    loss.backward()
    # In-place gradient clipping
    torch.nn.utils.clip_grad_value_(policy_net.parameters(), 100)
    optimizer.step()
    return expected_state_action_values
 
 
output_dist = numpy.zeros((10,10))
output_dist_2 = [0,0]  
total_reward_sum = 0
total_reward_sum2 = 0
mine_ratio_sum = 0
count_len = 0
tempVal2 = []
if torch.cuda.is_available() or torch.backends.mps.is_available():
    num_episodes = 150
else:
    num_episodes = 20001

for i_episode in range(num_episodes):
    # Initialize the environment and get its state
    state, info = env.reset()
    state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
    # state = [[0]]
    # # state = state.reshape(1, 1)
    # state[0][0] = newState
    # state = torch.tensor(state) 
    # print(state)
    # print(state)
    reward_sum = 0
    
    for t in count():
        
        action = select_action(state)
        action = action.reshape(10, 10)
        
        max = -1000 
        maxIndex = [0, 0]
        for i in range(10):
            for j in range(10):
                if action[i][j].item() >= max:
                    maxIndex[0] = i
                    maxIndex[1] = j
                    max = action[i][j].item()
                    
                    
        output_dist[maxIndex[0], maxIndex[1]] += 1
        # arr = action.numpy()
        # # print(arr)
        # if not arr.ndim == 1:
        #     arr = arr[0][0]
            
        # action = torch.tensor(arr)
        observation, reward, terminated, truncated, info = env.step(action)
        if(t == 0):
            reward = 0
        if(t == 50):
            terminated = True
            # reward = reward - 1000
        reward = torch.tensor([reward], device=device)
        # print(info)
        # print(reward)
        done = terminated or truncated
        # if(random.randint(1, 100) == 1):
        #     print(state)
        #     print(maxIndex)
            
        #     print(reward)
        # output_dist[action[0]] += 1
        # output_dist[action[1]] += 1   
        # output_dist_2[action[2]] += 1 
        # print(state)
        reward_sum += reward.item()
        if terminated:
            next_state = None
        else:
            next_state = torch.tensor(observation, dtype=torch.float32, device=device).unsqueeze(0)
            # print(next_state)
            # next_state = [[0]]
            # # next_state = next_state.reshape(1, 1)
            # next_state[0][0] = next_state_temp
            # next_state = torch.tensor(next_state)
            
        # Store the transition in memory
        memory.push(state, action, next_state, reward)

        # Move to the next state
        state = next_state

        # Perform one step of the optimization (on the policy network)
        tempVal2 = optimize_model()
        
           
        # Soft update of the target network's weights
        # θ′ ← τ θ + (1 −τ )θ′
        target_net_state_dict = target_net.state_dict()
        policy_net_state_dict = policy_net.state_dict()
        for key in policy_net_state_dict:
            target_net_state_dict[key] = policy_net_state_dict[key]*TAU + target_net_state_dict[key]*(1-TAU)
        target_net.load_state_dict(target_net_state_dict)

        if done:
            episode_durations.append(t + 1)
            total_reward_sum += (reward_sum / (t+1))
            total_reward_sum2 += (reward_sum)
            mine_ratio_sum += (info['mine_ratio'] * 100.0)
            count_len += t
            # plot_durations()
            break
    if(i_episode % 100) == 0:
        print("Episode " + str(i_episode - 100) + " to " + str(i_episode) + " avg reward per step: " + str(total_reward_sum / 100.0))
        print("Episode " + str(i_episode - 100) + " to " + str(i_episode) + " avg reward per game: " + str(total_reward_sum2 / 100.0))
        print("Episode " + str(i_episode - 100) + " to " + str(i_episode) + " avg mine clear per game: " + str(mine_ratio_sum / 100.0))
        print("Episode " + str(i_episode - 100) + " to " + str(i_episode) + " avg length: " + str(count_len / 100.0))
        # print(tempVal2)
        print(output_dist)
        print() 
        total_reward_sum = 0
        total_reward_sum2 = 0
        mine_ratio_sum = 0
        count_len = 0
        if(i_episode == 100):
            torch.save(policy_net.state_dict(), "Models/" + str(i_episode) + ".pt")
            print("Saved 100 Game Model")
        if(i_episode == 5000):
            torch.save(policy_net.state_dict(), "Models/" + str(i_episode) + ".pt")
            print("Saved 5000 Game Model")
        if(i_episode == 10000):
            torch.save(policy_net.state_dict(), "Models/" + str(i_episode) + ".pt")
            print("Saved 10000 Game Model")
        if(i_episode == 15000):
            torch.save(policy_net.state_dict(), "Models/" + str(i_episode) + ".pt")
            print("Saved 15000 Game Model")
        if(i_episode == 20000):
            torch.save(policy_net.state_dict(), "Models/" + str(i_episode) + ".pt")
            print("Saved 20000 Game Model")
    

print('Complete')
print(output_dist)
# torch.save(policy_net.state_dict(), "Models/test1.pt")
# print(output_dist_2)
# plot_durations(show_result=True)
# plt.ioff()
# plt.show()    
    
# print(obs_space_dims)
# print(action_space_dims)


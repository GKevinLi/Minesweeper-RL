from enum import Enum
import gymnasium as gym
from gymnasium import spaces
import pygame
import numpy as np

from minesweeper import clear
from minesweeper import setup
from minesweeper import getObs
from minesweeper import evalAction
from minesweeper import isGameFinished
from minesweeper import render
from minesweeper import getClickedArr
from minesweeper import getArr

# class Actions(Enum):
#     right = 0
#     up = 1
#     left = 2
#     down = 3


class MinesweeperEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, render_mode=None, size=5):
        self.size = size  # The size of the square grid
        self.window_size = 500  # The size of the PyGame window

        # Observations are dictionaries with the agent's and the target's location.
        # Each location is encoded as an element of {0, ..., `size`}^2,
        # i.e. MultiDiscrete([size, size]).
        self.observation_space = spaces.Box(-10, 10, shape=(10, 10), dtype=int)

        # We have 4 actions, corresponding to "right", "up", "left", "down", "right"
        self.action_space = spaces.Box(0, 9, shape=(10, 10), dtype=float)

        """
        The following dictionary maps abstract actions from `self.action_space` to 
        the direction we will walk in if that action is taken.
        i.e. 0 corresponds to "right", 1 to "up" etc.
        """
        # self._action_to_direction = {
        #     Actions.right.value: np.array([1, 0]),
        #     Actions.up.value: np.array([0, 1]),
        #     Actions.left.value: np.array([-1, 0]),
        #     Actions.down.value: np.array([0, -1]),
        # }

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        """
        If human-rendering is used, `self.window` will be a reference
        to the window that we draw to. `self.clock` will be a clock that is used
        to ensure that the environment is rendered at the correct framerate in
        human-mode. They will remain `None` until human-mode is used for the
        first time.
        """
        self.window = None
        self.clock = None

    def _get_obs(self):
        return getObs()

    def _get_info(self):
        cnt = 0
        if(isGameFinished()):
            arr = getArr()
            clickedArr = getClickedArr()
            
            for i in range(10):
                for j in range(10):
                    if(clickedArr[i][j] == 0 and arr[i][j] >= 0):
                        cnt += 1
        # if(cnt >= 0):
        #     print(cnt)
        
        return {
            "mine_ratio": cnt / 90.0  
        }
       

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        # Choose the agent's location uniformly at random
        # self._agent_location = self.np_random.integers(0, self.size, size=2, dtype=int)

        # # We will sample the target's location randomly until it does not
        # # coincide with the agent's location
        # self._target_location = self._agent_location
        # while np.array_equal(self._target_location, self._agent_location):
        #     self._target_location = self.np_random.integers(
        #         0, self.size, size=2, dtype=int
        #     )
        
        setup()

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info

    def step(self, action):
        # Map the action (element of {0,1,2,3}) to the direction we walk in observation = self._get_obs()
        # print(action)
        clickedArr = getClickedArr()
        max = -1000 
        
        maxIndex = [0, 0]
        for i in range(10):
            for j in range(10):
                item = action[i][j].item()
                # if(clickedArr[i][j] == 0):
                #     item = 0
                if item >= max:
                    maxIndex[0] = i
                    maxIndex[1] = j
                    max = action[i][j].item()
                    
                    
        # We use `np.clip` to make sure we don't leave the grid
        # print(action)
        # arr = action.numpy()
        # # print(arr)
        # if not arr.ndim == 1:
        #     arr = arr[0][0]
        reward = evalAction(maxIndex[0], maxIndex[1], 0)
        # An episode is done iff the agent has reached the target
        terminated = isGameFinished()
        
        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, False, info

    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()

    def _render_frame(self):
        # if self.window is None and self.render_mode == "human":
        #     pygame.init()
        #     pygame.display.init()
        #     self.window = pygame.display.set_mode((self.window_size, self.window_size))
        # if self.clock is None and self.render_mode == "human":
        #     self.clock = pygame.time.Clock()

        # canvas = pygame.Surface((self.window_size, self.window_size))
        # canvas.fill((255, 255, 255))
        # pix_square_size = (
        #     self.window_size / self.size
        # )  # The size of a single grid square in pixels

        # # First we draw the target
        

        # if self.render_mode == "human":
        #     # The following line copies our drawings from `canvas` to the visible window
        #     # self.window.blit(canvas, canvas.get_rect())
        #     pygame.event.pump()
        #     pygame.display.update()
        #     pygame.display.flip()

        #     # We need to ensure that human-rendering occurs at the predefined framerate.
        #     # The following line will automatically add a delay to
        #     # keep the framerate stable.
        #     self.clock.tick(self.metadata["render_fps"])
        # else:  # rgb_array
        #     return np.transpose(
        #         np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
        #     )
        render()

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()

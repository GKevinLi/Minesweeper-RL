from gymnasium.envs.registration import register

register(
    id="minesweeper_env/Minesweeper-v0",
    entry_point="minesweeper_env.envs:MinesweeperEnv",
)

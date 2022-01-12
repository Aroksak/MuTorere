import numpy as np
from gym import spaces
from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector, wrappers

from .board import Board


def env(n_kewai=8):
    env = raw_env(n_kewai=n_kewai)
    env = wrappers.CaptureStdoutWrapper(env)
    env = wrappers.TerminateIllegalWrapper(env, illegal_reward=-1)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env


class raw_env(AECEnv):
    metadata = {'render.modes': ['human'], "name": 'mutotere_v0'}

    def __init__(self, n_kewai=8):
        super().__init__()

        self.n_kewai = n_kewai
        self.board = Board(n_kewai=self.n_kewai)

        self.possible_agents = ['player_' + str(r) for r in range(2)]
        self.agents = self.possible_agents[:]

        self.action_spaces = {agent: spaces.Discrete(self.n_kewai + 1) for agent in self.possible_agents}
        self.observation_spaces = {agent: spaces.Dict({
            'observation': spaces.Box(low=0, high=1, shape=(self.n_kewai + 1, 2), dtype=np.int8),
            'action_mask': spaces.Box(low=0, high=1, shape=(self.n_kewai + 1,), dtype=np.int8)
        }) for agent in self.possible_agents}

        self._cumulative_rewards = {agent: 0 for agent in self.possible_agents}
        self.rewards = {agent: 0 for agent in self.possible_agents}
        self.dones = {agent: False for agent in self.possible_agents}
        self.infos = {agent: {} for agent in self.possible_agents}

        self._agent_selector = agent_selector(self.possible_agents)
        self.agent_selection = self._agent_selector.reset()

    def observation_space(self, agent):
        return self.observation_spaces[agent]

    def action_space(self, agent):
        return self.action_spaces[agent]

    def reset(self):
        self.board = Board(n_kewai=self.n_kewai)

        self.agents = self.possible_agents[:]
        self._cumulative_rewards = {agent: 0 for agent in self.agents}
        self.rewards = {agent: 0 for agent in self.agents}
        self.dones = {agent: False for agent in self.agents}
        self.infos = {agent: {} for agent in self.agents}

        self._agent_selector.reinit(self.agents)
        self.agent_selection = self._agent_selector.reset()

    def observe(self, agent):
        flat_board = self.board.kewai + [self.board.putahi]
        cur_player = self.agents.index(agent)
        opp_player = (cur_player + 1) % 2

        cur_p_stones = np.equal(flat_board, self.board.agent_stones[cur_player])
        opp_p_stones = np.equal(flat_board, self.board.agent_stones[opp_player])

        observation = np.stack([cur_p_stones, opp_p_stones], axis=-1).astype(np.int8)
        valid_moves = self.board.get_possible_actions(cur_player) if agent == self.agent_selection else []

        action_mask = np.zeros(self.n_kewai + 1, dtype=np.int8)
        for i in valid_moves:
            action_mask[i] = 1

        return {'observation': observation, 'action_mask': action_mask}

    def step(self, action):
        if self.dones[self.agent_selection]:
            return self._was_done_step(action)

        self.board.play_move(self.agents.index(self.agent_selection), action)

        next_agent = self._agent_selector.next()

        if len(self.board.get_possible_actions(self.agents.index(next_agent))) == 0:
            self.rewards[self.agent_selection] += 1
            self.rewards[next_agent] -= 1
            self.dones = {agent: True for agent in self.agents}

        self._cumulative_rewards[self.agent_selection] = 0
        self.agent_selection = next_agent
        self._accumulate_rewards()

    def render(self, mode='human'):
        self.board.render()

    def close(self):
        self.board.close()

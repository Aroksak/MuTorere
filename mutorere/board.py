import math
from enum import Enum

import pygame

KEWAI_RADIUS = 20
BOARD_RADIUS = KEWAI_RADIUS * 4
SCREEN_SIZE = (BOARD_RADIUS + KEWAI_RADIUS * 2) * 2
BACKGROUND_COLOR = "antiquewhite3"
LINE_COLOR = "black"
BOARD_LINE_WIDTH = 2
SPOT_LINE_WIDTH = 3
WHITE_STONE_COLOR = 'white'
BLACK_STONE_COLOR = 'grey35'


class Stones(Enum):
    EMPTY = 0
    WHITE = 1
    BLACK = 2


class Board:
    def __init__(self, n_kewai=8):
        self.putahi = Stones.EMPTY
        if n_kewai % 2 != 0:
            raise ValueError("n_kewai must be even")
        self.n_kewai = n_kewai
        self.empty_pos = self.n_kewai
        self.kewai = [Stones.WHITE] * (self.n_kewai // 2) + [Stones.BLACK] * (self.n_kewai // 2)
        self.agent_stones = [Stones.WHITE, Stones.BLACK]
        self.render_on = False
        pygame.init()
        self.screen = None
        self.size = SCREEN_SIZE, SCREEN_SIZE

    def get_possible_actions(self, agent):
        possible_actions = []
        if self.putahi == Stones.EMPTY:
            for i in range(self.n_kewai):
                if (self.kewai[i] == self.agent_stones[agent]) and (
                        (self.kewai[(i - 1) % self.n_kewai] != self.agent_stones[agent]) or
                        (self.kewai[(i + 1) % self.n_kewai] != self.agent_stones[agent])):
                    possible_actions.append(i)
        else:
            if self.kewai[(self.empty_pos - 1) % self.n_kewai] == self.agent_stones[agent]:
                possible_actions.append((self.empty_pos - 1) % self.n_kewai)
            if self.kewai[(self.empty_pos + 1) % self.n_kewai] == self.agent_stones[agent]:
                possible_actions.append((self.empty_pos + 1) % self.n_kewai)
            if self.putahi == self.agent_stones[agent]:
                possible_actions.append(self.n_kewai)
        return possible_actions

    def play_move(self, agent, action):
        if action not in self.get_possible_actions(agent):
            raise ValueError("Invalid move")
        if self.putahi == Stones.EMPTY:
            self.putahi = self.agent_stones[agent]
        else:
            self.kewai[self.empty_pos] = self.agent_stones[agent]
        if action < self.n_kewai:
            self.kewai[action] = Stones.EMPTY
        else:
            self.putahi = Stones.EMPTY
        self.empty_pos = action

    def render(self):
        if not self.render_on:
            self.screen = pygame.display.set_mode(self.size)
            self.render_on = True
        width, height = self.size
        center = width // 2, height // 2
        self.screen.fill(BACKGROUND_COLOR)
        pygame.draw.circle(self.screen, LINE_COLOR, center, BOARD_RADIUS, width=BOARD_LINE_WIDTH)
        for i, color in enumerate(self.kewai):
            phi = math.pi / (self.n_kewai // 2) * i
            x = center[0] - int(BOARD_RADIUS * math.sin(phi))
            y = center[1] - int(BOARD_RADIUS * math.cos(phi))
            pygame.draw.line(self.screen, "black", center, (x, y), width=2)
            match color:
                case Stones.WHITE:
                    pygame.draw.circle(self.screen, WHITE_STONE_COLOR, (x, y), KEWAI_RADIUS, width=0)
                case Stones.BLACK:
                    pygame.draw.circle(self.screen, BLACK_STONE_COLOR, (x, y), KEWAI_RADIUS, width=0)
            pygame.draw.circle(self.screen, LINE_COLOR, (x, y), KEWAI_RADIUS, width=SPOT_LINE_WIDTH)
        match self.putahi:
            case Stones.WHITE:
                pygame.draw.circle(self.screen, WHITE_STONE_COLOR, center, KEWAI_RADIUS, width=0)
            case Stones.BLACK:
                pygame.draw.circle(self.screen, BLACK_STONE_COLOR, center, KEWAI_RADIUS, width=0)
        pygame.draw.circle(self.screen, LINE_COLOR, center, KEWAI_RADIUS, width=SPOT_LINE_WIDTH)
        pygame.display.flip()

    def close(self):
        if self.render_on:
            self.render_on = False
            pygame.event.pump()
            pygame.display.quit()

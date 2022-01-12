from time import sleep

from pettingzoo.test import api_test

import mutorere


def mock_game(env, render=False):
    env.reset()
    steps = [0, 7, 8, 4, 3, 8, 2, 3, 8]
    for step in steps:
        if render:
            env.render()
            sleep(1)
        env.step(step)
    if render:
        env.render()
        sleep(1)
        env.close()


def main():
    env = mutorere.env()
    api_test(env)
    mock_game(env, render=True)


if __name__ == '__main__':
    main()

from pettingzoo.test import api_test, render_test

from mutorere import mutorere


def main():
    env = mutorere.env()
    api_test(env)
    render_test(env)


if __name__ == '__main__':
    main()

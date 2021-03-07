import argparse
from life import GameOfLife
import life_console

parser = argparse.ArgumentParser(description='"Game of life" console version with arguments.')
parser.add_argument("--rows", default=30)
parser.add_argument("--cols", default=75)
parser.add_argument("--max-generations", default=20)

args = parser.parse_args()
rows = int(args.rows)
cols = int(args.cols)
max_generations = int(args.max_generations)


if __name__ == '__main__':
    life = GameOfLife((rows, cols), max_generations=max_generations)
    ui = life_console.Console(life)
    ui.run()


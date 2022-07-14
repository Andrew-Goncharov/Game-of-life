import argparse
from life import GameOfLife
import life_gui

parser = argparse.ArgumentParser(description="'Game of life' graphic version with arguments.")

parser.add_argument("--rows", default=30)
parser.add_argument("--cols", default=75)
parser.add_argument("--max-generations", default=20)

args = parser.parse_args()

rows = int(args.rows)
cols = int(args.cols)
max_generations = int(args.max_generations)

if __name__ == "__main__":
    life = GameOfLife((rows, cols), randomize=False, max_generations=max_generations)
    gui = life_gui.GUI(life)
    gui.run()

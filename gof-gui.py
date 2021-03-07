import argparse
from life import GameOfLife
import life_gui

parser = argparse.ArgumentParser(description='"Game of life" graphic version with arguments.')
parser.add_argument("--width", default=200)
parser.add_argument("--height", default=100)
parser.add_argument("--cell-size", default=50)

args = parser.parse_args()

width = int(args.width)
height = int(args.height)
cell_size = int(args.cell_size)

if __name__ == '__main__':
    life = GameOfLife((200, 100), randomize=False, max_generations=50)
    gui = life_gui.GUI(life)
    gui.run()

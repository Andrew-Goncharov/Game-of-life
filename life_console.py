import curses
from life import GameOfLife
from ui import UI
import time

class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)
        self.life = life

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        y = self.life.rows + 1
        x = self.life.cols + 1
        screen.addstr(1, 1, "+")
        screen.addstr(y + 1, 1, "+")
        screen.addstr(1, x + 1, "+")
        screen.addstr(y + 1, x + 1, "+")
        for x in range(2, self.life.cols + 2):
            screen.addstr(1, x, "-")
        for x in range(2, self.life.cols + 2):
            screen.addstr(y + 1, x, "-")
        for y in range(2, self.life.rows + 2):
            screen.addstr(y, 1, "|")
        for y in range(2, self.life.rows + 2):
            screen.addstr(y, x + 1, "|")
        screen.border(0)

    def draw_grid(self, screen, grid) -> None:
        """ Отобразить состояние клеток. """
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if grid[i][j] == 1:
                    screen.addstr(i + 2, j + 2, "*")

    def run(self) -> None:
        screen = curses.initscr()
        screen.nodelay(True)
        curses.noecho()
        curses.cbreak()
        screen.keypad(True)
        win = curses.newwin(self.life.rows + 10, self.life.cols + 10)
        running = True
        while running:
            self.draw_borders(win)
            self.draw_grid(win, self.life.curr_generation)
            win.refresh()
            time.sleep(0.2)
            self.life.step()
            win.clear()
            if self.life.is_max_generations_exceeded:
                running = False
        curses.endwin()


if __name__ == '__main__':
    life = GameOfLife((30, 75), max_generations=20)
    ui = Console(life)
    ui.run()


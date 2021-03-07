import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI
import time


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        self.cell_size = cell_size
        self.speed = speed
        super().__init__(life)
        self.life = life
        self.width = self.life.cols * self.cell_size
        self.height = self.life.rows * self.cell_size
        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 0:
                    pygame.draw.rect(self.screen, pygame.Color("white"),
                                     (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color("green"),
                                     (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))

    def run(self) -> None:
        """
        Игра начинвается в замороженном режиме.
        Чтобы запустить игру нажмите - Space.
        Чтобы приостановить снова игры нажмите - leftCTRL.
        Жизнь в клетках можно создавать и уничтожать.
        """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        run, pause = 0, 1
        status = pause
        running = True
        position = []
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL:
                        status = pause
                    if event.key == pygame.K_SPACE:
                        status = run
                if status == pause:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            position.append(event.pos)
            self.draw_grid()
            self.draw_lines()
            if status == pause:
                if not(position == []):
                    for pos in position:
                        a = pos[0] // self.cell_size
                        b = pos[1] // self.cell_size
                        if self.life.curr_generation[b][a] == 0:
                            self.life.curr_generation[b][a] = 1
                        else:
                            self.life.curr_generation[b][a] = 0
                    self.draw_grid()
                    self.draw_lines()
                    position = []
            else:
                self.life.step()
            if self.life.is_max_generations_exceeded is True:
                running = False
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

if __name__ == '__main__':
    life = GameOfLife((200, 100), randomize=False, max_generations=50)
    gui = GUI(life)
    gui.run()

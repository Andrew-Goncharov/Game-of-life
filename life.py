import pathlib
import random
import typing as tp
from pprint import pprint as pp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize == True:
            grid = [[random.randint(0, 1) for y in range(self.cols)] for x in range(self.rows)]
        else:
            grid = [[0 for y in range(self.cols)] for x in range(self.rows)]
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        Cells = []
        x = cell[1]
        y = cell[0]
        if y + 1 < len(self.curr_generation):
            Cells.append(self.curr_generation[y + 1][x])
            if x + 1 < len(self.curr_generation[0]):
                Cells.append(self.curr_generation[y + 1][x + 1])
            if x - 1 >= 0:
                Cells.append(self.curr_generation[y + 1][x - 1])
        if y - 1 >= 0:
            Cells.append(self.curr_generation[y - 1][x])
            if x + 1 < len(self.curr_generation[0]):
                Cells.append(self.curr_generation[y - 1][x + 1])
            if x - 1 >= 0:
                Cells.append(self.curr_generation[y - 1][x - 1])
        if x + 1 < len(self.curr_generation[0]):
            Cells.append(self.curr_generation[y][x + 1])
        if x - 1 >= 0:
            Cells.append(self.curr_generation[y][x - 1])
        return Cells

    def get_next_generation(self) -> Grid:
        next_generation_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                cell_neighbors = self.get_neighbours((i, j))
                count_life = sum(cell_neighbors)
                if self.curr_generation[i][j] == 1:
                    if count_life == 2 or count_life == 3:
                        next_generation_grid[i][j] = 1
                    else:
                        next_generation_grid[i][j] = 0
                else:
                    if count_life == 3:
                        next_generation_grid[i][j] = 1
        return next_generation_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.generations >= self.max_generations:
            return True
        else:
            return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.curr_generation != self.prev_generation:
            return True
        else:
            return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        count_rows = 0
        count_cols = 0
        file = open(filename, "r")
        for line in file:
            count_rows += 1
            count_cols = len(line)
        file.close()
        grid = []
        line_grid = [0] * count_cols
        file = open(filename, "r")
        for line in file:
            for i in range(len(line)):
                if line[i] != "\n":
                    line_grid[i] = int(line[i])
            grid.append(line_grid.copy())
        file.close()
        game = GameOfLife((count_cols, count_rows))
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        file = open(filename, "w")
        for i in range(self.rows):
            for j in range(self.cols):
                if j == self.cols - 1:
                    file.write(str(self.curr_generation[i][j]) + "\n")
                else:
                    file.write(str(self.curr_generation[i][j]))
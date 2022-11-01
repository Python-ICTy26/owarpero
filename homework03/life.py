import pathlib
import random
import typing as tp

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
        max_generations: float = float("inf"),
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
        grid: Grid = []
        for i in range(self.rows):
            grid.append([])
            for j in range(self.cols):
                grid[i].append(random.randint(0, int(randomize)))

        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        row, col = cell
        answer = []

        positions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for i in positions:
            newrow, newcol = row + i[0], col + i[1]
            if newrow < 0 or newrow >= self.rows or newcol < 0 or newcol >= self.cols:
                continue
            answer.append(self.curr_generation[newrow][newcol])
        return answer

    def get_next_generation(self) -> Grid:
        newgrid: Grid = []

        for i in range(self.rows):
            newgrid.append([])
            for j in range(self.cols):
                neighbours = self.get_neighbours((i, j))
                count = 0
                for n in neighbours:
                    if n:
                        count += 1

                if count == 2 and self.curr_generation[i][j]:
                    newgrid[i].append(1)
                    continue

                if count == 3:
                    newgrid[i].append(1)
                    continue

                newgrid[i].append(0)

        return newgrid

    def step(self) -> None:
        self.prev_generation = [[j for j in i] for i in self.curr_generation]
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        f = open(filename, "r")

        grid: Grid = []
        for i in f.readlines():
            grid.append([])
            for j in i:
                grid[-1].append(int(j))

        rows = len(grid)
        cols = len(grid[0])

        a = GameOfLife(size=(rows, cols), randomize=False)
        a.curr_generation = grid

        f.close()

        return a

    def save(self, filename: pathlib.Path) -> None:
        f = open(filename, "w")

        for i in self.curr_generation:
            for j in i:
                f.write(str(j))
            f.write("\n")

        f.close()

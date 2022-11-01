import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.rows = self.height // self.cell_size
        self.cols = self.width // self.cell_size
        self.grid = self.create_grid(randomize=True)

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

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
            answer.append(self.grid[newrow][newcol])
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

                if count == 2 and self.grid[i][j]:
                    newgrid[i].append(1)
                    continue

                if count == 3:
                    newgrid[i].append(1)
                    continue

                newgrid[i].append(0)

        return newgrid

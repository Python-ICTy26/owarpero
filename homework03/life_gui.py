import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        self.speed = speed
        self.cell_size = cell_size
        self.width = life.cols * cell_size
        self.height = life.rows * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        super().__init__(life)

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j]:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("green"),
                        (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("white"),
                        (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size),
                    )

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        self.draw_grid()
        self.draw_lines()

        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.constants.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    if not pause:
                        continue

                    y, x = pygame.mouse.get_pos()
                    x //= self.cell_size
                    y //= self.cell_size

                    if self.life.curr_generation[x][y]:
                        self.life.curr_generation[x][y] = 0
                    else:
                        self.life.curr_generation[x][y] = 1
                    self.draw_grid()
                    self.draw_lines()

                    pygame.display.flip()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pause = not pause

            if not pause:
                if not self.life.is_max_generations_exceeded and self.life.is_changing:
                    self.life.step()
                    self.draw_grid()
                    self.draw_lines()

                pygame.display.flip()
                clock.tick(self.speed)
        pygame.quit()

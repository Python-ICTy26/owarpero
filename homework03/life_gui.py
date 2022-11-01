import argparse
import sys
import typing

import pygame
from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(
        self,
        screen_size: typing.Tuple[int, int],
        life: GameOfLife,
        cell_size: int = 10,
        speed: int = 10,
    ) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed

        self.pause = True

        self.screen = pygame.display.set_mode(screen_size)
        self.screen_size = self.width, self.height = screen_size

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                pygame.draw.rect(
                    self.screen,
                    pygame.Color("green")
                    if self.life.curr_generation[i][j]
                    else pygame.Color("white"),
                    (
                        j * self.cell_size,
                        i * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                    ),
                )

    def on_click(self, pos: typing.Tuple[int, int]) -> None:
        self.life.invert_value((pos[1] // self.cell_size, pos[0] // self.cell_size))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        self.pause = not self.pause
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        self.on_click(pygame.mouse.get_pos())

            self.screen.fill(pygame.Color("white"))
            self.draw_grid()
            self.draw_lines()

            pygame.display.flip()

            if not self.pause:
                self.life.step()

            if not self.life.is_changing or self.life.is_max_generations_exceeded:
                self.pause = True

            clock.tick(self.speed)
        pygame.quit()


def main():
    parser = argparse.ArgumentParser(prog="GameOfLife with gui")
    parser.add_argument("--width", type=int, default=640, required=False, nargs="?")
    parser.add_argument("--height", type=int, default=480, required=False, nargs="?")
    parser.add_argument("--cell-size", type=int, default=10, required=False, nargs="?")
    parser.add_argument("--speed", type=int, default=10, required=False, nargs="?")
    parser.add_argument("--max-generations", type=int, default=-1, required=False, nargs="?")
    parser.add_argument("--randomize", type=bool, default=False, required=False, nargs="?")

    parser.parse_args(sys.argv[1:])
    args = parser.parse_args()

    game_field_size = (args.height // args.cell_size, args.width // args.cell_size)
    game = GameOfLife(game_field_size, args.randomize, args.max_generations)
    gui = GUI((args.width, args.height), game, args.cell_size, args.speed)
    gui.run()


if __name__ == "__main__":
    main()

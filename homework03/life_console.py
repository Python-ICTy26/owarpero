import argparse
import curses
import sys
import typing

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, size: typing.Tuple[int, int], life: GameOfLife, speed: int = 20) -> None:
        super().__init__(life)
        self.size = self.rows, self.cols = size
        self.delay = 1 / speed

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.addstr(f"+{'-' * self.cols}+\n")
        for _ in range(self.rows):
            screen.addstr(f"|{' ' * self.cols}|\n")
        screen.addstr(f"+{'-' * self.cols}+\n")
        # screen.border()

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.get_cell((i, j)):
                    screen.addch(i + 1, j + 1, "*")

    def run(self) -> None:
        screen = curses.initscr()
        curses.resize_term(self.rows + 3, self.cols + 3)
        running = True
        print("Press 'q' to exit the program")
        while running:
            screen.clear()
            self.draw_borders(screen)
            self.draw_grid(screen)
            self.life.step()
            if screen.getch() == ord("q"):
                break
        curses.endwin()


def main():
    parser = argparse.ArgumentParser(prog="GameOfLife with console ui")
    parser.add_argument("--cols", type=int, default=10, required=False, nargs="?")
    parser.add_argument("--rows", type=int, default=10, required=False, nargs="?")
    parser.add_argument("--speed", type=int, default=10, required=False, nargs="?")
    parser.add_argument("--max-generations", type=int, default=-1, required=False, nargs="?")
    parser.add_argument("--randomize", type=bool, default=True, required=False, nargs="?")

    parser.parse_args(sys.argv[1:])
    args = parser.parse_args()

    game = GameOfLife((args.rows, args.cols), args.randomize, args.max_generations)
    gui = Console((args.rows, args.cols), game, args.speed)
    gui.run()


if __name__ == "__main__":
    main()

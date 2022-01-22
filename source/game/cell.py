import pygame
from .constants import CELL_SIZE


class Cell(pygame.sprite.Sprite):
    def __init__(self, color: str, row_index: int, column_index: int):
        super(Cell, self).__init__()

        # We need row index and column index to identify the position of the cell
        self.row_index = row_index
        self.column_index = column_index

        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image = pygame.transform.scale(
            pygame.image.load(f"./images/{color}.png").convert(), (45, 45)
        )
        self.rect = self.image.get_rect(
            topleft=(self.column_index * CELL_SIZE, self.row_index * CELL_SIZE)
        )

    def move(self, direction: str, times: int = 1):
        """
        Moves the cell in certain direction

        Args:
            direction (str): the direction
        """

        if direction == "down":
            if self.row_index == 14:
                return

            self.row_index += 1 * times
            self.rect.y += 45 * times

        if direction == "right":
            if self.column_index == 9:
                return

            self.column_index += 1
            self.rect.x += 45

        if direction == "left":
            if self.column_index == 0:
                return

            self.column_index -= 1
            self.rect.x -= 45

    def update(self):
        if self.column_index < 0:
            self.column_index = 0
        if self.column_index > 9:
            self.column_index = 9
        self.rect = self.image.get_rect(
            topleft=(self.column_index * CELL_SIZE, self.row_index * CELL_SIZE)
        )

import pygame
from .cell import Cell
from .constants import *


class Block:
    def __init__(self, type: str):
        # The block type
        self.type = type

        # a container of all cells of the block
        self.cell_grp = pygame.sprite.Group()

        # This attribute specifies the block's center cell index
        # this helps us be able to rotate the block
        self.center_cell_index = 0

        self.cell_outside_center_index = None
        self.cell_outside_center_state = ""

        # If the block (one of its cells) touches another cell or reaches
        # the bottom border of the board
        self.touch_bottom = False
        self.touch_sides = False
        self.moveable = True

        # start_ticks sets a time counter when the block touches the ground or another block
        # this allows us to know how many seconds have passed since the start_ticks's been set
        self.start_ticks = 0

        # Forms a brand new block
        self.form_block()

    def form_block(self):
        """
        Adds cells to the foundation of the block depending on 'self.type'
        """

        # self.center_cell_index: the index of the center cell

        # self.cell_outside_center_index: the index of the cell that is outside the center cell

        # self.cell_outside_center_state: this property determines the position of the cell mentioned above

        # first_cell_col_index = randint(3, 5)
        first_cell_col_index = 4
        if self.type == "T":
            self.center_cell_index = 2
            self.cell_grp.add(Cell("purple", 0, first_cell_col_index))
            self.cell_grp.add(Cell("purple", 1, first_cell_col_index - 1))
            self.cell_grp.add(Cell("purple", 1, first_cell_col_index))  # center
            self.cell_grp.add(Cell("purple", 1, first_cell_col_index + 1))

        if self.type == "S":
            self.center_cell_index = 0

            self.cell_outside_center_index = 2

            self.cell_outside_center_state = "down_2"

            self.cell_grp.add(Cell("green", 0, first_cell_col_index))  # center
            self.cell_grp.add(Cell("green", 0, first_cell_col_index + 1))
            self.cell_grp.add(Cell("green", 1, first_cell_col_index - 1))
            self.cell_grp.add(Cell("green", 1, first_cell_col_index))

        if self.type == "Z":
            # the center cell index
            self.center_cell_index = 1

            self.cell_outside_center_index = 3

            self.cell_outside_center_state = "down_1"

            self.cell_grp.add(Cell("red", 0, first_cell_col_index - 1))
            self.cell_grp.add(Cell("red", 0, first_cell_col_index))  # center
            self.cell_grp.add(Cell("red", 1, first_cell_col_index))
            self.cell_grp.add(Cell("red", 1, first_cell_col_index + 1))

        if self.type == "O":
            self.cell_grp.add(Cell("yellow", 0, first_cell_col_index))
            self.cell_grp.add(Cell("yellow", 0, first_cell_col_index + 1))
            self.cell_grp.add(Cell("yellow", 1, first_cell_col_index))
            self.cell_grp.add(Cell("yellow", 1, first_cell_col_index + 1))

        if self.type == "I":
            # first_cell_col_index = randint(3, 4)
            first_cell_col_index = 3

            self.center_cell_index = 1

            self.cell_outside_center_index = 3

            self.cell_outside_center_state = "up_2"

            self.cell_grp.add(Cell("cyan", 0, first_cell_col_index))
            self.cell_grp.add(Cell("cyan", 0, first_cell_col_index + 1))  # center
            self.cell_grp.add(Cell("cyan", 0, first_cell_col_index + 2))
            self.cell_grp.add(Cell("cyan", 0, first_cell_col_index + 3))

        if self.type == "J":
            self.center_cell_index = 2

            self.cell_outside_center_index = 0
            self.cell_outside_center_state = "up_1"

            # first_cell_col_index = randint(5, 5)
            first_cell_col_index = 3
            self.cell_grp.add(Cell("blue", 0, first_cell_col_index))
            self.cell_grp.add(Cell("blue", 1, first_cell_col_index))
            self.cell_grp.add(Cell("blue", 1, first_cell_col_index + 1))  # center
            self.cell_grp.add(Cell("blue", 1, first_cell_col_index + 2))

        if self.type == "L":
            self.center_cell_index = 2

            self.cell_outside_center_index = 0
            self.cell_outside_center_state = "up_2"

            # first_cell_col_index = randint(3, 5)
            first_cell_col_index = 5
            self.cell_grp.add(Cell("orange", 0, first_cell_col_index))
            self.cell_grp.add(Cell("orange", 1, first_cell_col_index))
            self.cell_grp.add(Cell("orange", 1, first_cell_col_index - 1))  # center
            self.cell_grp.add(Cell("orange", 1, first_cell_col_index - 2))

    def block_constraint(self, board: list):
        """
        Checks if one of the cell of the block reaches the bottom of the board
        """

        cell_that_touches = None
        for cell in self.cell_grp.sprites():
            # If one of the cell of the block reaches the last row
            # or reaches other cells

            if cell.row_index == 14:
                self.touch_bottom = True
                cell_that_touches = cell
            elif board[cell.row_index + 1][cell.column_index] == 1:
                self.touch_bottom = True
                cell_that_touches = cell
            else:
                continue

            if cell.row_index == 14 or self.touch_bottom:
                # If the block's row_index is 14, then give user another 1 seconds to move the block
                if self.start_ticks == 0:
                    self.start_ticks = str(pygame.time.get_ticks())[:-3]

                # While self.touch_bottom is True, if the block that touched something before has not touched anything so far
                # then reset the start_ticks, set self.touch_bottom to False
                try:
                    if (
                        not board[cell_that_touches.row_index + 1][
                            cell_that_touches.column_index
                        ]
                        == 1
                        and not int(str(pygame.time.get_ticks())[:-3])
                        - int(self.start_ticks)
                        == 2
                    ):
                        self.start_ticks = 0
                        self.touch_bottom = False
                        cell_that_touches = None
                        continue
                except IndexError:
                    pass

                # Set the self.touched to True if the extra seconds passed
                if int(str(pygame.time.get_ticks())[:-3]) - int(self.start_ticks) == 2:
                    self.moveable = False
                    self.start_ticks = 0

                return

    def rotate(self, board: list):
        # if the block type is "O", which is unnecessary to rotate
        if self.type == "O":
            return

        def next_to_the_center_cell(center_pos: tuple, block_pos: tuple) -> bool:
            """
            This function checks if block_pos is next to the center block or not.

            Args:
                center_pos (tuple): The position of the block block
                block_pos (tuple): The position of the center block

            Returns:
                bool: Result
            """

            # 0: x position, 1: y position
            # [center_x - block_x == 1]

            if any(
                [
                    center_pos[0] - block_pos[0] == 1,
                    block_pos[1] - center_pos[1] == 1,
                    block_pos[0] - center_pos[0] == 1,
                    center_pos[1] - block_pos[1] == 1,
                ]
            ):
                return True

            return False

        def direction_identification(center_pos: tuple, block_pos: tuple) -> str:
            """
            This function returns the direction of the center_pos according to block_pos

            Args:
                center_pos (tuple): Center Cell position
                block_pos (tuple): The block position used to calculate the direction of the block

            Returns:
                str: [description]
            """
            if center_pos[0] - block_pos[0] == 1:
                return "left"
            if block_pos[0] - center_pos[0] == 1:
                return "right"
            if center_pos[1] - block_pos[1] == 1:
                return "up"
            if block_pos[1] - center_pos[1] == 1:
                return "down"

        # Move cells that are next to the center cell around the center cell
        for cell in self.cell_grp.sprites():
            # If the cell is the center cell
            if self.cell_grp.sprites().index(cell) == self.center_cell_index:
                continue

            if self.cell_grp.sprites().index(cell) == self.cell_outside_center_index:
                if self.cell_outside_center_state == "down_1":
                    if self.type == "I":
                        cell.column_index -= 2
                        cell.row_index -= 2
                    else:
                        cell.column_index -= 2

                    self.cell_outside_center_state = "down_2"

                elif self.cell_outside_center_state == "down_2":
                    if self.type == "I":
                        cell.row_index -= 2
                        cell.column_index += 2
                    else:
                        cell.row_index -= 2

                    self.cell_outside_center_state = "up_1"

                elif self.cell_outside_center_state == "up_1":
                    if self.type == "I":
                        cell.column_index += 2
                        cell.row_index += 2
                    else:
                        cell.column_index += 2
                    self.cell_outside_center_state = "up_2"
                elif self.cell_outside_center_state == "up_2":
                    if self.type == "I":
                        cell.row_index += 2
                        cell.column_index -= 2
                    else:
                        cell.row_index += 2
                    self.cell_outside_center_state = "down_1"

                continue

            # Get the position of the center block
            center_cell_pos = (
                self.cell_grp.sprites()[self.center_cell_index].column_index,
                self.cell_grp.sprites()[self.center_cell_index].row_index,
            )

            # Get the position of the current cell
            cell_pos = (cell.column_index, cell.row_index)

            # Check if the current cell is next to the center cell
            if next_to_the_center_cell(center_cell_pos, cell_pos):
                # identify the direction of the current cell
                dir_iden_result = direction_identification(center_cell_pos, cell_pos)

                if dir_iden_result == "right":
                    cell.row_index += 1
                    cell.column_index -= 1

                elif dir_iden_result == "left":
                    cell.row_index -= 1
                    cell.column_index += 1

                elif dir_iden_result == "up":
                    cell.column_index += 1
                    cell.row_index += 1

                elif dir_iden_result == "down":
                    cell.column_index -= 1
                    cell.row_index -= 1

        # If a cell in the block is outside the board
        for cell in self.cell_grp.sprites():
            # After rotation if one of the cells position has been occupied by another cell
            if board[cell.row_index][cell.column_index] == 1:
                for cell in self.cell_grp.sprites():
                    cell.row_index -= 1

            if cell.row_index < 0:
                # Move the block down
                for cell in self.cell_grp.sprites():
                    cell.row_index += 1

            if cell.column_index < 0:
                # Move the block to the right
                for cell in self.cell_grp.sprites():
                    cell.column_index += 1

            if cell.column_index > 9:
                for cell in self.cell_grp.sprites():
                    cell.column_index -= 1

    def show_cells(self):
        """
        Draws / Blits and updates those cells on to the screen
        """

        self.cell_grp.draw(pygame.display.get_surface())
        self.cell_grp.update()

    def show_preview(self, start_x_pos, start_y_pos):
        """Shows a preview of where the block will be placed"""

        pygame.draw.line(
            pygame.display.get_surface(),
            (110, 221, 224),
            (start_x_pos, start_y_pos),
            (start_x_pos + 45, start_y_pos),
        )
        pygame.draw.line(
            pygame.display.get_surface(),
            (110, 221, 224),
            (start_x_pos + 45, start_y_pos),
            (start_x_pos + 45, start_y_pos + 45),
        )
        pygame.draw.line(
            pygame.display.get_surface(),
            (110, 221, 224),
            (start_x_pos + 45, start_y_pos + 45),
            (start_x_pos, start_y_pos + 45),
        )
        pygame.draw.line(
            pygame.display.get_surface(),
            (110, 221, 224),
            (start_x_pos, start_y_pos + 45),
            (start_x_pos, start_y_pos),
        )

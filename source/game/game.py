import pygame
import sys
from .constants import *
from .block import Block
from random import choice


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Tetris")

        # All blocks in the game
        self.all_blocks = []

        self.next_block = []

        # Each time this timer is triggered, the block controlled by user will move down 1 block
        self.block_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.block_event, 1000)

        # This board will have 15 rows and 10 columns
        self.board = [[0 for _ in range(10)] for _ in range(15)]

        self.score = 0

        self.game_over = False

    def fill_screen(self):
        self.screen.fill((51, 51, 51))
        # self.screen.blit(self.background, (0, 0))

    def events(self):
        """Tracks all events in the game"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # If user presses down arrow key
            if event.type == pygame.KEYDOWN:
                # If the game is not over
                if not self.game_over:
                    if (
                        not event.key
                        in [
                            pygame.K_DOWN,
                            pygame.K_UP,
                            pygame.K_RIGHT,
                            pygame.K_LEFT,
                            pygame.K_SPACE,
                        ]
                        or not self.all_blocks
                    ):
                        return

                    if self.all_blocks[0].moveable:
                        if event.key == pygame.K_DOWN:
                            # If the block has touched another block below it
                            # then we do not allow the block to be moved down
                            if self.all_blocks[0].touch_bottom:
                                return

                            # Otherwise moves the block down by moving every cell of the block
                            for cell_sprite in self.all_blocks[0].cell_grp.sprites():
                                cell_sprite.move("down")

                        if event.key == pygame.K_RIGHT:
                            # If there's a cell on the right side of the block, then do not move the block
                            for cell_sprite in self.all_blocks[0].cell_grp.sprites():
                                if (
                                    cell_sprite.column_index == 9
                                    or self.board[cell_sprite.row_index][
                                        cell_sprite.column_index + 1
                                    ]
                                    == 1
                                ):
                                    return

                            # Otherwise moves the block right by moving every cell of the block
                            for cell_sprite in self.all_blocks[0].cell_grp.sprites():
                                if (
                                    self.board[cell_sprite.row_index][
                                        cell_sprite.column_index + 1
                                    ]
                                    == 1
                                ):
                                    return

                                cell_sprite.move("right")

                        if event.key == pygame.K_LEFT:
                            for cell_sprite in self.all_blocks[0].cell_grp.sprites():
                                if (
                                    cell_sprite.column_index == 0
                                    or self.board[cell_sprite.row_index][
                                        cell_sprite.column_index - 1
                                    ]
                                    == 1
                                ):
                                    return

                            # Otherwise moves the block to the left by moving every cell of the block
                            for cell_sprite in self.all_blocks[0].cell_grp.sprites():
                                cell_sprite.move("left")

                        if event.key == pygame.K_UP:
                            # This list contains the distances between each cell and the nearest
                            # position that the cell can reach
                            # (this includes another cell or the bottom of the board)
                            cell_distances = []
                            for cell_sprite in self.all_blocks[0].cell_grp.sprites():
                                for row_index in range(cell_sprite.row_index, 15):
                                    if self.board[row_index][cell_sprite.column_index] == 1:
                                        cell_distances.append(
                                            row_index - cell_sprite.row_index - 1
                                        )
                                        break
                                else:
                                    cell_distances.append(
                                        14 - cell_sprite.row_index)
                                    continue

                            for cell_sprite in self.all_blocks[0].cell_grp.sprites():
                                cell_sprite.move("down", min(cell_distances))

                            self.all_blocks[0].moveable = False

                        if event.key == pygame.K_SPACE:
                            if self.all_blocks[0].moveable:
                                self.all_blocks[0].rotate()

                 # Otherwise
                else:
                    # If the space key is pressed
                    if event.key == pygame.K_SPACE:
                        # Create a brand new board
                        self.board = [
                            [0 for _ in range(10)] for _ in range(15)]

                        self.game_over = False

                        # Clear all blocks lists
                        self.next_block, self.all_blocks = [], []

                        # Clear all blocks on the screen
                        for block in self.all_blocks:
                            block.cell_grp.empty()
            # block event
            if event.type == self.block_event:
                for cell in self.all_blocks[0].cell_grp.sprites():
                    if cell.row_index == 14:
                        self.all_blocks[0].moveable = False
                        return
                    if (
                        cell.row_index == 14
                        or self.board[cell.row_index + 1][cell.column_index] == 1
                    ):
                        self.all_blocks[0].touch_bottom = True
                        return

                for cell in self.all_blocks[0].cell_grp.sprites():
                    cell.row_index += 1

    def draw_board(self):
        """Creates a board by using lines"""

        # Draw columns
        for i in range(int(BOARD_SIZE_WIDTH / CELL_SIZE) + 1):
            pygame.draw.line(self.screen, (74, 74, 74),
                             (45 * i, 0), (45 * i, HEIGHT), 1)

        # Draw rows
        for i in range(int(BOARD_SIZE_HEIGHT / CELL_SIZE) + 1):
            pygame.draw.line(
                self.screen, (74, 74, 74), (0, 45 *
                                            i), (BOARD_SIZE_WIDTH, 45 * i), 1
            )

        # Draw borders of the main game board
        pygame.draw.line(self.screen, (255, 84, 158), (0, 0), (450, 0), 15)
        pygame.draw.line(self.screen, (255, 84, 158), (450, 0), (450, 675), 8)

    def create_block(self):
        """Creates a new block if there's not any block that is moveable"""

        # If there's no next block, then add one
        if not self.next_block:
            new_block = Block(type=choice(
                ['S', 'Z', 'S', 'Z', 'L', 'J', 'L', 'J', 'T', 'O', 'I']))

            # We add new_block 2 times
            # the first block is used for moveable block
            # the second one is used for showing the next block
            self.next_block.append(new_block)
            self.next_block.append(new_block)

        # If there's no block in the list or no block is moveable
        if not self.all_blocks or not self.all_blocks[0].moveable:
            # Add the first item of self.next_block to the block list
            self.all_blocks.insert(0, self.next_block[0])

            # Empty the next_block list
            self.next_block.pop(0)
            self.next_block.pop(0)

    def update_and_show_blocks(self):
        """Shows all cells in all blocks"""

        self.all_blocks[0].block_constraint(self.board)
        self.all_blocks[0].cell_grp.update()
        for block in self.all_blocks:
            block.show_cells()

    def track_cells(self):
        """
        Checks if a square in the board is placed by a block cell
        then replace it with 1 in the board
        """

        for block in self.all_blocks:
            if not block.moveable:
                for cell in block.cell_grp.sprites():
                    self.board[cell.row_index][cell.column_index] = 1

    def get_points(self):
        """
        User will get a certain amount of points if one or more rows 
        is completely full
        """

        for board_row_index, row in enumerate(self.board):
            if sum(row) == 10:
                break
        else:
            return

        # This list contains all row indexes which indicate full rows
        rows_to_remove = []

        # If a row is full then add its index to rows_to_remove
        for board_row_index, row in enumerate(self.board):
            if sum(row) == 10:
                rows_to_remove.append(board_row_index)

        # We need to reverse the list to avoid logical index error
        rows_to_remove.reverse()

        # Each full row is equivalent to 10 points
        self.score += 10 * len(rows_to_remove)

        for removing_row_index in rows_to_remove:
            self.board.pop(removing_row_index)

        # Kill all cells that lie on all full rows in rows_to_remove
        for board_row_index in rows_to_remove:
            for block in self.all_blocks:
                if not block.moveable:
                    for cell in block.cell_grp.sprites():
                        if cell.row_index == board_row_index:
                            cell.kill()

            self.board.insert(0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        # Move all the cells that are above removed rows down
        for block in self.all_blocks:
            if not block.moveable:
                for cell in block.cell_grp.sprites():
                    if cell.row_index <= rows_to_remove[-1]:
                        cell.move('down', len(rows_to_remove))

    def show_next_block(self):
        """Shows what the next block is"""

        next_block_text_font = pygame.font.Font(None, 50)
        next_block_text_font.bold = True
        next_block_text_surf = next_block_text_font.render(
            'Next Block:', True, (255, 255, 255))
        self.screen.blit(next_block_text_surf, (510, 50))

        try:
            if not hasattr(self.next_block[1], 'show_only'):
                self.next_block[1].show_only = True

                for cell in self.next_block[1].cell_grp.sprites():
                    cell.rect.x += 45 * 9
                    cell.rect.y += 45 * 3
        except IndexError:
            return

        self.next_block[1].cell_grp.draw(self.screen)

    def show_score(self):
        """Shows the current score"""

        score_text_font = pygame.font.Font(None, 55)
        score_text_font.bold = True
        score_text_surf = score_text_font.render(
            'Score:', True, (255, 255, 255))
        score_text_rect = score_text_surf.get_rect(center=(615, 400))

        score_number_font = pygame.font.Font(None, 50)
        score_number_font.bold = True
        scrore_number_text_surf = score_number_font.render(
            str(self.score), True, (255, 255, 255))
        scrore_number_text_rect = scrore_number_text_surf.get_rect(
            center=(615, 470))

        self.screen.blit(score_text_surf, score_text_rect)
        self.screen.blit(scrore_number_text_surf, scrore_number_text_rect)

    def if_user_loses(self):
        if self.game_over:
            return

        for block in self.all_blocks:
            if not block.moveable:
                for cell in block.cell_grp.sprites():
                    if cell.row_index <= 0:
                        self.game_over = True

    def show_game_over(self):
        game_over_text_font = pygame.font.Font(None, 100)
        game_over_text_surf = game_over_text_font.render(
            'YOU LOST!', True, (255, 255, 255))
        game_over_text_rect = game_over_text_surf.get_rect(
            center=(int(WIDTH / 2), int(HEIGHT / 2)))
        self.screen.blit(game_over_text_surf, game_over_text_rect)

    def update_frame(self):
        self.clock.tick(FPS)
        pygame.display.update()

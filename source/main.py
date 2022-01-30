from game import *
import pygame

pygame.init()

bg_music = pygame.mixer.Sound("./sound/music.mp3")
bg_music.play(loops=-1)

if __name__ == "__main__":
    main_game = Game()

    while True:
        main_game.if_user_loses()

        main_game.events()
        if not main_game.game_over:
            main_game.fill_screen()

            main_game.create_block()
            main_game.update_and_show_blocks()
            main_game.track_cells()

            main_game.draw_board()

            main_game.get_points()

            main_game.show_blocks_preview()

            main_game.show_next_block()
            main_game.show_score()

        else:
            main_game.show_game_over()

        main_game.update_frame()

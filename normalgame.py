"""This is the normal game for a player. Controlled by the 1,2,3,4 and t,m keys"""
from time import sleep
import pygame
from funcs import render_multiline
import cardclass

def normal_game():
    """Just the main function of this game"""
    width = 500
    height = 400

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    comic_sans_font = pygame.font.SysFont('Comic Sans MS', 20)

    game = cardclass.GameWithRender(6, height, width)
    game.init_hand()

    done = False
    while not done:
        game_over = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                # Key 0 is 49 key 4 is 53
                if 49 <= event.key < 53:
                    current_key = event.key - 49
                    game.place_card(current_key)

                    if game.check_game_over():
                        screen.fill((0, 0, 0))
                        render_multiline("GAME OVER!\nYour score: {}".format(
                            game.score), width / 2, height / 2, screen,
                                         comic_sans_font, (255, 255, 255))
                        done = True
                        game_over = True
                        break

                if game.trashes > 0 and event.key == pygame.K_t:
                    # Throw away a card. Press the key K to activate
                    game.trash()

                if game.mix and event.key == pygame.K_m:
                    # Mixes the cards in the hand. Press the key U to activate
                    game.mix_hand()

        pygame.display.flip()
        screen.fill((50, 50, 50))  # Draw the background

        # Render the game
        game.render(comic_sans_font, screen, pygame)

        # Render the text.
        render_multiline('Score: {}\nMultiplier: x{}\nTrashes: {}'.format(
            game.score, game.multiplier, game.trashes) + '\nMix: ' + str(game.mix),
                         width - 200, height - 100, screen, comic_sans_font, (255, 255, 255))

        clock.tick(60)
        if done and game_over:
            sleep(2)

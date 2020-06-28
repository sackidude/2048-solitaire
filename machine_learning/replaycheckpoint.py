"""
This is a module that has a function that can replay a checkpoint file.
"""

import neat
import pygame

from cardclass import GameWithRender, INVALID_INPUT
from funcs import render_multiline


def replay_checkpoint(cp_str, eval_function, config, max_cards, width, height, runs_checks=5):
    """
    This function will find the best genome from a checkpoint file and then let it play a game.
    """
    # Get the population at the checkpoint.
    population = neat.Checkpointer.restore_checkpoint(cp_str)

    # Get the winner
    winner = population.run(eval_function, runs_checks)

    # We will show the ai playing a game here.
    game = GameWithRender(max_cards, width, height)
    game.init_hand()
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    comic_sans_font = pygame.font.SysFont('Comic Sans MS', 20)

    net = neat.nn.FeedForwardNetwork.create(winner, config)

    done = False
    i = 0
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pygame.display.flip()
        screen.fill((50, 50, 50))  # Draw the background

        # Render the game
        game.render(comic_sans_font, screen, pygame)

        # Render the text.
        string_to_show = 'Score: {}\nMultiplier: x{}\nTrashes: {}'.format(
            game.score, game.multiplier, game.trashes) + '\nMix: ' + str(game.mix)
        render_multiline(
            string_to_show,
            width - 200, height - 100,
            screen, comic_sans_font,
            (255, 255, 255)
        )

        clock.tick(60)

        if i % 60 == 0:
            i = 0

            # Get the networks choice
            result = net.activate(game.get_network_inputs())

            has_placed = False
            while not has_placed:
                highest_place = result.index(max(result))

                # Preform the result
                if highest_place < 4:
                    # This does not a count for if it want's to place in a full pile.
                    game.place_card(highest_place)

                elif highest_place == 4:
                    response = game.trash()

                    if response == INVALID_INPUT:
                        result[highest_place] = 0
                    else:
                        has_placed = True

                else:
                    game.mix_hand()
        i += 1

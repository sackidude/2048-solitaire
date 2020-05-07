"""
This is the document for machine learning part of this program.
It trains the AI using the neat python library.
"""

import neat
import numpy as np
import pygame
from matplotlib import pyplot as plt

from cardclass import GameWithRender  # , GameWithRender # Will add the game
from cardclass import NonRenderGame
from funcs import render_multiline

# with render when i get to making some visulizestion of the winning neural network

MAX_CARDS = 6
WIDTH = 500
HEIGHT = 400

highest_values = []

def eval_genomes(genomes, config):
    """
    This is the function for testing the model and seeing it's results.
    The fitness of each genome will be calculated by taking the score that they can acheive.
    It gets exponentially large the better the genome preforms,
    just because of how the game is built.
    Not doing this with all of them at the same time because they don't share anything.
    """

    # Go through all of the all the genomes and see how they do.
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        game = NonRenderGame(MAX_CARDS)
        game.init_hand()

        temp_highest = -1
        done = False
        while not done:
            # Evaluate the current game situation
            result = net.activate(game.get_network_inputs())

            # Execute the results from the neural network.
            # The first four numbers in the list are for where to place the card.
            highest_place = result.index(max(result)) # Get the highest num
            if highest_place < 4:
                 # Comparison to false because it's normally None
                if game.place_card(highest_place) == False:
                    genome.fitness = game.score
                    done = True
                    if game.score > temp_highest:
                        temp_highest = game.score
                    break
            elif highest_place < 6:
                if highest_place == 4:
                    if game.trashes == 0:
                        genome.fitness = game.score
                        done = True
                        if game.score > temp_highest:
                            temp_highest = game.score
                        break
                    else:
                        game.trash()

                else:
                    if game.mix:
                        game.mix_hand()
                    else:
                        genome.fitness = game.score
                        done = True
                        if game.score > temp_highest:
                            temp_highest = game.score
                        break

            # Check if it's game over
            if game.check_game_over():
                print("I lost with a score of: " + str(game.score))
                genome.fitness = game.score
                if game.score > temp_highest:
                    temp_highest = game.score
                done = True

    highest_values.append(temp_highest)

    plt.clf()
    plt.plot(np.arange(len(highest_values)), highest_values)
    plt.pause(0.01)


def machine_learning(config_file):
    """
    Machine learning part of this program.
    This will train an ai to be (hopefully) be really good at this game.
    Then show the results with a game with rendering capabilities from pygame.
    """

    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, by using the config just loaded.
    population = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    population.add_reporter(neat.StdOutReporter(True))  # What does this do?
    stats = neat.StatisticsReporter()  # Show the statistics
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = population.run(eval_genomes, 300)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    population = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    population.run(eval_genomes, 10)

    # We will show the ai playing a match here later when i add that feature.
    if input("Do you want to look a game of the best genome?[Y/n]: ") != "n":
        game = GameWithRender(MAX_CARDS, 500, 400)
        game.init_hand()
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        comic_sans_font = pygame.font.SysFont('Comic Sans MS', 20)

        net = neat.nn.FeedForwardNetwork.create(winner, config)

        done = False
        while not done:
            pygame.display.flip()
            screen.fill((50, 50, 50))  # Draw the background

            # Render the game
            game.render(comic_sans_font, screen, pygame)

            # Render the text.
            render_multiline('Score: {}\nMultiplier: x{}\nTrashes: {}'.format(
                game.score, game.multiplier, game.trashes) + '\nMix: ' + str(game.mix),
                             WIDTH - 200, HEIGHT - 100, screen, comic_sans_font, (255, 255, 255))

            clock.tick(60)

            # Get the networks choice
            result = net.activate(game.get_network_inputs())
            highest_place = result.index(max(result))
            # Preform the result
            if highest_place < 4:
                game.place_card(highest_place)
            elif highest_place == 4:
                game.trash()
            else:
                game.mix_hand()

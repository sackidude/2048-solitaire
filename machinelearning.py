"""
This is the document for machine learning part of this program.
It trains the AI using the neat python library.
"""

import neat
import numpy as np
from matplotlib import pyplot as plt
from operator import attrgetter

from cardclass import NonRenderGame  # , GameWithRender # Will add the game

# with render when i get to making some visulizestion of the winning neural network

MAX_CARDS = 6


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
    
    global highest_values
    highest_values.append(temp_highest)
    
    plt.clf()
    plt.plot(np.arange(len(highest_values)), highest_values)
    plt.pause(0.01)

    
highest_values = []

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

    # We will show the ai playing a match here later when i add that feature.
    population = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    population.run(eval_genomes, 10)

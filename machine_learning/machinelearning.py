"""
This is the document for machine learning part of this program.
It trains the AI using the neat python library.
This is a neuroevolution not deep learning.
"""

from math import floor

import neat

from cardclass import NonRenderGame
from machine_learning.replaycheckpoint import replay_checkpoint
from machine_learning.visualize import Visualizer

# with render when i get to making some visulizestion of the winning neural network

MAX_CARDS = 8
WIDTH = 500
HEIGHT = 400
CHECKPOINT_GAP = 10


def give_fitness(genome, score, _done):
    """
    This is to not repeat myself that much.
    It sets the genome fitness to a score and sets done to true
    """
    genome.fitness = score
    _done = True


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

        done = False
        while not done:
            # Evaluate the current game situation
            result = net.activate(game.get_network_inputs())

            # Execute the results from the neural network.
            # The first four numbers in the list are for where to place the card.
            highest_place = result.index(max(result))  # Get the highest num
            if highest_place < 4:
                 # Comparison to false because it's normally None
                if not game.place_card(highest_place):
                    give_fitness(genome, game.score, done)
                    break
            elif highest_place < 6:
                if highest_place == 4:
                    if game.trashes == 0:
                        give_fitness(genome, game.score, done)
                        break
                    else:
                        game.trash()

                else:
                    if game.mix:
                        game.mix_hand()
                    else:
                        give_fitness(genome, game.score, done)
                        break

            # Check if it's game over.
            if game.check_game_over():
                give_fitness(genome, game.score, done)


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
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(CHECKPOINT_GAP))
    plotter = Visualizer()
    population.add_reporter(plotter)
    how_many = int(
        input("How many iterations do you want to train the genomes? "))
    # Run for up to 300 generations.
    winner = population.run(eval_genomes, how_many)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Calculate what the last checkpoint will be.
    last_checkpoint = CHECKPOINT_GAP * floor(how_many / CHECKPOINT_GAP) - 1
    population = neat.Checkpointer.restore_checkpoint(
        'neat-checkpoint-' + str(last_checkpoint))
    population.run(eval_genomes, 10)

    # We will show the ai playing a game here.
    if input("Do you want to look a game of the best genome?[Y/n]: ") != "n":
        replay_checkpoint(
            'neat-checkpoint-' + str(last_checkpoint),
            eval_genomes, config,
            MAX_CARDS,
            WIDTH,
            HEIGHT
        )

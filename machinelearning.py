"""This is the document for machine learning part of this program."""

import neat

def eval_genomes():
    """This is the function for testing the model and seeing it's results"""

def machine_learning(config_file):
    """Machine learning part of this program. Will train an ai to be really good at this game."""
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    population = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = population.run(eval_genomes, 300)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # We will show the ai playing a match here later when i add that feature.

    population = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    population.run(eval_genomes, 10)

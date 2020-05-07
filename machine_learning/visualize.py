"""
This is the document for my own visualization module for visulizing the genomes progress.
"""

import matplotlib.pyplot as plt
from neat.math_util import mean
from neat.reporting import BaseReporter
from neat.six_util import itervalues
from numpy import arange


class Visualizer(BaseReporter):
    """
    This is a class based on the base reporter class.
    It can be used to visualize some information using matplotlib.
    """
    def __init__(self):
        self.fig = plt.figure()
        self.mean_arr = []
        self.best_arr = []

    def post_evaluate(self, config, population, species, best_genome):
        print("Here")
        fitnesses = [c.fitness for c in itervalues(population)]
        self.mean_arr.append(mean(fitnesses))
        self.best_arr.append(best_genome.fitness)

        # Show the thing
        length_range = arange(len(self.mean_arr))
        plt.plot(length_range, self.mean_arr, 'r--', length_range, self.best_arr, 'b')

        plt.pause(0.000001)

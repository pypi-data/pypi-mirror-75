import os
import glob
from pathlib import Path

import imageio
import numpy as np
import matplotlib.pyplot as plt
from joblib import Parallel, delayed


class DemoVisualizer:

    def __init__(self, cost_func: object, particle_positions_hist: list, global_best_position_hist: list,
                 low: float, high: float, n_jobs: int, last_only: bool, benchmark_name: str):
        """
        implements the demo visualizer class
        :param cost_func: the cost function to minimize
        :param particle_positions_hist: the history of particles' positions
        :param global_best_position_hist: the history of best global positions
        :param low: the lower bound of variables in the optimization problem
        :param high: the higher  bound of variables in the optimization problem
        :param n_jobs: the number of jobs
        :param last_only: only stores the last iteration
        :param benchmark_name: the benchmark name
        """

        # vars
        self.particle_positions_hist = particle_positions_hist
        self.global_best_position_hist = global_best_position_hist
        self.low = low
        self.high = high
        self.n_jobs = n_jobs
        self.last_only = last_only
        self.benchmark_name = benchmark_name
        self.plot_size = (12, 8)
        delta = 0.05
        x = np.arange(low, high, delta)
        y = np.arange(low, high, delta)
        self.X, self.Y = np.meshgrid(x, y)
        self.Z = cost_func([self.X, self.Y])
        Path(self.benchmark_name).mkdir(parents=True, exist_ok=True)

    def store_statistics(self, fitness_min_hist: list, fitness_mean_hist: list, fitness_max_hist: list):
        """
        plots the history of changes in the cost function over time
        :param fitness_min_hist: the history of the min values of cost function
        :param fitness_mean_hist: the history of the mean values of cost function
        :param fitness_max_hist: the history of the max values of cost function
        """

        plt.plot(fitness_min_hist)
        plt.plot(fitness_mean_hist)
        plt.plot(fitness_max_hist)
        plt.title('The changes of Fitness Function Over Time')
        plt.xlabel('# Iteration')
        plt.ylabel('Cost Function')
        plt.legend(['Min', 'Mean', 'Max'])
        plt.savefig(Path(self.benchmark_name) / Path('history'), bbox_inches='tight')
        plt.clf()

    def store_figs(self):
        """
        plots the positions over the time
        """

        if self.last_only:
            self.store_figs_iter(len(self.particle_positions_hist) - 1)
        else:
            Parallel(n_jobs=self.n_jobs) \
                (delayed(self.store_figs_iter)(counter) for counter in range(len(self.particle_positions_hist)))

    def store_figs_iter(self, counter: int):
        """
        plots the positions in each iteration
        :param counter: the iteration number
        """

        plt.rcParams['figure.figsize'] = self.plot_size
        plt.rcParams["lines.linewidth"] = 0.5

        # contour
        contours = plt.contour(self.X, self.Y, self.Z, colors='black')
        plt.clabel(contours, inline=True, fontsize=8)

        # history
        plt.scatter(self.particle_positions_hist[counter][:, 0], self.particle_positions_hist[counter][:, 1])
        plt.scatter(self.global_best_position_hist[counter][0], self.global_best_position_hist[counter][1])

        plt.title(f'Particle Positions over Time (Iteration {str(counter):>3s})')
        plt.tight_layout()
        plt.xlim([self.low, self.high])
        plt.ylim([self.low, self.high])
        plt.xlabel('X1')
        plt.ylabel('X2')
        file_name = Path(self.benchmark_name) / Path(f'{str(counter):>3s}.png')
        plt.savefig(file_name, bbox_inches='tight')
        plt.clf()

    def generate_gif(self):
        """
        generate a gif file by combining the positions over the time
        """
        images = []
        file_names = glob.glob(f'{self.benchmark_name}/*')

        for ind, filename in enumerate(file_names):
            images.append(imageio.imread(filename))
            if ind != len(file_names) - 1:
                os.remove(filename)
        imageio.mimsave(self.benchmark_name / Path('particles.gif'), images, duration=0.1)

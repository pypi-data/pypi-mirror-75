import numpy as np

from pyticle.particle import Particle


class SwarmOptimization:

    def __init__(self, cost_func: object, particle_num: int, omega_start: float, omega_end: float, coef: list,
                 low_bound: float, high_bound: float, boundary_strategy: str, var_size: int, max_iter_num: int,
                 elite_rate: float):
        """
        implements the Particle Swarm Intelligence class
        :param cost_func: the cost function to minimize
        :param particle_num: the number of particles
        :param omega_start: the starting value of Omega (linear schedule)
        :param omega_end: the ending value of Omega (linear schedule)
        :param coef: PSO coefficients (C1 and C2) as a list
        :param low_bound: the lower bound of variables in the optimization problem
        :param high_bound: the higher bound of variables in the optimization problem
        :param boundary_strategy: The strategy of handling particles outside of the boundary ("random", "clipping")
        :param var_size: the problem's dimension
        :param max_iter_num: the maximum number of iterations
        :param elite_rate: The elite rate in PSO
        """

        # vars
        self.cost_func = cost_func
        self.particle_num = particle_num
        self.omega_schedule = np.linspace(omega_start, omega_end, max_iter_num, endpoint=True)
        self.coef = coef
        self.low_bound = low_bound
        self.high_bound = high_bound
        self.boundary_strategy = boundary_strategy
        self.var_size = var_size
        self.max_inter_num = max_iter_num
        self.elite_rate = elite_rate
        self.elimination_rate = 1 - elite_rate
        self.global_best_position = None
        self.global_best_fitness = np.inf
        self.particles = [Particle(self.low_bound, self.high_bound, self.var_size) for i in range(self.particle_num)]

        # fitness and global best
        for i in range(self.particle_num):
            self.particles[i].fitness = self.cost_func(self.particles[i].position)
            if self.particles[i].fitness < self.global_best_fitness:
                self.global_best_position = self.particles[i].position
                self.global_best_fitness = self.particles[i].fitness

    def get_particle_positions(self):
        """
        returns the position of all particles as a numpy array
        """
        pos_list = [[i.position] for i in self.particles]
        return np.concatenate(pos_list, axis=0)

    def optimize(self):
        """
        Executes the cost function
        """

        # vars
        iter_num = 0
        self.fitness_max_hist = []
        self.fitness_mean_hist = []
        self.fitness_min_hist = []
        self.particle_positions_hist = []
        self.global_best_position_hist = []

        # the main loop
        while iter_num < self.max_inter_num:
            for particle_index in range(self.particle_num):
                self.update_particle(particle_index, iter_num)

            # store the history of optimization
            self.fitness_mean_hist.append(self.get_mean_fitness())
            self.fitness_min_hist.append(self.get_min_fitness())
            self.fitness_max_hist.append(self.get_max_fitness())
            self.particle_positions_hist.append(self.get_particle_positions())
            self.global_best_position_hist.append(self.global_best_position)

            iter_num = iter_num + 1

        return self.global_best_fitness, self.global_best_position

    def update_particle(self, particle_index: int, iter_num: int):
        """
        updates the velocity and position of a single particle
        :param particle_index: the index of the particle to update
        :param iter_num: the iteration number (for scheduling)
        """

        # no update for the global best
        elite_limit = np.quantile(self.get_particles_fitness(), self.elite_rate)
        distance_to_global_best = np.abs(self.particles[particle_index].fitness - self.global_best_fitness)
        if distance_to_global_best > elite_limit:
            self.update_particle_vel(particle_index, iter_num)
            self.update_particle_position(particle_index)



    def update_particle_vel(self, particle_index: int, iter_num: int):
        """
        updates the velocity of one particle
        :param particle_index: the index of the particle to update
        :param iter_num: the iteration number (for scheduling)
        """

        r = np.random.uniform(low=0.0, high=1.0, size=2)
        omega = self.omega_schedule[iter_num]
        vel = omega * self.particles[particle_index].velocity \
              + self.coef[0] * r[0] * self.particles[particle_index].particle_best_position \
              + self.coef[1] * r[1] * self.global_best_position

        self.particles[particle_index].velocity = vel


    def update_particle_position(self, particle_index: int):
        """
        updates the position of one particle
        :param particle_index: the index of the particle to update
        """

        # choose the best direction to move
        p1 = self.particles[particle_index].position + self.particles[particle_index].velocity
        p2 = self.particles[particle_index].position - self.particles[particle_index].velocity

        if self.get_out_range_dim_num(p1) < self.get_out_range_dim_num(p2):
            self.particles[particle_index].position = p1
        else:
            self.particles[particle_index].position = p2

        # check for out of range positions
        for dim in range(self.var_size):

            dim_value = self.particles[particle_index].position[dim]

            # pass the dimension if it's in the right range
            if self.low_bound <= dim_value <= self.high_bound:
                continue

            if self.boundary_strategy == 'random':
                    dim_new_value = np.random.uniform(low=self.low_bound, high=self.high_bound, size=1)
            elif self.boundary_strategy == 'clipping':
                if dim_value < self.low_bound:
                    dim_new_value = self.low_bound
                if dim_value > self.high_bound:
                    dim_new_value = self.high_bound
            else:
                raise Exception(f'{self.boundary_strategy} is a unknown boundary strategy')

            self.particles[particle_index].position[dim] = dim_new_value

        # reset weak particles
        if self.particles[particle_index].fitness > np.quantile(self.get_particles_fitness(), self.elimination_rate):
            mean_point = (self.high_bound - self.low_bound) / 2
            self.particles[particle_index].position = 0.5 * (self.particles[particle_index].particle_best_position
                                                             + self.global_best_position
                                                             + np.random.normal(0.0, np.sqrt(mean_point),
                                                                                size=self.var_size))
        self.particles[particle_index].fitness = self.cost_func(self.particles[particle_index].position)

        # update particle best
        if self.particles[particle_index].fitness < self.particles[particle_index].particle_best_fitness:
            self.particles[particle_index].particle_best_position = self.particles[particle_index].position
            self.particles[particle_index].particle_best_fitness = self.particles[particle_index].fitness

        # update global best
        if self.particles[particle_index].fitness < self.global_best_fitness:
            self.global_best_position = self.particles[particle_index].position
            self.global_best_fitness = self.particles[particle_index].fitness

    def get_particles_fitness(self):
        """
        returns the fitness of all particles as a list
        """
        return [i.fitness for i in self.particles]

    def get_mean_fitness(self):
        """
        returns the mean of fitness of all particles
        """
        return np.mean(self.get_particles_fitness())

    def get_median_fitness(self):
        """
        returns the median of fitness of all particles
        """
        return np.median(self.get_particles_fitness())

    def get_max_fitness(self):
        """
        returns the max of fitness of all particles
        """
        return np.max(self.get_particles_fitness())

    def get_min_fitness(self):
        """
        returns the min of fitness of all particles
        """
        return np.min(self.get_particles_fitness())

    def get_out_range_dim_num(self, position):
        """
        counts the number of dimensions of a position that are out of range
        :param position: the particle's position
        """
        return np.sum([0 if self.low_bound <= position[dim] <= self.high_bound else 1 for dim in range(self.var_size)])

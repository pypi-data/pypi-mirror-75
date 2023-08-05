from pyticle.swarm_optimization import SwarmOptimization
from pyticle.benchmark import Benchmark
from pyticle.data_visualizer import DemoVisualizer


def demo_run():

    # benchmarks
    cost_functions = [Benchmark.x2, Benchmark.salustowicz, Benchmark.ackley]
    low_high_ranges = [[-10, 10], [0, 10], [-15, 30]]

    for i in range(len(cost_functions)):

        # range
        low_bound = low_high_ranges[i][0]
        high_bound = low_high_ranges[i][1]

        # optimization
        optimizer = SwarmOptimization(cost_func=cost_functions[i], particle_num=100, omega_start=1, omega_end=0.0,
                                      coef=[2.0, 2.0], low_bound=low_bound, high_bound=high_bound,
                                      boundary_strategy='random', var_size=2, max_iter_num=100, elite_rate=0.1)
        optimizer.optimize()

        # history of optimization
        global_best_position_hist = optimizer.global_best_position_hist
        particle_positions_hist = optimizer.particle_positions_hist

        # visualization
        demo_visualizer = DemoVisualizer(cost_functions[i], particle_positions_hist, global_best_position_hist, low_bound,
                                         high_bound, n_jobs=7, last_only=False, benchmark_name=cost_functions[i].__name__)
        demo_visualizer.store_statistics(optimizer.fitness_min_hist, optimizer.fitness_mean_hist, optimizer.fitness_max_hist)
        demo_visualizer.store_figs()
        demo_visualizer.generate_gif()

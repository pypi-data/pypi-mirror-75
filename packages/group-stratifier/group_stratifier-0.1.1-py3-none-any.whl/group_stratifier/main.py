import numbers
import warnings

import numpy as np
from pyeasyga import pyeasyga

from group_stratifier.util import check_random_state


class GroupStratifiedKFold:
    def __init__(self, n_splits=5, *, random_state=None,
                 population_size=200, generations=200,
                 mutation_probability=0.8, mutation_ratio=0.03,
                 crossover_probability=0.8, crossover_ratio=0.4):
        """Stratified K-Folds cross-validator with non-overlapping groups.

        The same group will not appear in two different folds.

        The folds are made by preserving the percentage of samples for each class.
        """

        if not isinstance(n_splits, numbers.Integral):
            raise ValueError('The number of folds must be of Integral type. '
                             '%s of type %s was passed.'
                             % (n_splits, type(n_splits)))
        n_splits = int(n_splits)

        if n_splits <= 1:
            raise ValueError(
                "k-fold cross-validation requires at least one"
                " train/test split by setting n_splits=2 or more,"
                " got n_splits={0}.".format(n_splits))

        if not isinstance(population_size, numbers.Integral):
            raise ValueError('The population size must be of Integral type. '
                             '%s of type %s was passed.'
                             % (population_size, type(population_size)))
        population_size = int(population_size)

        if not isinstance(generations, numbers.Integral):
            raise ValueError('The number of generations must be of Integral type. '
                             '%s of type %s was passed.'
                             % (generations, type(generations)))
        generations = int(generations)

        self.n_splits = n_splits
        self.random_state = random_state
        self.population_size = population_size
        self.generations = generations
        self.mutation_probability = mutation_probability
        self.mutation_ratio = mutation_ratio
        self.crossover_probability = crossover_probability
        self.crossover_ratio = crossover_ratio

    def split(self, labels, groups):
        n_samples = len(labels)

        if self.n_splits > n_samples:
            raise ValueError(
                ("Cannot have number of splits n_splits={0} greater"
                 " than the number of samples: n_samples={1}.")
                .format(self.n_splits, n_samples))

        rng = check_random_state(self.random_state)

        n_splits = self.n_splits
        n_classes = np.max(labels) + 1
        n_groups = np.max(groups) + 1

        group_class_counts = np.zeros((n_groups, n_classes), dtype=np.int32)

        for i in range(n_samples):
            group_class_counts[groups[i], labels[i]] += 1

        ga = pyeasyga.GeneticAlgorithm(
            seed_data=group_class_counts,
            population_size=self.population_size,
            generations=self.generations,
            maximise_fitness=False,
            crossover_probability=self.crossover_probability,
            mutation_probability=self.mutation_probability
        )

        def fitness_function(individual, data):
            fold_class_counts = np.zeros((n_splits, n_classes), dtype=np.int32)

            for i in range(n_splits):
                fold_mask = (individual == i)
                fold_class_counts[i] = np.sum(group_class_counts, axis=0, where=fold_mask[:,None])

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                spread = (fold_class_counts.max(0) - fold_class_counts.min(0)) / fold_class_counts.sum(0)
                spread = np.nanmean(spread)

            return spread

        def create_individual(data):
            return rng.randint(0, self.n_splits, n_groups)

        def mutate(individual):
            mutate_indices = rng.choice(len(individual), int(len(individual) * self.mutation_ratio), replace=False)
            for mutate_index in mutate_indices:
                possible_folds = list(range(self.n_splits))
                possible_folds.remove(individual[mutate_index])
                individual[mutate_index] = rng.choice(possible_folds)

        def crossover(parent_1, parent_2):
            child_1, child_2 = parent_1.copy(), parent_2.copy()
            crossover_indices = rng.choice(len(parent_1), int(len(parent_1) * self.crossover_ratio), replace=False)

            for crossover_index in crossover_indices:
                child_1[crossover_index] = parent_2[crossover_index]
                child_2[crossover_index] = parent_1[crossover_index]

            return child_1, child_2

        ga.fitness_function = fitness_function
        ga.create_individual = create_individual
        ga.mutate_function = mutate
        ga.crossover_function = crossover
        ga.run()
        fitness, best_individual = ga.best_individual()

        return fitness, best_individual

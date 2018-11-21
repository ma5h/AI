import random
import heapq
from itertools import repeat
from dna import DNA


class Population:

    POPULATION_SIZE = 100

    def __init__(self):
        self.gene_pool = []

        for index in range(self.POPULATION_SIZE):
            new_dna = DNA()
            self.gene_pool.append(new_dna)

        heapq.heapify(self.gene_pool)

    def evaluate(self):
        max_fitness_gene = heapq.nlargest(1, self.gene_pool)[0]
        max_fitness = float(max_fitness_gene.fitness())

        mating_pool = []
        for gene in self.gene_pool:
            num_occurrences = int(gene.fitness() / max_fitness * 100)
            for _ in repeat(None, num_occurrences):
                mating_pool.append(gene)

        for _ in repeat(None, self.POPULATION_SIZE):
            parent_0 = mating_pool[random.randint(0, len(mating_pool)-1)]
            parent_1 = mating_pool[random.randint(0, len(mating_pool)-1)]

            new_gene = DNA(parent_0.crossover(parent_1))
            heapq.heappush(self.gene_pool, new_gene)

        self.gene_pool = heapq.nlargest(self.POPULATION_SIZE, self.gene_pool)

        return self.gene_pool[0]

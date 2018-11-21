import random
from itertools import repeat


class DNA:

    GENE_SIZE = 10
    MUTATION_RATE = 0.05

    def __init__(self, o_gene=None):
        if o_gene:
            self.gene = o_gene
        else:
            self.generate_gene()
        self.mutation()
        self.fit = self.fitness()

    def generate_gene(self):
        self.gene = []

        for _ in repeat(None, self.GENE_SIZE):
            self.gene.append(random.randint(0, 1))

    def crossover(self, other_dna):
        cut_index = random.randint(0, self.GENE_SIZE-1)
        new_gene = self.gene[:cut_index] + other_dna.gene[cut_index:]
        return new_gene

    def mutation(self):
        for i in range(self.GENE_SIZE):
            if random.uniform(0, 1) < self.MUTATION_RATE:
                self.gene[i] = random.randint(0, 1)
        self.fit = self.fitness()

    def fitness(self):
        group_0 = [x for x in self.gene if x == 0]
        group_1 = [x for x in self.gene if x == 1]

        group_0_sum = 0
        for i in range(len(self.gene)):
            group_0_sum += (i+1) if self.gene[i] == 0 else 0

        group_1_mul = 1
        for i in range(len(self.gene)):
            group_1_mul *= (i+1) if self.gene[i] == 1 else 1

        fitness_size_value = 200 if len(group_0) == len(group_1) else 0
        fitness_sum_value = (36 - abs(36 - group_0_sum)) * 60
        fitness_mul_value = 360 - abs(360 - group_1_mul)
        fitness_value = fitness_size_value + fitness_sum_value + fitness_mul_value

        return fitness_value

    def __cmp__(self, other):
        return cmp(self.fit, other.fit)

    def __str__(self):
        return "gene: " + str(self.gene) + ", fitness: " + str(self.fitness())

from population import Population

if __name__ == "__main__":
    pop = Population()

    iterations = 50
    res = None
    while iterations:
        res = pop.evaluate().gene
        iterations -= 1

        group_0 = []
        for i in range(len(res)):
            if res[i] == 0:
                group_0.append(i+1)

        group_1_mul = 1
        group_1 = []
        for i in range(len(res)):
            group_1_mul *= (i + 1) if res[i] == 1 else 1
            if res[i] == 1:
                group_1.append(i+1)

        print "iteration: " + str(iterations) + \
              ", Result: " + str(res) + \
              ", group_0_sum: " + str(sum(group_0)) + \
              ", group_0: " + str(group_0) + \
              ", group_1_mul: " + str(group_1_mul) + \
              ", group_1: " + str(group_1)

        # Result: [1, 0, 1, 1, 1, 1, 0, 0, 0, 0], group_0_sum: 36, group_1_mul: 360
        # group_0: [2, 7, 8, 9, 10]
        # group_1: [1, 3, 4, 5, 6]

from deap import base, creator, tools
from random import random, randint

import algo.functions_const
from output.generateoutput import generate_csv, generate_plot

bounds = algo.functions_const.BEALE_FUNCTION_CONST

def decode(bound, n_bits, bitstring):
    decoded = list()
    largest = 2 ** n_bits
    for i in range(len(bound)):
        start, end = i * n_bits, (i * n_bits) + n_bits
        substring = bitstring[start:end]
        chars = ''.join([str(s) for s in substring])
        integer = int(chars, 2)
        value = bound[i][0] + (integer / largest) * (bound[i][1] - bound[i][0])
        decoded.append(value)
    return decoded


def individual(icls):
    genome = list()
    for x in range(0, 40):
        genome.append(randint(0, 1))
    return icls(genome)


def fitnessFunction(individual):
    x = decode(bounds, int(len(individual) / 2), individual)
    result = pow((1.5 - x[0] + x[0] * x[1]), 2) + pow(2.25 - x[0] + x[0] * pow(x[1], 2), 2) + pow(
        (2.625 - x[0] + x[0] * pow(x[1], 3)), 2)

    return result,


def deap(user_input):
    bounds = algo.functions_const.BEALE_FUNCTION_CONST
    sizePopulation = user_input.population_amount
    probabilityMutation = user_input.mutation_probability
    probabilityCrossover = user_input.cross_probability
    numberIteration = user_input.epochs_amount
    maximum = user_input.maximum
    mutationMethod= user_input.mutation_method
    crossMethod = user_input.cross_method
    selectionMethod = user_input.selection_method
    print("#######################################\n" + str(maximum) + "\n############################################")
    if maximum:
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)
    else:
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)
    if user_input.elite_strategy:
        numberElitism = 1
    else:
        numberElitism = 0
    toolbox = base.Toolbox()
    toolbox.register('individual', individual, creator.Individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", fitnessFunction)

    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)

    pop = toolbox.population(n=sizePopulation)
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    gen_b_rows = []
    gen_avg_rows = []
    gen_std_dev_rows = []
    g = 0
    while g < numberIteration:
        g = g + 1
        print("-- Generation %i --" % g)
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
        listElitism = []
        fits = [ind.fitness.values[0] for ind in pop]
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x * x for x in fits)
        std = abs(sum2 / length - mean ** 2) ** 0.5
        best_ind = tools.selBest(pop, 1)[0]
        gen_b_rows.append([str(g), best_ind.fitness.values[0]])
        gen_avg_rows.append([str(g), mean])
        gen_std_dev_rows.append([str(g), std])
        for x in range(0, numberElitism):
            listElitism.append(tools.selBest(pop, 1)[0])
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            # cross two individuals with probability CXPB
            if random() < probabilityCrossover:
                toolbox.mate(child1, child2)
            # fitness values of the children
            # must be recalculated later
            del child1.fitness.values
            del child2.fitness.values
        for mutant in offspring:
            # mutate an individual with probability MUTPB
            if random() < probabilityMutation:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        print(" Evaluated %i individuals" % len(invalid_ind))
        pop[:] = offspring + listElitism
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x * x for x in fits)
        std = abs(sum2 / length - mean ** 2) ** 0.5
        print(" Min %s" % min(fits))
        print(" Max %s" % max(fits))
        print(" Avg %s" % mean)
        print(" Std %s" % std)
    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual is %s, %s" % (decode(bounds, 20, best_ind), best_ind.fitness.values))
    #
    print("-- End of (successful) evolution --")
    return gen_b_rows, gen_avg_rows, gen_std_dev_rows

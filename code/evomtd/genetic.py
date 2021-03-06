#!/usr/bin/env python3
"""
    This is the main genetic algorithm based on the sample
    code of TR4NSDUC7OR for an article in robologs.net
"""
__author__ = "Ernesto Serrano"
__license__ = "GPLv3"
__email__ = "erseco@correo.ugr.es"


from evomtd.fitness import calculate_fitness
from evomtd.config.nginx import generate_random_config, mutate_config

import random
import click
from pytictoc import TicToc
from pprint import pprint

genes = 15  # The length of each individual's genetic material
individuals = 20  # The number of individuals in the population
pressure = 2  # How many individuals are selected for reproduction. Must be greater than 2
mutation_chance = 0.2  # The probability that an individual mutates
generations = 32  # The number of generations that we will evolve
crossover_type = 1  # The crossover type, can be 1 or 2
mutation_type_random = True  # Set if the mutation is random or +-1
tournament_size = 2

def print_variable_info():
    print("genes: %d" % genes)
    print("individuals : %d" % individuals)
    print("generations: %d" % generations)


def individual():
    """
        Create a random individual using the function defined in our
        NGINX generator
    """
    config = generate_random_config()
    # return [fitness(config), config]
    return config


def initialize():
    """
        Create a new population of individuals
    """
    return [individual() for i in range(individuals)]


def crossover_one_point(individual1, individual2):
    """
        Executes a one point crossover on the input individuals.
    """

    # A random crosspoint is chosen to make the exchange
    crosspoint = random.randint(1, genes - 1)

    return individual2[:crosspoint] + individual1[crosspoint:]


def crossover_two_points(individual1, individual2):
    """
        Executes a two-point crossover on the input individuals.
    """

    # Two random cross points is chosen to make the exchange
    crosspoint1 = random.randint(1, genes - 3)
    crosspoint2 = random.randint(crosspoint1, genes - 2)
#    print( "Points ", genes, crosspoint1, crosspoint2 )
    return individual1[:crosspoint1] + individual2[crosspoint1:crosspoint2] + individual1[crosspoint2:]


def crossover(individual1, individual2):

    # Genetic material from parents is mixed into the new individual
    if crossover_type == 1:
        result = crossover_one_point(individual1, individual2)
    else:
        result = crossover_two_points(individual1, individual2)

    return (calculate_fitness(result), result)

def minTournament(population, k, tournsize):
    selection = []
    for _ in range(k):
        players = random.sample(population, tournsize)
        selection.append(min(players))
    return selection[:]

def selection_and_reproduction(population):
    """
        Scores all elements of the population and keeps the best.
        by saving them under 'selected'.
        Then mix the genetic material of the chosen ones to create new individuals and
        fill in the population (also keeping a copy of the selected individuals without the
        modify).
    """

    selected =  minTournament(population, k=len(population), tournsize = tournament_size)
    # print("Selected")
    # pprint(selected)

    # Shuffle the individuals
    # random.shuffle(selected)
    crossed_population = []

    # Genetic material is mixed to create new individuals
    for i in range(0, len(selected)):
        parent = random.sample(selected, 2)  # Two parents are selected
        # Generate a new crossed individual
        crossed_individual = mutate_config(crossover_two_points(parent[0][1], parent[1][1]))

        # Add the crossed one to the population
        crossed_population.append(crossed_individual)

    # print("crossed")
    # pprint(crossed_population)

    # print("Computing fitness")
    crossed_population = [(calculate_fitness(i), i) for i in crossed_population]

    # Add the crossed_population to the population
    population = population + crossed_population

    # Sort again the population
    population = sorted(population, key=lambda x: x[0])[0:individuals]

    print("sorted")
    pprint(population)

    return population  # The array now has a new population of individuals, which are returned.

def print_results(initial_population, last_population):
    """
        Print the results
    """
    print("")
    print("Población de %d individuos durante %d generaciones" % (individuals, generations))
    print("Población inicial:")
    pprint(initial_population)
    print("Población final:")
    pprint(last_population)


@click.command()
@click.option('--individuals', '-i', 'individuals_number', help='Number of individuals', default=16)
def main(individuals_number):

    global individuals
    individuals = individuals_number
    print_variable_info()

    t = TicToc()
    t.tic()

    # Initialize a population
    population = initialize()

    population = [(calculate_fitness(i), i) for i in population] # Calculates the fitness of each individual, and stores it in pairs ordered in the form (5 , [1,2,1,1,1,4,1,8,9,4,1])

    initial_population = sorted(population, key= lambda x: x[0])

    # Evolves the population
    for i in range(generations):
        population = selection_and_reproduction(population)

    # Print the results
    print_results(initial_population, population)

    t.toc()


if __name__ == "__main__":

    main()

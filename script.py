import math
import random
from heapq import heappush, heappop

cities = [
    'F',  # "Fortaleza",
    'C',  # "Caucaia",
    'J',  # "Juazeiro do Norte",
    'M',  # "Maracanaú"
    'S'  # "SOBRAL"
]
costs = [
    [0, 10, 100, 50, 23],
    [10, 0, 20, 20, 12],
    [100, 20, 0, 10, 50],
    [50, 20, 10, 0, 17],
    [23, 12, 50, 17, 0]
]

# Since we will always be back to initial state, doesn't seem smart to set start state inside the DNA
bases = "1234"  # == C J M S


def convert_chromosome(chromosome):
    if type(chromosome) is str:
        return list(chromosome)
    return ''.join(chromosome)


def fitness(chromosome: str, invert=False) -> int:
    cost = 0
    prev = 0
    for dna in chromosome:
        n = int(dna)
        cost += costs[prev][n]
        prev = n

    total_cost = (cost + costs[int(chromosome[len(chromosome) - 1])][0])
    return total_cost if invert is False else -total_cost


random_gen = random.Random()


def genesis(n: int) -> list[str]:
    pop = []
    for _ in range(n):
        dna = random_gen.sample(bases, len(bases))
        pop.append(convert_chromosome(dna))

    return pop


def progenitor_selection(population_set: list[str], choice_p=.2) -> list[tuple[str, str]]:
    progenitors = []
    valuable_progenitors = []
    for gene in population_set:
        v = fitness(gene)
        valuable_progenitors.append((gene, v))

    sorted_values = sorted(valuable_progenitors, key=lambda x: x[1])
    random_gen.randint(0, len(sorted_values) - 1)

    for index, (gene, fit) in enumerate(sorted_values):
        one = random_gen.random() < choice_p

        if index == len(sorted_values) - 1:
            random_index = 0 if one else random_gen.randint(index, len(sorted_values) - 1)
        else:
            random_index = (index + 1) if one else random_gen.randint(index, len(sorted_values) - 1)

        progenitors.append(
            (gene, sorted_values[random_index][0])
        )

    return progenitors


def mate_progenitors(progenitors: tuple[str, str], mate=.5) -> str:
    dad, mom = progenitors
    finish = int(mate * len(dad))
    son = convert_chromosome(dad[:finish])

    mom_copy = convert_chromosome(mom)
    # mom_copy.reverse()
    for gene in mom_copy:
        if gene not in son:
            son.append(gene)
            finish += 1

        if finish == len(dad):
            break

    return convert_chromosome(son)


def mutate(cromo: str, mp=.1):
    chromo2 = convert_chromosome(cromo)
    while random_gen.random() < mp:
        a = random_gen.randint(0, len(chromo2) - 1)
        b = random_gen.randint(0, len(chromo2) - 1)
        chromo2[a], chromo2[b] = chromo2[b], chromo2[a]

    return convert_chromosome(chromo2)


if __name__ == '__main__':
    heap = []

    parents = genesis(5)

    # for chromo in parents:
    #     v = fitness(chromo)
    #     heappush(heap, (v, chromo))
    #
    # selection = progenitor_selection(parents)
    #
    # parents = []
    # for mate in selection:
    #     son = mate_progenitors(mate)
    #     son = mutate(son)
    #     parents.append(son)
    #
    # for chromo in parents:
    #     v = fitness(chromo)
    #     heappush(heap, (v, chromo))
    #
    # pop = heappop(heap)
    #
    # print(pop)

    repeated_v = 0
    last_v = math.inf
    for _ in range(100_000):
        internal_heap = []

        selection = progenitor_selection(parents)

        parents = []
        for mate in selection:
            son = mate_progenitors(mate)
            son = mutate(son)
            parents.append(son)

        for chromo in parents:
            v = fitness(chromo)
            heappush(internal_heap, (v, chromo))

        best_from_gen = internal_heap[0]
        heappush(heap, best_from_gen)

        if last_v == best_from_gen[0]:
            repeated_v += 1
            if repeated_v >= 10:
                break
        else:
            last_v = best_from_gen[0]
            repeated_v = 0

    print("Best: ", heap[0])

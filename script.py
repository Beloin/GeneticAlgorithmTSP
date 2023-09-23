import math
import random
from heapq import heappush, heappop

cities = [
    "FORTALEZA",
    "CAUCAIA",
    "JUAZEIRO DO NORTE",
    "MARACANAÚ",
    "SOBRAL",
    "CRATO",
    "ITAPIPOCA",
    "MARANGUAPE",
    "IGUATU",
    "QUIXADÁ",
    "PACATUBA",
    "QUIXERAMOBIM",
    "AQUIRAZ",
    "CANINDÉ",
    "CRATEÚS",
    "ARACATI",
    "PACAJUS",
    "RUSSAS",
    "ICÓ",
    "TIANGUÁ",
]

costs = [
    [0, 20, 500, 30, 220, 400, 90, 40, 320, 220, 10, 180, 25, 130, 260, 110, 35, 280, 170, 410],
    [20, 0, 480, 28, 240, 420, 110, 60, 300, 200, 8, 160, 15, 140, 270, 100, 25, 260, 150, 400],
    [500, 480, 0, 510, 180, 560, 410, 470, 260, 360, 490, 320, 475, 375, 190, 410, 485, 170, 295, 60],
    [30, 28, 510, 0, 280, 460, 50, 75, 320, 220, 22, 190, 20, 140, 270, 100, 25, 260, 150, 400],
    [220, 240, 180, 280, 0, 360, 190, 260, 330, 240, 235, 70, 220, 45, 260, 220, 245, 30, 155, 200],
    [400, 420, 560, 460, 360, 0, 510, 500, 160, 60, 410, 190, 390, 440, 540, 300, 420, 400, 390, 520],
    [90, 110, 410, 50, 190, 510, 0, 50, 270, 170, 85, 140, 35, 70, 180, 65, 100, 160, 90, 350],
    [40, 60, 470, 75, 260, 500, 50, 0, 310, 210, 35, 150, 25, 95, 220, 55, 80, 210, 100, 360],
    [320, 300, 260, 320, 330, 160, 270, 310, 0, 100, 310, 140, 295, 195, 110, 230, 260, 140, 30, 250],
    [220, 200, 360, 220, 240, 60, 170, 210, 100, 0, 220, 100, 195, 170, 300, 60, 120, 70, 165, 180],
    [10, 8, 490, 22, 235, 410, 85, 35, 310, 220, 0, 150, 15, 120, 250, 80, 15, 250, 140, 380],
    [180, 160, 320, 190, 70, 190, 140, 150, 140, 100, 150, 0, 155, 30, 230, 90, 115, 90, 15, 200],
    [25, 15, 475, 20, 220, 390, 35, 25, 295, 195, 15, 155, 0, 115, 245, 75, 10, 245, 135, 375],
    [130, 140, 375, 140, 45, 440, 70, 95, 195, 170, 120, 30, 115, 0, 290, 100, 125, 45, 90, 225],
    [260, 270, 190, 270, 260, 540, 180, 220, 110, 300, 250, 230, 245, 290, 0, 320, 350, 220, 170, 80],
    [110, 100, 410, 100, 220, 300, 65, 55, 230, 60, 80, 90, 75, 100, 320, 0, 65, 160, 100, 300],
    [35, 25, 485, 25, 245, 420, 100, 80, 260, 120, 15, 115, 10, 125, 350, 65, 0, 235, 125, 365],
    [280, 260, 170, 260, 30, 400, 160, 210, 140, 70, 250, 90, 245, 45, 220, 160, 235, 0, 125, 170],
    [170, 150, 295, 150, 155, 390, 90, 100, 30, 165, 140, 15, 135, 90, 170, 100, 125, 125, 0, 240],
    [410, 400, 60, 400, 200, 520, 350, 360, 250, 180, 380, 200, 375, 225, 80, 300, 365, 170, 240, 0]
]


def convert_chromosome(chromosome):
    if type(chromosome) is str:
        return chromosome.split(',')
    return ','.join(chromosome)


# Since we will always be back to initial state, doesn't seem smart to set start state inside the DNA
b = []
for i in range(1, len(costs)):
    b.append(str(i))
bases = convert_chromosome(b)


def fitness(chromosome: str, invert=False) -> int:
    cost = 0
    prev = 0
    chromosome = convert_chromosome(chromosome)
    for dna in chromosome:
        n = int(dna)
        cost += costs[prev][n]
        prev = n

    total_cost = cost + costs[int(chromosome[len(chromosome) - 1])][0]
    return total_cost if invert is False else -total_cost


random_gen = random.Random()


def genesis(n: int) -> list[str]:
    pop = []
    for _ in range(n):
        c_chromo = convert_chromosome(bases)
        dna = random_gen.sample(c_chromo, len(c_chromo))
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
    dad = convert_chromosome(dad)
    finish = int(mate * len(dad))
    son = dad[:finish]

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


def pretty_print(chromossome: str):
    chromosome = convert_chromosome('0,' + chromossome)
    print('Path:\n\t', end='')
    for base in chromosome:
        index = int(base)
        print(cities[index] + ' -> ', end='')

    print(cities[0])


def get_mean(heap: list[tuple[int, str]]):
    fullsize = 0
    for v, _ in heap:
        fullsize += v

    return fullsize / len(heap)


if __name__ == '__main__':
    heap = []

    parents = genesis(5)

    repeated_v = 0
    last_v = math.inf
    for _ in range(100_000):
        if _ and _ % 1000 == 0:
            print(f"Current Generation: {_}\n\tBest: {heap[0]} -> Mean: {get_mean(heap)}")

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

    best = heap[0]
    print("Best: ", best)
    pretty_print(best[1])

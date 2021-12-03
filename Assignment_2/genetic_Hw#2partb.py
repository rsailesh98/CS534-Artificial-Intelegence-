import numpy as np, random, operator, pandas as pd
import matplotlib.pyplot as plt

def create_total(size, city_number):
    total = []
    for i in range(0, size):
        total.append(new(city_number))

    return total

def pick_mate(N):

    i = random.randint(0, N)
    return i

def dist(i, j):

    return np.sqrt((i[0] - j[0]) ** 2 + (i[1] - j[1]) ** 2)

def score_total(total, CityList):

    scores = []

    for i in total:
        scores.append(fitness(i, CityList))
    return scores

def fitness(path, CityList):

    score = 0
    for i in range(1, len(path)):
        k = int(path[i - 1])
        l = int(path[i])

        score = score + dist(CityList[k], CityList[l])

    return score

def new(city_number):

    pop = set(np.arange(city_number, dtype=int))
    path = list(random.sample(pop, city_number))

    return path

def crossover(a, b):

    child = []
    childA = []
    childB = []

    geneA = int(random.random() * len(a))
    geneB = int(random.random() * len(a))

    start_gene = min(geneA, geneB)
    end_gene = max(geneA, geneB)

    for i in range(start_gene, end_gene):
        childA.append(a[i])

    childB = [item for item in a if item not in childA]
    child = childA + childB

    return child

def mutate(path, probablity):


    path = np.array(path)
    for swaping_p in range(len(path)):
        if (random.random() < probablity):
            swapedWith = np.random.randint(0, len(path))

            temp1 = path[swaping_p]

            temp2 = path[swapedWith]
            path[swapedWith] = temp1
            path[swaping_p] = temp2

    return path

def selection(popRanked, eliteSize):
    selectionResults = []
    result = []
    for i in popRanked:
        result.append(i[0])
    for i in range(0, eliteSize):
        selectionResults.append(result[i])

    return selectionResults

def rankpaths(total, List_Cities):
    fitnessResults = {}
    for i in range(0, len(total)):
        fitnessResults[i] = fitness(total[i], List_Cities)
    return sorted(fitnessResults.items(), key=operator.itemgetter(1), reverse=False)

def breedtotal(mating_pool):
    in_children = []
    for i in range(len(mating_pool) - 1):
        in_children.append(crossover(mating_pool[i], mating_pool[i + 1]))
    return in_children

def mutatetotal(in_children, mutation_rate):
    new_generation = []
    for i in in_children:
        muated_child = mutate(i, mutation_rate)
        new_generation.append(muated_child)
    return new_generation

def matingPool(total, selectionResults):
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(total[index])
    return matingpool

def next_generation(List_Cities, current_total, mutation_rate, elite_size):
    total_rank = rankpaths(current_total, List_Cities)

    selection_result = selection(total_rank, elite_size)

    mating_pool = matingPool(current_total, selection_result)

    in_children = breedtotal(mating_pool)

    next_generation = mutatetotal(in_children, mutation_rate)

    return next_generation


def genetic_algorithm(List_Cities, size_total=2000, elite_size=85, mutation_Rate=0.01, generation=2000):
    pop = []
    progress = []

    Number_of_cities = len(List_Cities)

    total = create_total(size_total, Number_of_cities)
    progress.append(rankpaths(total, List_Cities)[0][1])
    print(f"initial path dist {progress[0]}")
    print(f"initial path {total[0]}")
    for i in range(0, generation):
        pop = next_generation(List_Cities, total, mutation_Rate, elite_size)
        progress.append(rankpaths(pop, List_Cities)[0][1])

    rank_ = rankpaths(pop, List_Cities)[0]

    print(f"Best path :{pop[rank_[0]]} ")
    print(f"best path dist {rank_[1]}")
    plt.plot(progress)
    plt.ylabel('dist')
    plt.xlabel('Generation')
    plt.show()

    return rank_, pop

cityList = []

for i in range(0, 25):
    x = int(random.random() * 200)
    y = int(random.random() * 200)
    cityList.append((x, y))

rank_, pop = genetic_algorithm(List_Cities=cityList)

x_axis=[]
y_axis=[]
for i in cityList:
    x_axis.append(i[0])
    y_axis.append(i[1])

plt.scatter(x_axis,y_axis)
plt.show()

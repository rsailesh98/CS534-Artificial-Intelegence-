import random

def randomans(tsp):
    cities = list(range(len(tsp)))
    ans = []

    for i in range(len(tsp)):
        randomCity = cities[random.randint(0, len(cities) - 1)]
        ans.append(randomCity)
        cities.remove(randomCity)

    return ans

def distance(tsp, ans):
    distance = 0
    for i in range(len(ans)):
        distance += tsp[ans[i - 1]][ans[i]]
    return distance

def getneighbors(ans):
    neighbors = []
    for i in range(len(ans)):
        for j in range(i + 1, len(ans)):
            neighbor = ans.copy()
            neighbor[i] = ans[j]
            neighbor[j] = ans[i]
            neighbors.append(neighbor)
    return neighbors

def getidealneighbor(tsp, neighbors):
    idealdistance = distance(tsp, neighbors[0])
    idealneighbor = neighbors[0]
    for neighbor in neighbors:
        currentdistance = distance(tsp, neighbor)
        if currentdistance < idealdistance:
            idealdistance = currentdistance
            idealneighbor = neighbor
    return idealneighbor, idealdistance

def hillClimbing(tsp):
    currentans = randomans(tsp)
    currentdistance = distance(tsp, currentans)
    neighbors = getneighbors(currentans)
    idealneighbor, idealneighbordistance = getidealneighbor(tsp, neighbors)

    while idealneighbordistance < currentdistance:
        currentans = idealneighbor
        currentdistance = idealneighbordistance
        neighbors = getneighbors(currentans)
        idealneighbor, idealneighbordistance = getidealneighbor(tsp, neighbors)

    return currentans, currentdistance

def main():
    tsp = [
        [0, 800, 1000, 600],
        [800, 0, 600, 1000],
        [1000, 600, 0, 800],
        [600, 600, 800, 0]
    ]

    print(hillClimbing(tsp))

if __name__ == "__main__":
    main()
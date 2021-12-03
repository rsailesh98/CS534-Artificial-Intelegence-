import numpy as np

ACTIONS = ((0, "Move Forward"),
           (1, "Go Right"),
           (2, "Go Left"),
           (3, "Remove Dirt"),
           (4, "Turn Off"),
           (-1, "Break"),)


class RandomAgent(object):
    def __init__(item):
        item.reward = 0

    def act(item, observation, reward):
        item.reward += reward

        action = ACTIONS[np.random.randint(len(ACTIONS))]
        return action


class ReflexAgent(object):
    def __init__(item):
        item.reward = 0

    def act(item, observation, reward):
        item.reward += reward

        if observation['dirt'] == 1:
            return ACTIONS[3]

        if observation['obstacle'] == 1:
            return ACTIONS[1]

        return ACTIONS[np.random.randint(3)]


class InternalAgent(object):
    def __init__(item):
        item.reward = 0
        item.map = [[-1, -1], [-1, -1]]

        item.x = 0
        item.y = 0
        item.facing = 0

    def add_map(item):

        side = item.edge()

        while side >= 0:
            if side == 0:
                item.map.insert(0, [-1] * len(item.map[0]))
                item.x += 1

            elif side == 1:
                for row in item.map:
                    row.append(-1)

            elif side == 2:
                item.map.append([-1] * len(item.map[0]))

            elif side == 3:
                for row in item.map:
                    row.insert(0, -1)
                item.y += 1

            side = item.edge()

    def edge(item):
        if item.x == 0:
            return 0

        elif item.y == len(item.map[0]) - 1:
            return 1

        elif item.x == len(item.map) - 1:
            return 2

        elif item.y == 0:
            return 3

        return -1

    def forward(item):
        if item.facing == 0:
            item.x -= 1

        elif item.facing == 1:
            item.y += 1

        elif item.facing == 2:
            item.x += 1

        elif item.facing == 3:
            item.y -= 1

    def backwards(item):
        if item.facing == 0:
            item.x += 1

        elif item.facing == 1:
            item.y -= 1

        elif item.facing == 2:
            item.x -= 1

        elif item.facing == 3:
            item.y += 1

    def update_map(item, observation):
        if observation['dirt'] == 1:
            item.map[item.x][item.y] = 1

        elif observation['home'] == 1:
            item.map[item.x][item.y] = 3

        else:
            item.map[item.x][item.y] = 0

        if observation['obstacle'] == 1:
            item.map[item.x][item.y] = 2
            item.backwards()

        x_len = len(item.map) - 1
        y_len = len(item.map[0]) - 1

        if item.map[0][1] == 2 and item.map[1][0] == 2:
            item.map[0][0] = 2

        if item.map[0][y_len - 1] == 2 and item.map[1][y_len] == 2:
            item.map[0][y_len] = 2

        if item.map[x_len - 1][0] == 2 and item.map[x_len][1] == 2:
            item.map[x_len][0] = 2

        if item.map[x_len][y_len - 1] == 2 and item.map[x_len - 1][y_len] == 2:
            item.map[x_len][y_len] = 2


    def next_move(item, next_square):
        if next_square[0] < item.x and item.facing != 0 and item.map[item.x - 1][item.y] != 2:
            action = ACTIONS[2]

        elif next_square[0] < item.x and item.facing == 0 and item.map[item.x - 1][item.y] != 2:
            action = ACTIONS[0]

        elif next_square[0] > item.x and item.facing != 2 and item.map[item.x + 1][item.y] != 2:
            action = ACTIONS[2]

        elif next_square[0] > item.x and item.facing == 2 and item.map[item.x + 1][item.y] != 2:
            action = ACTIONS[0]

        elif next_square[1] > item.y and item.facing != 1 and item.map[item.x][item.y + 1] != 2:
            action = ACTIONS[2]

        elif next_square[1] > item.y and item.facing == 1 and item.map[item.x][item.y + 1] != 2:
            action = ACTIONS[0]

        elif next_square[1] < item.y and item.facing != 3 and item.map[item.x][item.y - 1] != 2:
            action = ACTIONS[2]

        elif next_square[1] < item.y and item.facing == 3 and item.map[item.x][item.y - 1] != 2:
            action = ACTIONS[0]

        else:
            action = ACTIONS[4]


        if action[0] == 0:
            item.forward()

        if action[0] == 2:
            item.facing = (item.facing - 1) % 4

        return action

    def nearest(item, square_type):

        min_dist = None
        next_square = None

        for i, row in enumerate(item.map):
            for j, square in enumerate(row):
                if square == square_type:
                    dist = (item.x - i) ** 2 + (item.y - j) ** 2
                    if min_dist is None or dist < min_dist:
                        min_dist = dist
                        next_square = (i, j)

        return next_square

    def choose_action(item):

        if item.map[item.x][item.y] == 1:
            return ACTIONS[3]

        next_square = item.nearest(-1)


        if next_square is None:
            next_square = item.nearest(3)

        return item.next_move(next_square)

    def act(item, observation, reward):
        item.reward += reward

        item.update_map(observation)
        item.add_map()


        return item.choose_action()
import numpy as np

class VacuumEnvironment(object):
    def __init__(item, size, dirt):
        item.size = size
        item.dirt = dirt

        item.agent_x = np.random.randint(item.size[0])
        item.agent_y = np.random.randint(item.size[1])
        item.agent_facing = np.random.randint(4)    # For the directions

        item.room = np.zeros((2, item.size[0], item.size[1]))

        for row in range(item.size[0]):
            for col in range(item.size[1]):
                if np.random.uniform() < item.dirt:
                    item.room[0][row][col] = 1


        home_x = np.random.randint(item.size[0])
        home_y = np.random.randint(item.size[1])
        item.room[1][home_x][home_y] = 1

    def state(item, obstacle=False):
        return {"obstacle": int(obstacle),
                "dirt": item.room[0][item.agent_x][item.agent_y],
                "home": item.room[1][item.agent_x][item.agent_y],
                "agent": (item.agent_x, item.agent_y)}

    def has_hit_obstacle(item):
        if (item.agent_facing == 0 and item.agent_x == 0) or \
           (item.agent_facing == 1 and item.agent_y == item.size[1] - 1) or \
           (item.agent_facing == 2 and item.agent_x == item.size[0] - 1) or \
           (item.agent_facing == 3 and item.agent_y == 0):
            return True

        return False

    def forward(item):

        if item.has_hit_obstacle():
            return True

        if item.agent_facing == 0:
            item.agent_x -= 1

        elif item.agent_facing == 1:
            item.agent_y += 1

        elif item.agent_facing == 2:
            item.agent_x += 1

        elif item.agent_facing == 3:
            item.agent_y -= 1

        return False

    def step(item, action):
        obstacle = False
        reward = -1
        done = False

        if action == 0:
            obstacle = item.forward()

        elif action == 1:
            item.agent_facing = (item.agent_facing + 1) % 4

        elif action == 2:
            item.agent_facing = (item.agent_facing - 1) % 4

        elif action == 3:

            if item.room[0][item.agent_x][item.agent_y] == 1:
                reward += 100
                item.room[0][item.agent_x][item.agent_y] = 0

        elif action == 4:

            if item.room[1][item.agent_x][item.agent_y] != 1:
                reward -= 1000

            done = True

        return item.state(obstacle), reward, done
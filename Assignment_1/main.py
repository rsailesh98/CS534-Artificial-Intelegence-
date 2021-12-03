from environments import VacuumEnvironment
from Agents import RandomAgent, ReflexAgent, InternalAgent

environment_size = (12, 12)
DIRT_CHANCE = 0.05


def main():
    env = VacuumEnvironment(environment_size, DIRT_CHANCE)
    agent = InternalAgent()

    print (env.room[0])
    print (env.room[1])

    observation = env.state()
    reward = 0
    done = False
    action = agent.act(observation, reward)
    turn = 1

    while not done:

        observation, reward, done = env.step(action[0])
        print ("Step {0}: Action - {1}".format(turn, action[1]))

        action = agent.act(observation, reward)

        turn += 1

    print (env.room[0])

if __name__ == "__main__":
    main()
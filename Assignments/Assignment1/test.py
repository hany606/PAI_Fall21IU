from dots_env import Dots
from agent import MinMaxBot, RandomBot, CycleBot
from time import sleep

width = 8
height = 8
node_size = 50
env = Dots(width=width, height=height, node_size=node_size, max_num_step=1000)
# bot = MinMaxBot()
bot = RandomBot(width=width, height=height)
# bot = CycleBot(width=width, height=height)

done = False
obs = env.reset()
while not done:
# for i in range(100):
    print(env.num_steps)
    actions = bot.compute_action(obs)
    obs, reward, done, info = env.step(actions)
    env.render(timeout=0.01)

while True:
    env.render()
    # sleep(1)
    

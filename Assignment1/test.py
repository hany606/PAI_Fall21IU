from dots_env import Dots
from agent import MinMaxBot, RandomBot

width = 10
height = 10
node_size = 20
env = Dots(width=width, height=height, node_size=node_size)
# bot = MinMaxBot()
bot = RandomBot(width=width, height=height)


done = False
obs = env.reset()
while not done:
    actions = bot.compute_action(obs)
    obs, reward, done, info = env.step(actions)
    env.render(timeout=700)

from dots_env import Dots
from agent import MinMaxBot, RandomBot, CycleBot
from time import sleep, time

width = 3#15
height = 3#15
node_size = 50
env = Dots(width=width, height=height, node_size=node_size, max_num_step=999)
bot = MinMaxBot()
bot_random = RandomBot(width=width, height=height)
# bot = CycleBot(width=width, height=height)

print("------------ Start planning ------------")
# bot.plan(env=env)
print("------------ Finished planning ------------")
# exit()
done = False
obs = env.reset()
print(f"You are {obs['turn']}")
while not done:
# for i in range(100):
    env.render(timeout=0.1)
    # ------------------------------------ USER ----------------
    # user_input = ""
    # break_flag = True
    # while break_flag:
    #     user_input = input(f"Please input in the following format x,y: ").strip().replace(' ', '')
    #     if(not("," in user_input)):
    #         print("Not correct input, try again")
    #         break_flag = True
    #     else:
    #         user_input = user_input.split(',')
    #         for i in range(2):
    #             try:
    #                 user_input[i] = int(user_input[i])
    #                 break_flag = False
    #             except:
    #                 print("Please enter x and y as integers")
    #                 break_flag = True
    # # ------------------------------------
    # actions = {obs["turn"]: [tuple(user_input)]}
    # obs, reward, done, info = env.step(actions)
    # if(info["error"] == "not_empty_node"):
    #     continue

    # ---------------------------------------------------------------
    while True:
        # actions = bot.compute_action(actions)
        # actions = bot.compute_action(obs, tuple(user_input))
        actions = bot_random.compute_action(obs)
        print("Random bot",actions)
        # input("Enter: ?")
        obs, reward, done, info = env.step(actions)
        if(info["error"] == "not_empty_node"):  # in case of error from the bot then repeat till the bot place it correctly
            continue
        else:
            break

    

    print(reward)
    env.render(timeout=0.1)
    
    while True:
        # actions = bot.compute_action(actions)
        # actions = bot.compute_action(obs, tuple(user_input))
        t1 = time()
        actions = bot.compute_action(env)
        if(actions["red"][0] is None):
            break
        print(f"Time for computation: {time()-t1}")
        print("Minmax bot",actions)
        # input("Enter: ?")
        obs, reward, done, info = env.step(actions)
        if(info["error"] == "not_empty_node"):  # in case of error from the bot then repeat till the bot place it correctly
            continue
        else:
            break

    print(reward)

while True:
    env.render()
    # sleep(1)
    

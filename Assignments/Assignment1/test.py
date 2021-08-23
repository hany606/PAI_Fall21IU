from dots_env import Dots
from agent import MinMaxBot, RandomBot, CycleBot
from time import sleep, time
from cs50TicTacToe import TicTacToe

width = 5#15
height = 4#15
dimensions = [width, height]
node_size = 50
env = Dots(width=width, height=height, node_size=node_size, max_num_step=9999) # TicTacToe()#
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
user_input = ""
while not done:
# for i in range(100):
    env.render(timeout=0.1)
    # ------------------------------------ USER ----------------
    break_flag = True
    user_input_flag = True
    while break_flag:
        if(user_input != "r"):
            user_input = input(f"Please input in the following format x,y or '-' for random: ").strip().replace(' ', '')

        if(user_input == "q"):
            print(env.get_scores())
            exit()

        if(user_input == "-" or user_input == "r"):
            while True:
                actions = bot_random.compute_action(obs)
                print("Random bot",actions)
                # input("Enter: ?")
                obs, reward, done, info = env.step(actions)
                if(info["error"] == "not_empty_node"):  # in case of error from the bot then repeat till the bot place it correctly
                    continue
                else:
                    break
            
            user_input_flag = False
            break
        elif(not("," in user_input)):
            print("Not correct input, try again")
            break_flag = True
        else:
            user_input = user_input.split(',')
            for i in range(2):
                try:
                    user_input[i] = int(user_input[i])
                    if(user_input[i] >= dimensions[i]):
                        raise ValueError("Bigger than dimensions")
                    break_flag = False
                except:
                    print("Please enter x and y as integers")
                    break_flag = True
    # ------------------------------------
    if(user_input_flag): # input from the user not random
        actions = {obs["turn"]: [tuple(user_input)]}
        obs, reward, done, info = env.step(actions)
        if(info["error"] == "not_empty_node"):
            continue

    # ---------------------------------------------------------------
    # while True:
    #     # actions = bot.compute_action(actions)
    #     # actions = bot.compute_action(obs, tuple(user_input))
    #     actions = bot_random.compute_action(obs)
    #     print("Random bot",actions)
    #     # input("Enter: ?")
    #     obs, reward, done, info = env.step(actions)
    #     if(info["error"] == "not_empty_node"):  # in case of error from the bot then repeat till the bot place it correctly
    #         continue
    #     else:
    #         break

    

    print(reward)
    env.render(timeout=0.1)
    
    while True:
        # actions = bot.compute_action(actions)
        # actions = bot.compute_action(obs, tuple(user_input))
        t1 = time()
        actions = bot.compute_action(env, depth=0, max_depth=4, max_width=10, random_explore=False)
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

print("Finished")
while True:
    env.render()
    # sleep(1)



# Max depth is horizon, Max width is obserability
# Max depth: 5, Max width:30 -> worst computation time for single move -> Too much
# Max depth: 5, Max width:10 -> worst computation time for single move: ~5s -> not too good

# Max depth: 8, Max width:3 -> worst computation time for single move: ~200s -> but kinda goo 
# Max depth: 4, Max width:20 -> worst computation time for single move: ~80


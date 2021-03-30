import retro
from datetime import datetime
import time
import random
import itertools
import time
import numpy as np


def get_all_pairwise_actions(possible_actions):
    groupings = []
    for each in itertools.permutations(possible_actions.keys(),2):
        groupings.append(possible_actions[each[0]] + possible_actions[each[1]])
    return groupings
def spin_run(possible_actions, direction, run_distance_before_spin):
    set_of_actions = []
    for i in range(run_distance_before_spin):
        set_of_actions.append(possible_actions[direction])
    set_of_actions.append(possible_actions["DOWN"])
    return set_of_actions
def spin_dash(possible_actions, direction, taps):
    set_of_actions = []
    set_of_actions.append(possible_actions[direction])
    for i in range(taps):
        set_of_actions.append(possible_actions["DOWN"])
        set_of_actions.append(possible_actions["DOWN"] + possible_actions["B"])
    return set_of_actions
def run(possible_actions, direction, run_distance):
    set_of_actions = []
    for i in range(run_distance):
        set_of_actions.append(possible_actions[direction])
    return set_of_actions

def jump(possible_actions, direction, jump_duration):
    set_of_actions = []

    set_of_actions.append(possible_actions["A"])
    set_of_actions.append(possible_actions["A"])
    for i in range(jump_duration):
        set_of_actions.append(possible_actions[direction])

    return set_of_actions

def actions_available(possible_actions, action_chosen, rand = True):
    #https://info.sonicretro.org/index.php?title=File:Sonic2_MD_US_manual.pdf&page=7

    x = {"run_left_spin_X_frames" : spin_run(possible_actions, "LEFT", 100), # This could be a variable amount of running
         "run_left_spin_Y_frames" : spin_run(possible_actions, "LEFT", 200), # This could be a variable amount of running
         "run_right_spin_X_frames" : spin_run(possible_actions, "RIGHT", 100), # This could be a variable amount of running
         "run_right_spin_Y_frames" : spin_run(possible_actions, "RIGHT", 200), # This could be a variable amount of running
         "run_left_X_frames" : run(possible_actions, "LEFT", 100), # This could be a variable amount of running
         "run_left_Y_frames" : run(possible_actions, "LEFT", 200), # This could be a variable amount of running
         "run_right_X_frames" : run(possible_actions, "RIGHT", 100), # This could be a variable amount of running
         "run_right_Y_frames" : run(possible_actions, "RIGHT", 200), # This could be a variable amount of running
         "spindash_right_X_times" : spin_dash(possible_actions, "RIGHT", 5),
         "spindash_left_X_times" : spin_dash(possible_actions, "LEFT", 5),
         "jump_right_X_frames" : jump(possible_actions, "RIGHT", 5),
         "jump_left_X_frames" : jump(possible_actions, "LEFT", 5),
         "jump_up_X_frames" : jump(possible_actions, "RIGHT", 5),
         
     }
    if rand:
        action_chosen = random.randint(0,len(x.keys())-1)
        

    return x[list(x.keys())[action_chosen]], action_chosen

def main():

    # From gensis.json "buttons": ["B", "A", "MODE", "START", "UP", "DOWN", "LEFT", "RIGHT", "C", "Y", "X", "Z"],
    
    actions_by_value = {"B" : 2**11, "A" : 2**10, "START" : 2**8, "UP" : 2**7, "DOWN" : 2**6, "LEFT" : 2**5, "RIGHT" : 2**4, "C" : 2**3, "Y" : 2**2, "X" : 2**1, "Z" : 2**0} # "MODE" : 2**9
    env = retro.make(game='SonicTheHedgehog2-Genesis')
    obs = env.reset()
    obs, rew, done, info = env.step([0] * env.action_space.shape[0])
    env.render()
    q_learner = {}
    #print ("press enter to start")
    #print (obs)
    #print (info)
    #input()
    last_x = info["x"]
    last_y = info["y"]
    reward = 0
    alpha = .9
    gamma = .995
    while True:
        random_action = 35 > random.randint(1,100)
        if info["x"] in q_learner and info["y"] in q_learner[info["x"]]:
            action_selection = np.argmax(q_learner[info["x"]][info["y"]])
        else:
            action_selection = 0
            random_action = True
        action_sequence, action_index = actions_available(actions_by_value, action_selection, random_action)
        last_x = info["x"]
        last_y = info["y"]
        for i in action_sequence:
            binary_value = str(bin(i))
            binary_value = ''.join(list(binary_value)[2:])
            action = list(map(int,list(str(binary_value).zfill(12))))
            
            obs, rew, done, info = env.step(action)

            time.sleep(1.0/60.0)
            env.render()
            if done:
                print ("bdone", done)
                print (info)
                print (rew)
                #print ("WHAT???")
                input()
                obs = env.reset()
                continue
        

         # This seems like it should move to out of the for loop it should run on completion of the whole thing
         # I speculate if we hit "done" there is gonna be something wonky as our state changes drastically
        if last_x not in q_learner:
            q_learner[last_x] = {} 
        if last_y not in q_learner[last_x]:
            q_learner[last_x][last_y] = np.zeros(13)

        if last_x == info["x"]:
            reward += -1

        if last_y == info["y"]:
            reward += -1
        old_value = q_learner[last_x][last_y][action_index]
        next_max = np.argmax(q_learner[last_x][last_y])
        if info["x"] not in q_learner:
            q_learner[info["x"]] = {} 
        if info["y"] not in q_learner[info["x"]]:
            q_learner[info["x"]][info["y"]] = np.zeros(13)
        q_learner[info["x"]][info["y"]][action_index] = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)# Q learner stuff

    env.close()


if __name__ == "__main__":
    main()

'''
/home/hotdog/.local/lib/python3.6/site-packages/retro/data/stable/SonicTheHedgehog2-Genesis/

contest.json
data.json
metadata.json
scenario.json
script.lua
xpos.json
'''
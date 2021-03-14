import retro
from datetime import datetime
import time
import random
import itertools
import time



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

def actions_available(possible_actions):
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
    return x[list(x.keys())[random.randint(0,len(x.keys())-1)]]

def main():

    # From gensis.json "buttons": ["B", "A", "MODE", "START", "UP", "DOWN", "LEFT", "RIGHT", "C", "Y", "X", "Z"],

    actions_by_value = {"B" : 2**11, "A" : 2**10, "START" : 2**8, "UP" : 2**7, "DOWN" : 2**6, "LEFT" : 2**5, "RIGHT" : 2**4, "C" : 2**3, "Y" : 2**2, "X" : 2**1, "Z" : 2**0} # "MODE" : 2**9
    env = retro.make(game='SonicTheHedgehog2-Genesis')
    obs = env.reset()
    
    while True:
        action_sequence = actions_available(actions_by_value)
        for i in action_sequence:
            binary_value = str(bin(i))
            binary_value = ''.join(list(binary_value)[2:])
            action = list(map(int,list(str(binary_value).zfill(12))))
            
            obs, rew, done, info = env.step(action)
           # time.sleep(1.0/60.0)
            env.render()
            if done:
                #print ("bdone", done)
                #print ("WHAT???")
                #input()
                obs = env.reset()
                continue
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
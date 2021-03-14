import retro
from datetime import datetime
import time
import random
import itertools
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
def run(possible_actions, direction, run_distance):
    set_of_actions = []
    for i in range(run_distance):
        set_of_actions.append(possible_actions[direction])
    return set_of_actions


def actions_available(possible_actions):
    x = {"run_left_spin_10_frames" : spin_run(possible_actions, "LEFT", 10), # This could be a variable amount of running
         "run_left_spin_20_frames" : spin_run(possible_actions, "LEFT", 20), # This could be a variable amount of running
         "run_right_spin_10_frames" : spin_run(possible_actions, "RIGHT", 10), # This could be a variable amount of running
         "run_right_spin_20_frames" : spin_run(possible_actions, "RIGHT", 20), # This could be a variable amount of running
         "run_left_10_frames" : run(possible_actions, "LEFT", 10), # This could be a variable amount of running
         "run_left_20_frames" : run(possible_actions, "LEFT", 20), # This could be a variable amount of running
         "run_right_10_frames" : run(possible_actions, "RIGHT", 10), # This could be a variable amount of running
         "run_right_20_frames" : run(possible_actions, "RIGHT", 20), # This could be a variable amount of running
     }
    return x[list(x.keys())[random.randint(0,len(x.keys())-1)]]

def main():

    # From gensis.json "buttons": ["B", "A", "MODE", "START", "UP", "DOWN", "LEFT", "RIGHT", "C", "Y", "X", "Z"],

    actions_by_value = {"B" : 2**11, "A" : 2**10, "START" : 2**8, "UP" : 2**7, "DOWN" : 2**6, "LEFT" : 2**5, "RIGHT" : 2**4, "C" : 2**3, "Y" : 2**2, "X" : 2**1, "Z" : 2**0} # "MODE" : 2**9
    all_pairwise_actions = get_all_pairwise_actions(actions_by_value)
    all_individual_actions = list(map(lambda x: actions_by_value[x], actions_by_value))
    all_actions_we_care_about = all_pairwise_actions + all_individual_actions
    print (len(all_actions_we_care_about))
    env = retro.make(game='SonicTheHedgehog2-Genesis')
    obs = env.reset()
    print (env.action_space.sample())
    last_time = datetime.now()
    while True:
        #action = env.action_space.sample()
        #print (dir(env.action_space.sample()))
        #print (env.action_space.to_jsonable([0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]))
        i = actions_by_value["DOWN"]
        binary_value = str(bin(i))
        #binary_value = '0b10000000000'
        #print (binary_value)
        binary_value = ''.join(list(binary_value)[2:])
        #print (str(binary_value),str(binary_value).zfill(12)) 
        action = list(map(int,list(str(binary_value).zfill(12))))
        
        obs, rew, done, info = env.step(action)
        # Hold the action for a bit
        for j in range(50):
            obs, rew, done, info = env.step(action)
            
            env.render()
            if done:
                print ("bdone", done)
                print ("WHAT???")
                input()
                obs = env.reset()

        i = actions_by_value["DOWN"] + actions_by_value["A"]
        binary_value = str(bin(i))
        binary_value = ''.join(list(binary_value)[2:])
        action = list(map(int,list(str(binary_value).zfill(12))))
        for j in range(5):
            obs, rew, done, info = env.step(action)
            
            env.render()
            if done:
                print ("bdone", done)
                print ("WHAT???")
                input()
                obs = env.reset()

        # Let the action clear out
        for j in range(150):
            obs, rew, done, info = env.step([0] * env.action_space.shape[0])
            
            env.render()
        obs = env.reset()
            #time.sleep(.01)
            
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
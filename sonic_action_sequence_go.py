import retro
from datetime import datetime
import time
import random
def actions_available():
    x = {"jump" : [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], # [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # This is also jump?
     "right" : [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
     "left" : [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
     "down" : [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
     "up" : [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
     "nothing" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     "jump_left" : [0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0],
     "jump_right" : [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
     }
    return x[list(x.keys())[random.randint(0,len(x.keys())-1)]]
def main():


    env = retro.make(game='SonicTheHedgehog2-Genesis', state='AquaticRuinZone.Act2')
    obs = env.reset()
    print (env.action_space.sample())
    obs, rew, done, info = env.step([0] * env.action_space.shape[0])
    last_time = datetime.now()
    time.sleep(5)
    while True:
        
        for j in range(100):
            obs, rew, done, info = env.step([0] * env.action_space.shape[0])
            
            env.render()
            if done:
                print ("bdone", done)
                print ("WHAT???")
                input()
                obs = env.reset()

        action = actions_available()
        print (action)
        # Hold the action for a bit
        for j in range(500):
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
        #obs = env.reset()
            
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
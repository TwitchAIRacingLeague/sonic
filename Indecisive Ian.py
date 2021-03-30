import retro
from datetime import datetime
import time
import random
def main():
    levels = ['AquaticRuinZone.Act1', 'EmeraldHillZone.Act2', 'OilOceanZone.Act1',
              'AquaticRuinZone.Act2', 'HillTopZone.Act1','OilOceanZone.Act2', 
              'CasinoNightZone.Act1', 'HillTopZone.Act2', 'CasinoNightZone.Act2',
              'ChemicalPlantZone.Act1', 'MetropolisZone.Act1','ChemicalPlantZone.Act2',
              'MetropolisZone.Act2', 'MetropolisZone.Act3', #'WingFortressZone',
              'MysticCaveZone.Act1', 'EmeraldHillZone.Act1', 'MysticCaveZone.Act2']

    env = retro.make(game='SonicTheHedgehog2-Genesis') #, state=levels[random.randint(0,len(levels)-1)])
    obs = env.reset()
    env.render()
    print ("press enter to start")
    input()
    action = [0] * env.action_space.shape[0]
    last_time = datetime.now()
    
    while True:
        current_time = datetime.now()
        delta =  (current_time - last_time)
        if delta.seconds >= 1:
            action = env.action_space.sample()
            last_time = current_time
            print ("Resetting time", action)
        else:
            action = [0] * env.action_space.shape[0]
        obs, rew, done, info = env.step(action)
        env.render()
        time.sleep(.01)
        if done:
            env.close()
            env = retro.make(game='SonicTheHedgehog2-Genesis') #, state=levels[random.randint(0,len(levels)-1)])
            obs = env.reset()
    env.close()


if __name__ == "__main__":
    main()

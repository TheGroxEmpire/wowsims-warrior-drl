import numpy as np

import wowsims
from fury import *

import gymnasium as gym
from gymnasium import spaces

class FurySimEnv(gym.Env):
    def __init__(self, render_mode=None):
        Load(True)
        aura_count = len(Auras.Labels)
        target_aura_count = len(TargetAuras.Labels)
        # Rage + sim duration shape count
        other_count = 2
        Spells.register()
        self.spells_count = len(Spells.registered_actions())

        self.last_damage_done = 0

        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(aura_count+target_aura_count+other_count+self.spells_count,), dtype=np.float64)
        # Last action is reserved for doNothing()
        self.action_space = spaces.Discrete(self.spells_count+1)

    def _get_obs(self):
        Auras.update()
        TargetAuras.update()
        Spells.update()
        resources = np.array([wowsims.getRemainingDuration(), wowsims.getRage()], dtype=np.float64)
        return np.concatenate((resources, Auras.Durations, TargetAuras.Durations, Spells.Cooldowns))
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed, options=options)
        Reset()
        self.last_damage_done = 0
        observation = self._get_obs()
        info = {}
        return observation, info
    
    def step(self, action):
        truncated = False
        cast = False
        terminated, needs_input = False, False
        while not (terminated or needs_input):
            needs_input = wowsims.needsInput()
            terminated = wowsims.step()
        
        if needs_input :
            # Last index of action means DoNothing
            if action == self.spells_count:
                cast = wowsims.doNothing()
            else :
                cast = wowsims.trySpell(Spells.registered_actions()[action])
        
        damage_done = wowsims.getDamageDone()
        current_time = wowsims.getCurrentTime()
        dps = 0 if current_time <= 0 else damage_done / current_time
        damage_this_step = damage_done - self.last_damage_done
        self.last_damage_done = damage_done

        reward = dps / 10000

        observation = self._get_obs()
        
        info = {'dps': dps, 'spell metrics': wowsims.getSpellMetrics(), 'debug log': [current_time, action, cast, damage_this_step, damage_done, observation[1]]}
            
        return observation, reward, terminated, truncated, info

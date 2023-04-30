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

        self.last_damage_done = 0

        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(aura_count+target_aura_count+other_count,), dtype=np.float64)

        self.action_space = spaces.Discrete(len(Spells.registered_actions()))

    def _get_obs(self):
        Auras.update()
        TargetAuras.update()
        resources = np.array([wowsims.getRemainingDuration(), wowsims.getRage()], dtype=np.float64)
        return np.concatenate((resources, Auras.Durations, TargetAuras.Durations))
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed, options=options)
        Reset()
        self.last_damage_done = 0
        observation = self._get_obs()
        info = {}
        return observation, info
    
    def step(self, action):
        truncated = False
        terminated, needs_input = False, False
        while not (terminated or needs_input):
            needs_input = wowsims.needsInput()
            terminated = wowsims.step()
        if needs_input :
            wowsims.trySpell(Spells.registered_actions()[action])
        damage_done = wowsims.getDamageDone()
        reward = (damage_done - self.last_damage_done) / 1000
        self.last_damage_done = damage_done
        observation = self._get_obs()
        dps = damage_done / SettingsGetDuration()
        info = {'dps': dps}
        return observation, reward, terminated, truncated, info

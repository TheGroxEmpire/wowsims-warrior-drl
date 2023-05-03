import numpy as np

import wowsims
from fury import *

import gymnasium as gym
from gymnasium import spaces

class FurySimEnv(gym.Env):
    def __init__(self, config):
        Load(True)
        aura_count = len(Auras.Labels)
        target_aura_count = len(TargetAuras.Labels)
        # Rage, sim duration, melee swing time [MH, OH] shape count
        other_count = 4
        Spells.register()
        self.spells_count = len(Spells.registered_actions())

        self.last_damage_done = 0

        self.observation_space = gym.spaces.Box(low=-1, high=1, shape=(aura_count+target_aura_count+other_count+self.spells_count,), dtype=np.float64)
        # Last action is reserved for doNothing()
        self.action_space = spaces.Discrete(self.spells_count+1)

        self.reward_time_factor = config["reward_time_factor"] if config["reward_time_factor"] != 0 else 0
        self.dps_reward_coef = config["dps_reward_coef"] if config["dps_reward_coef"] != 1000 else 1000

    def _get_obs(self):
        Auras.update()
        # TargetAuras.update()
        Spells.update()
        resources = np.array([wowsims.getRemainingDuration() / wowsims.getIterationDuration(), wowsims.getRage()], dtype=np.float64)
        return np.concatenate((resources, Auras.Durations, TargetAuras.Durations, Spells.Cooldowns, AutoAttacks.get_swing_time()))
    
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
                # Sometimes idle can fail if it's on the end of the fight, we don't want to punish the model for that
            else :
                cast = wowsims.trySpell(Spells.registered_actions()[action])
        
        damage_done = wowsims.getDamageDone()
        dps = 0 if wowsims.getCurrentTime() <= 0 else damage_done / wowsims.getCurrentTime()
        damage_this_step = damage_done - self.last_damage_done
        self.last_damage_done = damage_done
        remaining_duration = wowsims.getRemainingDuration()

        reward = dps / self.dps_reward_coef / (remaining_duration**self.reward_time_factor) if remaining_duration > 0 else dps / self.dps_reward_coef

        observation = self._get_obs()
        
        info = {'dps': dps, 'spell metrics': wowsims.getSpellMetrics(), 'debug log': [wowsims.getCurrentTime(), action, cast, damage_this_step, damage_done, observation[1]]}
            
        return observation, reward, terminated, truncated, info

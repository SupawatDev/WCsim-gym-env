from gym.envs.registration import register

register(id='wcsim-env-v0',
         entry_point='wcsim_env.envs:WCSimEnv')

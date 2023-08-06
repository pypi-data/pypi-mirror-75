import time
from gym.core import Wrapper


class Monitor(Wrapper):

    def __init__(self, env, prefix=None, allow_early_resets=False):
        """ Monitor Wrapper

        This wrapper uses ml-logger to cache environment metrics.

        :param env: gym environment
        :param prefix: cache prefix, used to direct the stored metrics
            to a specific cache namescope.
        :param allow_early_resets: default False. raise exception
            if manual reset is detected.
        """
        Wrapper.__init__(self, env=env)
        from ml_logger import logger

        self.prefix = prefix  # used as cache key for the summary cache
        self.logger = logger
        self.allow_early_resets = allow_early_resets
        self.now = self.t0 = time.time()
        self.rewards = []

        self.total_steps = 0
        self.additional_key_values = {}  # extra info that gets injected into each log entry
        # Useful for metalearning where we're modifying the environment externally
        # But want our logs to know about these modifications

    def __getstate__(self):
        return self.__dict__.copy()

    def __setstate__(self, d):
        self.__dict__ = d

    def reset(self):
        if not self.allow_early_resets and self.rewards:
            raise RuntimeError("Tried to reset an environment before done. If "
                               "you want to allow early resets, wrap your env "
                               "with Monitor(env, path, allow_early_resets=True)")
        return self.env.reset()

    def step(self, action):
        ob, rew, done, info = self.env.step(action)
        self.rewards.append(rew)
        if done:
            self.rewards = []
            ep_rew = sum(self.rewards)
            ep_len = len(self.rewards)
            now = time.time()
            dt, self.now = now - self.now, now
            ep_info = {"r": ep_rew, "l": ep_len, "t": round(self.now - self.t0, 6)}
            ep_info.update(self.additional_key_values)
            ep_info["total_steps"] = self.total_steps

            self.logger.store(ep_rew=ep_rew, ep_len=ep_len, dt=round(dt, 6), cache=self.prefix)

            info['episode'] = ep_info

        self.total_steps += 1
        return ob, rew, done, info

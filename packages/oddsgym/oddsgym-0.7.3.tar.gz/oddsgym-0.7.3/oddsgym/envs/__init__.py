import gym

from .base import BaseOddsEnv
from .base_percentage import BasePercentageOddsEnv
from .daily_bets import DailyOddsEnv, DailyPercentageOddsEnv
from .soccer import ThreeWaySoccerOddsEnv, ThreeWaySoccerPercentageOddsEnv
from .soccer import ThreeWaySoccerDailyOddsEnv, ThreeWaySoccerDailyPercentageOddsEnv
from .footballdata import FootballDataDailyEnv, FootballDataDailyPercentageEnv

__all__ = ['BaseOddsEnv', 'BasePercentageOddsEnv', 'DailyOddsEnv', 'DailyPercentageOddsEnv', 'ThreeWaySoccerOddsEnv',
           'ThreeWaySoccerPercentageOddsEnv', 'ThreeWaySoccerDailyOddsEnv', 'ThreeWaySoccerDailyPercentageOddsEnv',
           'FootballDataDailyEnv', 'FootballDataDailyPercentageEnv']

# register the football-data.co.uk environments, so they would be ready for usage when installing with pip
gym.register(id='FootballDataDaily-v0',
             entry_point='oddsgym.envs:FootballDataDailyEnv',
             max_episode_steps=365)
gym.register(id='FootballDataDailyPercent-v0',
             entry_point='oddsgym.envs:FootballDataDailyPercentageEnv',
             max_episode_steps=365)

# register the football-data.co.uk environments in ray, only if ray is installed
try:
    from ray.tune.registry import register_env
except ImportError:  # pragma: no cover
    pass
else:
    register_env('FootballDataDaily-ray-v0', lambda env_config: FootballDataDailyEnv(**env_config))
    register_env('FootballDataDailyPercent-ray-v0', lambda env_config: FootballDataDailyPercentageEnv(**env_config))

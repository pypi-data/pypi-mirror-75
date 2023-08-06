import torch
import torch.nn as nn
import copy
import math

from torch.optim import Adam
from d3rlpy.models.torch.policies import create_normal_policy
from d3rlpy.models.torch.q_functions import create_continuous_q_function
from d3rlpy.algos.sac import ISACImpl
from .utility import torch_api, train_api
from .ddpg_impl import DDPGImpl


class SACImpl(DDPGImpl, ISACImpl):
    def __init__(self, observation_shape, action_size, actor_learning_rate,
                 critic_learning_rate, temp_learning_rate, gamma, tau,
                 n_critics, bootstrap, initial_temperature, eps,
                 use_batch_norm, q_func_type, use_gpu, scaler):
        self.temp_learning_rate = temp_learning_rate
        self.initial_temperature = initial_temperature

        super().__init__(observation_shape, action_size, actor_learning_rate,
                         critic_learning_rate, gamma, tau, n_critics,
                         bootstrap, 0.0, eps, use_batch_norm, q_func_type,
                         use_gpu, scaler)

        # TODO: save and load temperature parameter
        # setup temeprature after device property is set.
        self._build_temperature()
        self._build_temperature_optim()

    def _build_actor(self):
        self.policy = create_normal_policy(self.observation_shape,
                                           self.action_size,
                                           self.use_batch_norm)

    def _build_temperature(self):
        initial_val = math.log(self.initial_temperature)
        data = torch.full((1, 1), initial_val, device=self.device)
        self.log_temp = nn.Parameter(data)

    def _build_temperature_optim(self):
        self.temp_optim = Adam([self.log_temp], self.temp_learning_rate)

    @train_api
    @torch_api
    def update_actor(self, obs_t):
        if self.scaler:
            obs_t = self.scaler.transform(obs_t)

        action, log_prob = self.policy(obs_t, with_log_prob=True)
        entropy = self.log_temp.exp() * log_prob
        q_t = self.q_func(obs_t, action, 'min')
        loss = (entropy - q_t).mean()

        self.actor_optim.zero_grad()
        loss.backward()
        self.actor_optim.step()

        return loss.cpu().detach().numpy()

    @train_api
    @torch_api
    def update_temp(self, obs_t):
        if self.scaler:
            obs_t = self.scaler.transform(obs_t)

        with torch.no_grad():
            _, log_prob = self.policy.sample(obs_t, with_log_prob=True)
            targ_temp = log_prob - self.action_size

        loss = -(self.log_temp.exp() * targ_temp).mean()

        self.temp_optim.zero_grad()
        loss.backward()
        self.temp_optim.step()

        # current temperature value
        cur_temp = self.log_temp.exp().cpu().detach().numpy()[0][0]

        return loss.cpu().detach().numpy(), cur_temp

    @train_api
    @torch_api
    def sample_action(self, x):
        if self.scaler:
            x = self.scaler.transform(x)

        with torch.no_grad():
            return self.policy.sample(x).cpu().detach().numpy()

    def compute_target(self, x):
        with torch.no_grad():
            action, log_prob = self.policy.sample(x, with_log_prob=True)
            entropy = self.log_temp.exp() * log_prob
            return self.targ_q_func.compute_target(x, action) - entropy

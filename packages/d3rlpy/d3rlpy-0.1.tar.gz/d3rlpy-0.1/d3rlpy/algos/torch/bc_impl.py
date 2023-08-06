import torch
import copy

from torch.optim import Adam
from d3rlpy.models.torch.imitators import create_deterministic_regressor
from d3rlpy.models.torch.imitators import create_discrete_imitator
from d3rlpy.algos.bc import IBCImpl
from .base import TorchImplBase
from .utility import torch_api, train_api


class BCImpl(TorchImplBase, IBCImpl):
    def __init__(self, observation_shape, action_size, learning_rate, eps,
                 use_batch_norm, use_gpu, scaler):
        self.observation_shape = observation_shape
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.eps = eps
        self.use_batch_norm = use_batch_norm
        self.scaler = scaler

        self._build_network()

        if use_gpu:
            self.to_gpu(use_gpu)
        else:
            self.to_cpu()

        self._build_optim()

    def _build_network(self):
        self.imitator = create_deterministic_regressor(self.observation_shape,
                                                       self.action_size)

    def _build_optim(self):
        self.optim = Adam(self.imitator.parameters(),
                          lr=self.learning_rate,
                          eps=self.eps)

    @train_api
    @torch_api
    def update_imitator(self, obs_t, act_t):
        if self.scaler:
            obs_t = self.scaler.transform(obs_t)

        loss = self.imitator.compute_error(obs_t, act_t)

        self.optim.zero_grad()
        loss.backward()
        self.optim.step()

        return loss.cpu().detach().numpy()

    def _predict_best_action(self, x):
        return self.imitator(x)

    def predict_value(self, x, action, with_std):
        raise NotImplementedError('BC does not support value estimation')

    def sample_action(self, x):
        raise NotImplementedError('BC does not support sampling action')


class DiscreteBCImpl(BCImpl):
    def __init__(self, observation_shape, action_size, learning_rate, eps,
                 beta, use_batch_norm, use_gpu, scaler):
        self.beta = beta
        super().__init__(observation_shape, action_size, learning_rate, eps,
                         use_batch_norm, use_gpu, scaler)

    def _build_network(self):
        self.imitator = create_discrete_imitator(self.observation_shape,
                                                 self.action_size, self.beta)

    def _predict_best_action(self, x):
        return self.imitator(x).argmax(dim=1)

    @train_api
    @torch_api
    def update_imitator(self, obs_t, act_t):
        if self.scaler:
            obs_t = self.scaler.transform(obs_t)

        loss = self.imitator.compute_error(obs_t, act_t.long())

        self.optim.zero_grad()
        loss.backward()
        self.optim.step()

        return loss.cpu().detach().numpy()

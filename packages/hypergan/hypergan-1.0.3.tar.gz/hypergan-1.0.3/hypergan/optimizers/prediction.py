# From https://raw.githubusercontent.com/sanghoon/prediction_gan/master/prediction.py
import torch
import torch.nn as nn
import torch.optim as optim
import copy
from hypergan.gan_component import ValidationException, GANComponent
from contextlib import contextmanager


class Prediction(optim.Optimizer):
    def __init__(self, params, lr=1.0, optimizer=None):
        super(optim.Optimizer, self).__init__()
        if optimizer is None:
            raise ValidationException("optimizer required for PredOpt")

        self._params = list(params)
        self.optimizer = self.create_optimizer(optimizer)
        self.lr = lr

        self._prev_params = copy.deepcopy(self._params)
        self._diff_params = None

        self.step()

    def create_optimizer(self, defn):
        klass = GANComponent.lookup_function(None, defn['class'])
        del defn["class"]
        optimizer = klass(self._params, **defn)
        return optimizer

    def step(self):
        if self._diff_params is None:
            # Preserve parameter memory
            self._diff_params = copy.deepcopy(self._params)

        for i, _new_param in enumerate(self._params):
            # Calculate difference and store new params
            self._diff_params[i].data[:] = _new_param.data[:] - self._prev_params[i].data[:]
            self._prev_params[i].data[:] = _new_param.data[:]

        self.optimizer.step()

        # Roll-back to the original values
        for i, _cur_param in enumerate(self._params):
            _cur_param.data[:] = self._prev_params[i].data[:]

    def zero_grad(self):
        self.optimizer.zero_grad()

        for i, _cur_param in enumerate(self._params):
            # Integrity check (whether we have the latest copy of parameters)
            if torch.sum(_cur_param.data[:] != self._prev_params[i].data[:]) > 0:
                raise RuntimeWarning("Stored parameters differ from the current ones. Call step() after parameter updates")

            _cur_param.data[:] += self.lr * self._diff_params[i].data[:]


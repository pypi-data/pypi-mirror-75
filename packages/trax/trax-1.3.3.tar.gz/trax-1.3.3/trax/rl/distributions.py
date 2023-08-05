# coding=utf-8
# Copyright 2020 The Trax Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""Probability distributions for RL training in Trax."""

import gin
import gym
import numpy as np

from trax import layers as tl
from trax.fastmath import numpy as jnp


class Distribution:
  """Abstract class for parametrized probability distributions."""

  @property
  def n_inputs(self):
    """Returns the number of inputs to the distribution (i.e. parameters)."""
    raise NotImplementedError

  def sample(self, inputs, temperature=1.0):
    """Samples a point from the distribution.

    Args:
      inputs (jnp.ndarray): Distribution inputs. Shape is subclass-specific.
        Broadcasts along the first dimensions. For example, in the categorical
        distribution parameter shape is (C,), where C is the number of
        categories. If (B, C) is passed, the object will represent a batch of B
        categorical distributions with different parameters.
      temperature: sampling temperature; 1.0 is default, at 0.0 chooses
        the most probable (preferred) action.

    Returns:
      Sampled point of shape dependent on the subclass and on the shape of
      inputs.
    """
    raise NotImplementedError

  def log_prob(self, inputs, point):
    """Retrieves log probability (or log probability density) of a point.

    Args:
      inputs (jnp.ndarray): Distribution parameters.
      point (jnp.ndarray): Point from the distribution. Shape should be
        consistent with inputs.

    Returns:
      Array of log probabilities of points in the distribution.
    """
    raise NotImplementedError

  def LogProb(self):  # pylint: disable=invalid-name
    """Builds a log probability layer for this distribution."""
    return tl.Fn('LogProb',
                 lambda inputs, point: self.log_prob(inputs, point))  # pylint: disable=unnecessary-lambda


@gin.configurable(blacklist=['n_categories', 'shape'])
class Categorical(Distribution):
  """Categorical distribution parametrized by logits."""

  def __init__(self, n_categories, shape=()):
    """Initializes Categorical distribution.

    Args:
      n_categories (int): Number of categories.
      shape (tuple): Shape of the sample.
    """
    self._n_categories = n_categories
    self._shape = shape

  @property
  def n_inputs(self):
    return np.prod(self._shape, dtype=jnp.int32) * self._n_categories

  def _unflatten_inputs(self, inputs):
    return jnp.reshape(
        inputs, inputs.shape[:-1] + self._shape + (self._n_categories,)
    )

  def sample(self, inputs, temperature=1.0):
    # No need for LogSoftmax with sampling - softmax normalization is
    # subtracting a constant from every logit, and sampling is taking
    # a max over logits plus noise, so invariant to adding a constant.
    if temperature == 0.0:
      return jnp.argmax(self._unflatten_inputs(inputs), axis=-1)
    return tl.logsoftmax_sample(self._unflatten_inputs(inputs), temperature)

  def log_prob(self, inputs, point):
    inputs = tl.LogSoftmax()(self._unflatten_inputs(inputs))
    return jnp.sum(
        # Select the logits specified by point.
        inputs * tl.one_hot(point, self._n_categories),
        # Sum over the parameter dimensions.
        axis=[-a for a in range(1, len(self._shape) + 2)],
    )

  def entropy(self, log_probs):
    probs = jnp.exp(log_probs)
    return -jnp.sum(probs * log_probs, axis=-1)


@gin.configurable(blacklist=['shape'])
class Gaussian(Distribution):
  """Independent multivariate Gaussian distribution parametrized by mean."""

  def __init__(self, shape=(), std=1.0):
    """Initializes Gaussian distribution.

    Args:
      shape (tuple): Shape of the sample.
      std (float): Standard deviation, shared across the whole sample.
    """
    self._shape = shape
    self._std = std

  @property
  def n_inputs(self):
    return np.prod(self._shape, dtype=jnp.int32)

  def sample(self, inputs, temperature=1.0):
    if temperature == 0:
      # this seemingly strange if solves the problem
      # of calling np/jnp.random in the metric PreferredMove
      return inputs
    else:
      return np.random.normal(
          loc=jnp.reshape(inputs, inputs.shape[:-1] + self._shape),
          scale=self._std * temperature,
      )

  def log_prob(self, inputs, point):
    point = point.reshape(inputs.shape[:-1] + (-1,))
    return (
        # L2 term.
        -jnp.sum((point - inputs) ** 2, axis=-1) / (2 * self._std ** 2) -
        # Normalizing constant.
        ((jnp.log(self._std) + jnp.log(jnp.sqrt(2 * jnp.pi)))
         * np.prod(self._shape))
    )

  # At that point self._std is not learnable, hence
  # we return a constant
  def entropy(self, log_probs):
    del log_probs  # would be helpful if self._std was learnable
    return jnp.exp(self._std) + .5 * jnp.log(2.0 * jnp.pi * jnp.e)


# TODO(pkozakowski): Implement GaussianMixture.


def create_distribution(space):
  """Creates a Distribution for the given Gym space."""
  if isinstance(space, gym.spaces.Discrete):
    return Categorical(shape=(), n_categories=space.n)
  elif isinstance(space, gym.spaces.MultiDiscrete):
    assert space.nvec.size
    assert min(space.nvec) == max(space.nvec), (
        'Every dimension must have the same number of categories, got '
        '{}.'.format(space.nvec)
    )
    return Categorical(shape=(len(space.nvec),), n_categories=space.nvec[0])
  elif isinstance(space, gym.spaces.Box):
    return Gaussian(shape=space.shape)
  else:
    raise TypeError('Space {} unavailable as a distribution support.')


def LogLoss(distribution, **unused_kwargs):  # pylint: disable=invalid-name
  """Builds a log loss layer for a Distribution."""
  return tl.Serial(
      distribution.LogProb(),
      tl.Negate(),
      tl.WeightedSum()
  )

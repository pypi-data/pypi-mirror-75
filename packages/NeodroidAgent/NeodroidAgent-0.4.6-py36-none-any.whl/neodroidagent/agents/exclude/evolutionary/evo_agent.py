#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC
from itertools import count
from typing import Any

from tqdm import tqdm

from neodroidagent.agents.agent import Agent

__author__ = "Christian Heider Nielsen"

from warg import drop_unused_kws


class EVOAgent(Agent, ABC):
  """
Base class for evolution strategy (ES) based agents
"""

  # region Public

  def sample(self, state, **kwargs):
    pass

  def evaluate(self, batch, **kwargs):
    pass

  @drop_unused_kws
  def rollout(self, initial_state, environment, *, train=True, render=False) -> Any:
    if train:
      self.update_i += 1

    episode_signal = 0
    episode_length = 0

    state = initial_state

    T = count(1)
    T = tqdm(T, f"Rollout #{self.update_i}", leave=False, disable=not render)

    for t in T:
      action = int(self.sample(state)[0])

      (state, signal, terminated, info) = environment.act(action=action)
      episode_signal += signal

      if render:
        environment.render()

      if terminated:
        episode_length = t
        break

    if train:
      self.update()

    return episode_signal, episode_length

  # endregion

  # region Protected

  def _optimise(self, error, **kwargs):
    pass

  # endregion

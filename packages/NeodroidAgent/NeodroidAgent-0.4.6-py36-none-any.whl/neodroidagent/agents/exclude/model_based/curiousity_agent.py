#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any, Dict, Sequence, Tuple

from neodroidagent.architectures import Architecture

from draugr.writers import MockWriter, Writer
from neodroid.utilities import (
  ActionSpace,
  EnvironmentSnapshot,
  ObservationSpace,
  SignalSpace,
  )
from neodroidagent.agents.torch_agents.torch_agent import TorchAgent

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 9/6/19
           """


class CuriousityAgent(TorchAgent):
  def __build__(
    self,
    observation_space: ObservationSpace,
    action_space: ActionSpace,
    signal_space: SignalSpace,
    **kwargs
    ) -> None:
    pass

  def _sample(
    self,
    state: EnvironmentSnapshot,
    *args,
    deterministic: bool = False,
    metric_writer: Writer = MockWriter(),
    **kwargs
    ) -> Tuple[Sequence, Any]:
    pass

  def _update(self, *args, metric_writer: Writer = MockWriter(), **kwargs) -> None:
    pass

  @property
  def models(self) -> Dict[str, Architecture]:
    pass

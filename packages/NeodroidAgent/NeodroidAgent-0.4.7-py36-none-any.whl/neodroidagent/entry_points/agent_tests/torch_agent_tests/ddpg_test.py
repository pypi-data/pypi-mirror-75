#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Union

from neodroidagent.agents import DeepDeterministicPolicyGradientAgent
from neodroidagent.common import ParallelSession
from neodroidagent.entry_points.session_factory import session_factory
from neodroidagent.configs.test_reference.base_continous_test_config import *

__author__ = "Christian Heider Nielsen"

"""
Description: Config for training
Author: Christian Heider Nielsen
"""

# General

CONFIG_NAME = __name__
import pathlib

CONFIG_FILE_PATH = pathlib.Path(__file__)

CONNECT_TO_RUNNING = False

# RENDER_FREQUENCY = 1
BATCH_SIZE = 256

ddpg_config = globals()


def ddpg_run(
  skip_confirmation: bool = True,
  environment_type: Union[bool, str] = True,
  config=ddpg_config
  ):
  session_factory(
    DeepDeterministicPolicyGradientAgent,
    config,
    session=ParallelSession,
    skip_confirmation=skip_confirmation,
    environment=environment_type,
    )


def ddpg_test(config=ddpg_config):
  ddpg_run(environment_type="gym", config=config)


if __name__ == "__main__":
  ddpg_test()

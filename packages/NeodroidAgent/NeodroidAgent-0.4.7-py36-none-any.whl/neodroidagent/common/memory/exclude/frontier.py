#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Christian Heider Nielsen'


class Frontier(object):
  '''For storing transitions explored in the environment.'''

  def __init__(self):
    self.memory = []

  def add(self, value):
    '''Saves a transition.'''
    self.memory.append(value)

  def sample(self, num):
    '''Randomly sample transitions from memory.'''
    batch = []
    while len(self.memory) > 0 and len(batch) < num:
      batch.append(self.memory.pop())
    return batch

  def __len__(self):
    '''Return the length of the memory list.'''
    return len(self.memory)


if __name__ == '__main__':

  def test_frontier_buffer():
    rb = Frontier()
    a = tuple(range(3))
    rb.add(a)
    b = rb.sample(1)
    assert [a] == b, f'Expected {a} and {b} to be equal'

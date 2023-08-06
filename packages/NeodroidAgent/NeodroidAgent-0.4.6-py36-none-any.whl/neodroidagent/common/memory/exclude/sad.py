#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Christian Heider Nielsen'
__doc__ = r'''

           Created on 24/02/2020
           '''

import math
import random

import numpy


class SumTree:
  '''
  a binary tree data structure where the parent’s value is the sum of its children
  '''
  write = 0

  def __init__(self, capacity):
    self.capacity = capacity
    self.tree = numpy.zeros(2 * capacity - 1)
    self.data = numpy.zeros(capacity, dtype=object)
    self.n_entries = 0

  def _propagate(self, idx, change):
    '''
    update to the root node

    @param idx:
    @param change:
    @return:
    '''
    # parent = (idx - 1) // 2
    parent = math.ceil((idx - 1) / 2)

    self.tree[parent] += change

    if parent != 0:
      self._propagate(parent, change)

  def _retrieve(self, idx, s):
    '''
    find sample on leaf node
    @param idx:
    @param s:
    @return:
    '''
    left = 2 * idx + 1
    right = left + 1

    if left >= len(self.tree):
      return idx

    if s <= self.tree[left]:
      return self._retrieve(left, s)
    else:
      return self._retrieve(right, s - self.tree[left])

  def total(self):
    return self.tree[0]

  def add(self, p, data):
    '''
    store priority and sample
    @param p:
    @param data:
    @return:
    '''
    idx = self.write + self.capacity - 1

    self.data[self.write] = data
    self.update(idx, p)

    self.write += 1
    if self.write >= self.capacity:
      self.write = 0

    if self.n_entries < self.capacity:
      self.n_entries += 1

  def update(self, idx, p):
    '''
    update priority
    @param idx:
    @param p:
    @return:
    '''
    change = p - self.tree[idx]

    self.tree[idx] = p
    self._propagate(idx, change)

  def get(self, s):
    '''
    get priority and sample
    @param s:
    @return:
    '''
    idx = self._retrieve(0, s)
    dataIdx = idx - self.capacity + 1

    return (idx, self.tree[idx], self.data[dataIdx])


class PMemory:
  e = 0.01
  a = 0.6

  def __init__(self, capacity):
    self.tree = SumTree(capacity)

  def _getPriority(self, error):
    return (error + self.e) ** self.a

  def add(self, error, sample):
    p = self._getPriority(error)
    self.tree.add(p, sample)

  def sample(self, n):
    batch = []
    segment = self.tree.total() / n

    for i in range(n):
      a = segment * i
      b = segment * (i + 1)

      s = random.uniform(a, b)
      (idx, p, data) = self.tree.get(s)
      batch.append((idx, data))

    return batch

  def update(self, idx, error):
    p = self._getPriority(error)
    self.tree.update(idx, p)


'''

    def _getTargets(self, batch):
        no_state = numpy.zeros(self.stateCnt)

        states = numpy.array([ o[1][0] for o in batch ])
        states_ = numpy.array([ (no_state if o[1][3] is None else o[1][3]) for o in batch ])

        p = agent.brain.predict(states)

        p_ = agent.brain.predict(states_, target=False)
        pTarget_ = agent.brain.predict(states_, target=True)

        x = numpy.zeros((len(batch), IMAGE_STACK, IMAGE_WIDTH, IMAGE_HEIGHT))
        y = numpy.zeros((len(batch), self.actionCnt))
        errors = numpy.zeros(len(batch))

        for i in range(len(batch)):
            o = batch[i][1]
            s = o[0]; a = o[1]; r = o[2]; s_ = o[3]

            t = p[i]
            oldVal = t[a]
            if s_ is None:
                t[a] = r
            else:
                t[a] = r + GAMMA * pTarget_[i][ numpy.argmax(p_[i]) ]  # double DQN

            x[i] = s
            y[i] = t
            errors[i] = abs(oldVal - t[a])

        return (x, y, errors)

    def replay(self):
        batch = self.memory.sample(BATCH_SIZE)
        x, y, errors = self._getTargets(batch)

        #update errors
        for i in range(len(batch)):
            idx = batch[i][0]
            self.memory.update(idx, errors[i])

        self.brain.train(x, y)
'''


class Memory:
  '''
  # stored as ( s, a, r, s_ ) in SumTree

  The main idea is that we prefer transitions that does not fit well to our current estimate of the Q
  function, because these are the transitions that we can learn most from. This reflects a simple intuition
  from our real world - if we encounter a situation that really differs from our expectation,
  we think about it over and over and change our model until it fits.

  '''
  e = 0.01
  a = 0.6
  beta = 0.4
  beta_increment_per_sampling = 0.001

  def __init__(self, capacity):
    self.tree = SumTree(capacity)
    self.capacity = capacity

  def _get_priority(self, error):
    return (numpy.abs(error) + self.e) ** self.a

  def add(self, error, sample):
    p = self._get_priority(error)
    self.tree.add(p, sample)

  def sample(self, n):
    batch = []
    idxs = []
    segment = self.tree.total() / n
    priorities = []

    self.beta = numpy.min([1., self.beta + self.beta_increment_per_sampling])

    for i in range(n):
      a = segment * i
      b = segment * (i + 1)

      s = random.uniform(a, b)
      (idx, p, data) = self.tree.get(s)
      priorities.append(p)
      batch.append(data)
      idxs.append(idx)

    sampling_probabilities = priorities / self.tree.total()
    is_weight = numpy.power(self.tree.n_entries * sampling_probabilities, -self.beta)
    is_weight /= is_weight.max()

    return batch, idxs, is_weight

  def update(self, idx, error):
    p = self._get_priority(error)
    self.tree.update(idx, p)


if __name__ == '__main__':
  '''
  def append_sample(self, state, action, reward, next_state, done):
    new_val = self.model(Variable(torch.FloatTensor(state))).data
    old_val = new_val[0][action]
    target_val = self.target_model(Variable(torch.FloatTensor(next_state))).data

    if done:
      a = reward
    else:
      a = reward + self.discount_factor * torch.max(target_val)

    error = abs(old_val - a)

    self.memory.add(error, (state, action, reward, next_state, done))
  '''


  def stest_experience_buffer():
    capacity = int(1)
    s = SumTree(capacity)
    for i in range(1, capacity + 1):
      s.add(math.cos(i) + 2, math.cos(i))
    print(s.get(0))
    print(s.get(0.5))
    print(s.get(3))


  stest_experience_buffer()

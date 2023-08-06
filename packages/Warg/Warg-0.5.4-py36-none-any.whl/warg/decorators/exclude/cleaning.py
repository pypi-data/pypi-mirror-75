#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Christian Heider Nielsen'
__doc__ = r'''

           Created on 03/03/2020
           '''

from itertools import count


def final_yield(f):
  f_ = f()
  def a():
    try:
      while True:
        yield next(f_)
    except GeneratorExit:
      raise
  return a

if __name__ == '__main__':

  def gen():
    yield 'so far so good'
    try:
      yield 'yay'
    finally:
      yield 'bye'

  @final_yield
  def safe_gen():
    yield 'so far so good'
    try:
      yield 'yay'
    finally:
      yield 'bye'

  c = count()
  g = safe_gen()
  print(next(c),next(g))
  print(next(c),next(g))
  print(next(c),g.throw(ValueError('too bad')))
  print(next(c),next(g))

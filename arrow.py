from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Callable, Tuple

T1 = TypeVar('T1')
T2 = TypeVar('T2')
T3 = TypeVar('T3')
T4 = TypeVar('T4')

class Product(Generic[T1, T2, T3, T4]):
  def __init__(self, f1: Callable[[T1], T3], f2: Callable[[T2], T4]):
    self.f1 = f1
    self.f2 = f2

  def __call__(self, t: Tuple[T1, T2]) -> Tuple[T3, T4]:
    return (self.f1(t[0]), self.f2(t[1]))

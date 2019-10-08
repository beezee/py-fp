from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Callable, List

T1 = TypeVar('T1')
T2 = TypeVar('T2')
T3 = TypeVar('T3')
T4 = TypeVar('T4')

class Functor(ABC, Generic[T1, T2, T3, T4]):
  @abstractmethod
  def fmap(self, c: Callable[[T1], T2]) -> Callable[[T3], T4]: pass

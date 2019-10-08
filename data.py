from adt import F1, F2, Sum2
from functor import Functor
from typing import Callable, List, TypeVar

T1 = TypeVar('T1')
T2 = TypeVar('T2')

Maybe = Sum2[None, T1]

class MaybeF(Functor):
  def fmap(self, c: Callable[[T1], T2]) -> Callable[[Maybe[T1]], Maybe[T2]]:
    def run(m: Maybe[T1]):
      if m.run is not None:
        return F2(c(m.run))
      else:
        return F1(None)
    return run

class ListF(Functor):
  def fmap(self, c: Callable[[T1], T2]) -> Callable[[List[T1]], List[T2]]:
    return lambda l: list(map(c, l))

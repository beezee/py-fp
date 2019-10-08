from typing import Generic, TypeVar, Callable

T1 = TypeVar('T1')
T2 = TypeVar('T2')
T3 = TypeVar('T3')

class Compose(Generic[T1, T2, T3]):
  def __init__(self, f1: Callable[[T1], T2], f2: Callable[[T2], T3]):
    self.f1 = f1
    self.f2 = f2

  def __call__(self, t1: T1) -> T3:
    return self.f2(self.f1(t1))


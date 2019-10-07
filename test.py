from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, TypeVar, Generic, NamedTuple, Union

T1 = TypeVar('T1')
T2 = TypeVar('T2')
T3 = TypeVar('T3')
Out = TypeVar('Out')

@dataclass
class F1(Generic[T1]):
  run: T1
@dataclass
class F2(Generic[T2]):
  run: T2 
@dataclass
class F3(Generic[T3]):
  run: T3 

Foo = NamedTuple('Foo', [])
Bar = NamedTuple('Bar', [])
Baz = NamedTuple('Baz', [('name', str), ('num', int)])
Quux = NamedTuple('Quux', [('num', int)])

class Fold2(ABC, Generic[T1, T2, Out]):
  @abstractmethod
  def f1(self, f: T1) -> Out: pass
  @abstractmethod
  def f2(self, f: T2) -> Out: pass

  def run(self, d: Union[F1[T1], F2[T2]]) -> Out:
    if isinstance(d, F1): 
      return self.f1(d.run)
    elif isinstance(d, F2): 
      return self.f2(d.run)
    else: assert False

class Fold3(ABC, Generic[T1, T2, T3, Out]):
  @abstractmethod
  def f1(self, f: T1) -> Out: pass
  @abstractmethod
  def f2(self, f: T2) -> Out: pass
  @abstractmethod
  def f3(self, f: T3) -> Out: pass

  def run(self, d: Union[F1[T1], F2[T2], F3[T3]]) -> Out:
    if isinstance(d, F1): 
      return self.f1(d.run)
    elif isinstance(d, F2): 
      return self.f2(d.run)
    elif isinstance(d, F3): 
      return self.f3(d.run)
    else: assert False

class FoldPBQ(Fold2[Baz, Quux, str]):
  def f1(self, baz: Baz) -> str:
    return baz.name * baz.num
  def f2(self, quux: Quux) -> str:
    return 'quux' * quux.num

class FoldPrint(Fold3[Foo, Bar, Union[F1[Baz], F2[Quux]], str]):
  def f1(self, foo: Foo) -> str: return 'foo'
  def f2(self, bar: Bar) -> str: return 'bar'
  def f3(self, bq: Union[F1[Baz], F2[Quux]]) -> str:
    return FoldPBQ().run(bq)

class FoldLen(Fold3[Foo, Bar, Baz, int]):
  def f1(self, foo: Foo) -> int: return 1
  def f2(self, bar: Bar) -> int: return 2
  def f3(self, baz: Baz) -> int:
    return len(baz.name) * baz.num

print(FoldPrint().run(F1(Foo())))
#print(FoldPrint().run(R('baz')))
print(FoldPrint().run(F3(F1(Baz('bazzz', 3)))))

print(FoldLen().run(F1(Foo())))
print(FoldLen().run(F3(Baz('bazzz', 3))))

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, TypeVar, Generic, NamedTuple, Union

LT = TypeVar('LT')
MT = TypeVar('MT')
RT = TypeVar('RT')
T = TypeVar('T')

@dataclass
class L(Generic[LT]):
  run: LT
@dataclass
class M(Generic[MT]):
  run: MT
@dataclass
class R(Generic[RT]):
  run: RT

Foo = NamedTuple('Foo', [])
Bar = NamedTuple('Bar', [])
Baz = NamedTuple('Baz', [('name', str), ('num', int)])

class Fold3(ABC, Generic[LT, MT, RT, T]):
  @abstractmethod
  def left(self, l: L) -> T: pass
  @abstractmethod
  def middle(self, m: M) -> T: pass
  @abstractmethod
  def right(self, r: R) -> T: pass

  def run(self, d: Union[L[LT], M[MT], R[RT]]) -> T:
    if isinstance(d, L): 
      return self.left(d)
    elif isinstance(d, M): 
      return self.middle(d)
    elif isinstance(d, R): 
      return self.right(d)
    else: assert False

class FoldPrint(Fold3[Foo, Bar, Baz, str]):
  def left(self, foo: L[Foo]) -> str: return 'foo'
  def middle(self, bar: M[Bar]) -> str: return 'bar'
  def right(self, baz: R[Baz]) -> str:
    return baz.run.name * baz.run.num

class FoldLen(Fold3[Foo, Bar, Baz, int]):
  def left(self, foo: L[Foo]) -> int: return 1
  def middle(self, bar: M[Bar]) -> int: return 2
  def right(self, baz: R[Baz]) -> int:
    return len(baz.run.name) * baz.run.num

print(FoldPrint().run(L(Foo())))
#print(FoldPrint().run(R('baz')))
print(FoldPrint().run(R(Baz('bazzz', 3))))

print(FoldLen().run(L(Foo())))
print(FoldLen().run(R(Baz('bazzz', 3))))

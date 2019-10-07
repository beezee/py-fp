from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, TypeVar, Generic, NamedTuple, Union

T1 = TypeVar('T1')
T2 = TypeVar('T2')
T3 = TypeVar('T3')
T4 = TypeVar('T4')
T5 = TypeVar('T5')
T6 = TypeVar('T6')
T7 = TypeVar('T7')
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
@dataclass
class F4(Generic[T4]):
  run: T4 
@dataclass
class F5(Generic[T5]):
  run: T5 
@dataclass
class F6(Generic[T6]):
  run: T6 
@dataclass
class F7(Generic[T7]):
  run: T7 

Foo = NamedTuple('Foo', [])
Bar = NamedTuple('Bar', [])
Baz = NamedTuple('Baz', [('name', str), ('num', int)])
Quux = NamedTuple('Quux', [('num', int)])

Sum2 = Union[F1[T1], F2[T2]]
Sum3 = Union[F1[T1], F2[T2], F3[T3]]
Sum4 = Union[F1[T1], F2[T2], F3[T3], F4[T4]]
Sum5 = Union[F1[T1], F2[T2], F3[T3], F4[T4], F5[T5]]
Sum6 = Union[F1[T1], F2[T2], F3[T3], F4[T4], F5[T5], F6[T6]]
Sum7 = Union[F1[T1], F2[T2], F3[T3], F4[T4], F5[T5], F6[T6], F7[T7]]

class Fold2(ABC, Generic[T1, T2, Out]):
  @abstractmethod
  def f1(self, f: T1) -> Out: pass
  @abstractmethod
  def f2(self, f: T2) -> Out: pass

  def run(self, d: Sum2[T1, T2]) -> Out:
    if isinstance(d, F1): 
      return self.f1(d.run)
    elif isinstance(d, F2): 
      return self.f2(d.run)
    else: assert False

class Fold3(Fold2[T1, T2, Out], Generic[T1, T2, T3, Out]):
  @abstractmethod
  def f3(self, f: T3) -> Out: pass

  def run(self, d: Sum3[T1, T2, T3]) -> Out:
    if isinstance(d, F3): 
      return self.f3(d.run)
    else: 
      return super().run(d)

class Fold4(Fold3[T1, T2, T3, Out], Generic[T1, T2, T3, T4, Out]):
  @abstractmethod
  def f4(self, f: T4) -> Out: pass

  def run(self, d: Sum4[T1, T2, T3, T4]) -> Out:
    if isinstance(d, F4): 
      return self.f4(d.run)
    else: 
      return super().run(d)

class Fold5(Fold4[T1, T2, T3, T4, Out], Generic[T1, T2, T3, T4, T5, Out]):
  @abstractmethod
  def f5(self, f: T5) -> Out: pass

  def run(self, d: Sum5[T1, T2, T3, T4, T5]) -> Out:
    if isinstance(d, F5): 
      return self.f5(d.run)
    else: 
      return super().run(d)

class Fold6(Fold5[T1, T2, T3, T4, T5, Out], 
            Generic[T1, T2, T3, T4, T5, T6, Out]):
  @abstractmethod
  def f6(self, f: T6) -> Out: pass

  def run(self, d: Sum6[T1, T2, T3, T4, T5, T6]) -> Out:
    if isinstance(d, F6): 
      return self.f6(d.run)
    else: 
      return super().run(d)

class Fold7(Fold6[T1, T2, T3, T4, T5, T6, Out], 
            Generic[T1, T2, T3, T4, T5, T6, T7, Out]):
  @abstractmethod
  def f7(self, f: T7) -> Out: pass

  def run(self, d: Sum7[T1, T2, T3, T4, T5, T6, T7]) -> Out:
    if isinstance(d, F7): 
      return self.f7(d.run)
    else: 
      return super().run(d)

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

class FoldP4(Fold4[Foo, Bar, Baz, Quux, Sum2[Baz, Quux]]):
  def f1(self, foo: Foo) -> F1[Baz]: return F1(Baz("foo", 1))
  def f2(self, bar: Bar) -> F2[Quux]: return F2(Quux(2))
  def f3(self, baz: Baz) -> F1[Baz]: return F1(baz)
  def f4(self, quux: Quux) -> F1[Baz]: return F1(Baz("quux", quux.num))

# there are too many of these to define. where to put? how to discover?
class F12to34(Fold2[T1, T2, Sum4[T3, T4, T1, T2]], Generic[T1, T2, T3, T4]):
  def f1(self, t1: T1) -> F3[T1]: return F3(t1)
  def f2(self, t2: T2) -> F4[T2]: return F4(t2)

class FoldLen(Fold3[Foo, Bar, Baz, int]):
  def f1(self, foo: Foo) -> int: return 1
  def f2(self, bar: Bar) -> int: return 2
  def f3(self, baz: Baz) -> int:
    return len(baz.name) * baz.num

print(FoldPrint().run(F1(Foo())))
#print(FoldPrint().run(F3('baz')))
print(FoldPrint().run(F3(F1(Baz('bazzz', 3)))))

print(FoldP4().run(F1(Foo())))
print(FoldP4().run(F12to34[Baz, Quux, Foo, Bar]().run(FoldP4().run(F2(Bar())))))
print(FoldP4().run(F4(Quux(7))))

print(FoldLen().run(F1(Foo())))
print(FoldLen().run(F3(Baz('bazzz', 3))))

import adt
from adt import F1, F2, F3, F4
from arrow import Product
from category import Compose, Id
from data import ListF, MaybeF
from typing import Generic, NamedTuple, TypeVar

T1 = TypeVar('T1')
T2 = TypeVar('T2')
T3 = TypeVar('T3')
T4 = TypeVar('T4')

Foo = NamedTuple('Foo', [])
Bar = NamedTuple('Bar', [])
Baz = NamedTuple('Baz', [('name', str), ('num', int)])
Quux = NamedTuple('Quux', [('num', int)])

FBBQ = adt.Sum4[Foo, Bar, Baz, Quux]
BQ = adt.Sum2[Baz, Quux]

class FoldPBQ(adt.Fold2[Baz, Quux, str]):
  def f1(self, baz: Baz) -> str:
    return baz.name * baz.num
  def f2(self, quux: Quux) -> str:
    return 'quux' * quux.num

class FoldPrint(adt.Fold3[Foo, Bar, BQ, str]):
  def f1(self, foo: Foo) -> str: return 'foo'
  def f2(self, bar: Bar) -> str: return 'bar'
  def f3(self, bq: BQ) -> str:
    return FoldPBQ()(bq)

class FoldP4(adt.Fold4[Foo, Bar, Baz, Quux, adt.Sum2[Baz, Quux]]):
  def f1(self, foo: Foo) -> F1[Baz]: return F1(Baz("foo", 1))
  def f2(self, bar: Bar) -> F2[Quux]: return F2(Quux(2))
  def f3(self, baz: Baz) -> F1[Baz]: return F1(baz)
  def f4(self, quux: Quux) -> F1[Baz]: return F1(Baz("quux", quux.num))


# there are too many of these to define. where to put? how to discover?
class F12to34(adt.Fold2[T1, T2, adt.Sum4[T3, T4, T1, T2]], Generic[T1, T2, T3, T4]):
  def f1(self, t1: T1) -> F3[T1]: return F3(t1)
  def f2(self, t2: T2) -> F4[T2]: return F4(t2)

class FoldLen(adt.Fold4[Foo, Bar, Baz, Quux, int]):
  def f1(self, foo: Foo) -> int: return 1
  def f2(self, bar: Bar) -> int: return 2
  def f3(self, baz: Baz) -> int:
    return len(baz.name) * baz.num
  def f4(self, quux: Quux) -> int:
    return quux.num

print(FoldPrint()(F1(Foo())))
#print(FoldPrint()(F3('baz')))
print(FoldPrint()(F3(F1(Baz('bazzz', 3)))))

print(FoldP4()(F1(Foo())))
print(ListF().fmap(Compose(
  Compose(F12to34[Baz, Quux, Foo, Bar](), FoldP4()),
    Id[adt.Sum4[Foo, Bar, Baz, Quux]]()))(
      [F2(Bar()), F3(Baz("hi", 3))]))
print(MaybeF().fmap(Compose(
  Compose(FoldP4(), Id[adt.Sum4[Foo, Bar, Baz, Quux]]()),
    F12to34[Baz, Quux, Foo, Bar]()))(F1(None)))
"""print(ListF().fmap(Compose(
  Compose(FoldP4(), Id[Sum4[Foo, Bar, Baz, Quux]]()),
    F12to34[Baz, Quux, Foo, Bar]()))(
      [F1(Baz('a', 2)), F1(Bar()), F2(Quux(3))]))"""
print(ListF().fmap(Compose(
  Compose(FoldP4(), Id[adt.Sum4[Foo, Bar, Baz, Quux]]()),
    F12to34[Baz, Quux, Foo, Bar]()))(
      [F1(Baz('a', 2)), F2(Quux(3))]))
print(Compose(
  FoldLen(),
  Compose(F12to34[Baz, Quux, Foo, Bar](),
         FoldP4()))(F2(Bar())))
print(FoldP4()(F4(Quux(7))))

print(FoldLen()(F1(Foo())))
print(FoldLen()(F3(Baz('bazzz', 3))))
print(Product(len, Compose(lambda x: x + 1, len))(('foo', 'bar')))

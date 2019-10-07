from abc import ABC, abstractmethod
from typing import Callable, TypeVar, Generic, NamedTuple, Union

T = TypeVar('T')

Foo = NamedTuple('Foo', [])
Bar = NamedTuple('Bar', [])
Baz = NamedTuple('Baz', [('name', str), ('num', int)])

class FoldAdt(ABC, Generic[T]):
  @abstractmethod
  def foo(self) -> T: pass
  @abstractmethod
  def bar(self) -> T: pass
  @abstractmethod
  def baz(self, name: str, num: int) -> T: pass

def test(d: Union[Foo, Bar, Baz], t: FoldAdt[T]) -> T:
  if isinstance(d, Foo): return t.foo()
  elif isinstance(d, Bar): return t.bar()
  elif isinstance(d, Baz): return t.baz(d.name, d.num)
  else: assert False

class FoldPrint(FoldAdt):
  def foo(self) -> str: return 'foo'
  def bar(self) -> str: return 'bar'
  def baz(self, name: str, num: int) -> str:
    return name * num

class FoldLen(FoldAdt):
  def foo(self) -> int: return 1
  def bar(self) -> int: return 2
  def baz(self, name: str, num: int) -> int:
    return len(name) * num

print(test(Foo(), FoldPrint()))
print(test(Baz('bazzz', 3), FoldPrint()))

print(test(Foo(), FoldLen()))
print(test(Baz('bazzz', 3), FoldLen()))

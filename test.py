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

  def run(self, d: Union[Foo, Bar, Baz]) -> T:
    if isinstance(d, Foo): return self.foo()
    elif isinstance(d, Bar): return self.bar()
    elif isinstance(d, Baz): return self.baz(d.name, d.num)
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

print(FoldPrint().run(Foo()))
print(FoldPrint().run(Baz('bazzz', 3)))

print(FoldLen().run(Foo()))
print(FoldLen().run(Baz('bazzz', 3)))

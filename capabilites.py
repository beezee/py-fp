from typing import Callable, NamedTuple, Tuple 

Read = NamedTuple('Read', [('read', Callable[[str], str])])
Write = NamedTuple('Write', [('write', Callable[[str], None])])

ProdRead = Read(input)
ProdWrite = Write(print)

def prompt(p: str, eff: Tuple[Read]) -> str:
  return eff[0].read(p)

def _print(p: str, eff: Tuple[Write]) -> None:
  return eff[0].write(p)

def greet(eff: Tuple[Read, Write]) -> None:
  name = prompt('Who are you?', (eff[0],))
  return _print('Hi, ' + name, (eff[1],))

def greet_console() -> None:
  greet((ProdRead, ProdWrite))

greet_console()

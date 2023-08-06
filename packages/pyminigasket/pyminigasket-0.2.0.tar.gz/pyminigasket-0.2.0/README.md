![MiniGasket banner](docs/header.png "MiniGasket")

# MiniGasket: A Tiny Flow-Based Programming Library

[![pipeline status](https://gitlab.com/cvpines/pyminigasket/badges/stable/pipeline.svg)](https://gitlab.com/cvpines/pyminigasket/-/commits/stable)
[![coverage report](https://gitlab.com/cvpines/pyminigasket/badges/stable/coverage.svg)](https://gitlab.com/cvpines/pyminigasket/-/commits/stable)
[![PyPI](https://img.shields.io/pypi/v/pyminigasket)](https://pypi.org/project/pyminigasket/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyminigasket)]((https://pypi.org/project/pyminigasket/))
[![PyPI - License](https://img.shields.io/pypi/l/pyminigasket)](https://gitlab.com/cvpines/pyminigasket/-/blob/stable/LICENSE)

MiniGasket is a tiny library for facilitating flow-based programming.

## Installation

Installation is simple using `pip`:

> `$ pip install pyminigasket`

MiniGasket has no external dependencies.

## Examples


Directing data flows:

```python
import minigasket
from minigasket import SourceBase


class StringSource(minigasket.SourceBase):
    def emit(self, value: str):
        self.send(value)


class ToUpper(minigasket.SourceSinkBase):
    def __init__(self):
        super().__init__()

    def receive(self, sender: SourceBase, message: str) -> None:
        self.send(message.upper())


class Appender(minigasket.SourceSinkBase):
    def __init__(self, value: str):
        super().__init__()
        self._value = value

    def receive(self, sender: SourceBase, message) -> None:
        self.send(message + self._value)


class Collector(minigasket.SinkBase):
    def __init__(self):
        super().__init__()
        self.received = []

    def receive(self, sender: SourceBase, message) -> None:
        self.received.append(message)


source = StringSource()
sink = Collector()

source >> sink
source >> ToUpper() >> sink
source >> Appender('!') >> sink

source.emit('hello')
source.emit('world')
assert sink.received == ['hello', 'HELLO', 'hello!', 'world', 'WORLD', 'world!']
```

Creating a filter:

```python
import random

import minigasket
from minigasket import SourceBase


class RandomNumberSource(minigasket.SourceBase):
    def emit(self):
        self.send(random.randrange(100))


class EvenNumberFilter(minigasket.FilterBase):
    def predicate(self, sender: SourceBase, message: int) -> bool:
        return (message % 2) == 0


class Collector(minigasket.SinkBase):
    def __init__(self):
        super().__init__()
        self.received = []

    def receive(self, sender: SourceBase, message) -> None:
        self.received.append(message)


source = RandomNumberSource()
even_sink = Collector()
odd_sink = Collector()

filt = EvenNumberFilter()
source >> filt >> even_sink
filt.rejected >> odd_sink

for _ in range(10):
    source.emit()

print('EVENS:', even_sink.received)
print('ODDS:', odd_sink.received)
```

Multiple sources:

```python
import minigasket


class IntSource(minigasket.SourceBase):
    def emit(self, value: int):
        self.send(value)


class IncrementDecrement(minigasket.SinkBase):
    def __init__(self):
        super().__init__()
        self.incremented = minigasket.SourceProxy(self)
        self.decremented = minigasket.SourceProxy(self)

    def receive(self, sender, message: int) -> None:
        self.incremented.send(message + 1)
        self.decremented.send(message - 1)


class Collector(minigasket.SinkBase):
    def __init__(self):
        super().__init__()
        self.received = []

    def receive(self, sender, message) -> None:
        self.received.append(message)


source = IntSource()
sink_increment = Collector()
sink_decrement = Collector()

incdec = IncrementDecrement()
source >> incdec
incdec.incremented >> sink_increment
incdec.decremented >> sink_decrement

source.emit(1)
source.emit(2)
source.emit(3)

assert sink_increment.received == [2, 3, 4]
assert sink_decrement.received == [0, 1, 2]
```

Multiple Sinks:

```python
import minigasket


class StringSource(minigasket.SourceBase):
    def emit(self, value: str):
        self.send(value)


class MultiPrint(object):
    def __init__(self):
        super().__init__()
        self.sink_a = minigasket.SinkProxy(self.receive_a)
        self.sink_b = minigasket.SinkProxy(self.receive_b)

    def receive_a(self, sender, message) -> None:
        print('Got message from sink A:', message)

    def receive_b(self, sender, message) -> None:
        print('Got message from sink B:', message)


source_a = StringSource()
source_b = StringSource()

sink = MultiPrint()

source_a >> sink.sink_a
source_b >> sink.sink_b

source_a.emit('Hello to sink A!')
source_b.emit('Hello to sink B!')
```
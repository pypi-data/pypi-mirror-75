from typing import List, Union, Callable, Any
from ._exceptions import PipeCannotSendException, PipeCannotReceiveException

class SourceBase(object):

    def __init__(self):
        self._sinks: List[SinkBase] = []

    def send(self, message) -> None:
        for sink in self._sinks:
            sink.receive(self, message)

    def connect(self, sink: Union['SinkBase', 'Pipe']) -> 'Pipe':
        self._sinks.append(sink)
        return Pipe(self, sink)

    def disconnect(self):
        self._sinks.clear()

    def __rshift__(self, other) -> 'Pipe':
        return self.connect(other)


class SinkBase(object):

    def receive(self, sender: SourceBase, message) -> None:
        raise NotImplementedError


class SourceSinkBase(SinkBase, SourceBase):

    def receive(self, sender: SourceBase, message) -> None:
        raise NotImplementedError


class SourceProxy(SourceBase):

    def __init__(self, parent):
        super().__init__()
        self._parent = parent

    def send(self, message) -> None:
        for sink in self._sinks:
            sink.receive(self._parent, message)


class SinkProxy(SinkBase):

    def __init__(self, callback: Callable[[SourceBase, Any], None]):
        super().__init__()
        self._callback = callback

    def receive(self, sender: SourceBase, message) -> None:
        self._callback(sender, message)


class FilterBase(SourceSinkBase):

    def __init__(self):
        super().__init__()
        self.rejected = SourceProxy(self)

    def predicate(self, sender: SourceBase, message) -> bool:
        raise NotImplementedError

    def receive(self, sender: SourceBase, message) -> None:
        if self.predicate(sender, message):
            self.send(message)
        else:
            self.rejected.send(message)


class Passthrough(SourceSinkBase):

    def receive(self, sender: SourceBase, message) -> None:
        self.send(message)


class Pipe(object):

    def __init__(self, root_source: SourceBase, root_sink: SinkBase):
        super().__init__()
        self._start: Union[SourceBase, SourceSinkBase, Pipe] = root_source
        self._end: Union[SinkBase, SourceSinkBase, Pipe] = root_sink

    def send(self, message) -> None:
        if hasattr(self._end, 'send'):
            self._end.send(message)
        else:
            raise PipeCannotSendException()

    def receive(self, sender: SourceBase, message) -> None:
        if hasattr(self._start, 'receive'):
            self._start.receive(sender, message)
        else:
            raise PipeCannotReceiveException()

    def connect(self,
                sink: Union[SinkBase,
                            'Pipe',
                            List[Union[SinkBase, 'Pipe']]])\
            -> 'Pipe':
        if hasattr(self._end, 'send'):
            self._end.connect(sink)
            return Pipe(self._start, sink)
        else:
            raise PipeCannotSendException()

    def disconnect(self):
        if hasattr(self._end, 'send'):
            self._end.disconnect()
        else:
            raise PipeCannotSendException()

    def __rshift__(self, other) -> 'Pipe':
        return self.connect(other)

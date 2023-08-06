__version__ = '0.2.0'

from ._core import \
    SourceBase, SourceSinkBase, SinkBase, \
    SourceProxy, SinkProxy, \
    FilterBase, \
    Passthrough, \
    Pipe
from ._exceptions import \
    MiniGasketExceptionBase, \
    PipeCannotReceiveException, PipeCannotSendException

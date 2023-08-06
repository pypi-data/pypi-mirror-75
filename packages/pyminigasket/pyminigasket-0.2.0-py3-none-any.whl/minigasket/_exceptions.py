class MiniGasketExceptionBase(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class PipeCannotSendException(MiniGasketExceptionBase):
    """Raised when a pipe's endpoint is not capable of sending messages."""

    def __init__(self):
        super().__init__(
            'The pipe cannot send messages or connect to sinks as '
            'its endpoint does not implement "send".')


class PipeCannotReceiveException(MiniGasketExceptionBase):
    """Raised when a pipe's endpoint is not capable of receiving messages."""

    def __init__(self):
        super().__init__(
            'The pipe cannot receive messages as its starting point '
            'does not implement "receive".')

"""
Defines all ps_ams exceptions
"""


class WowPyException(Exception):
    """
    Base exception class
    """

    def __init__(self, msg=None, cause=None):
        self.msg = msg or self.msg
        self.cause = cause
        super().__init__(self.msg)


class DeleteRecordingException(WowPyException):
    """
    Thrown when a recording resource has been deleted.
    """
    msg = 'The recording resource has been deleted.'


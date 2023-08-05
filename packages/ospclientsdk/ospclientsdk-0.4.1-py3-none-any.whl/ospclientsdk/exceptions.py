"""
    ospclientsdk.exceptions.

    Module containing all custom exceptions used by ospclientsdk.

"""


class OspShellError(Exception):
    """Ospclientsdk's base Exception class"""

    def __init__(self, message):
        """Constructor.

        :param message: error message
        :type message: str
        """
        super(OspShellError, self).__init__(message)
        self.message = message

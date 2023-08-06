from typing import Dict, Any


class Logger:
    """
    Log printing
    """

    # message info prefix
    _prefix = "Currently executing SQL>>>"

    def print_info(self, sql: str, parameters: Any):
        """
        Print info message
        :param sql: Executing SQL statement
        :param parameters: parameters
        """
        pass

    def print_error(self, exception: Any):
        """
        Print error message
        :param exception: exception
        """
        pass


class DefaultLogger(Logger):
    """
    Default log printing
    """
    def print_info(self, msg: str, parameters: Dict):
        """
        Print info message
        :param msg: Executing SQL statement
        :param parameters: parameters
        """
        print(self._prefix, msg, parameters)

    def print_error(self, exception: Any):
        """
        Print error message
        :param exception: exception
        """
        print(self._prefix, exception)

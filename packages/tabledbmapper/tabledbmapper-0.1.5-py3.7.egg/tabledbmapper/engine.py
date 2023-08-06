from abc import abstractmethod
from threading import Lock
from typing import List, Dict, Tuple, Any

from tabledbmapper.logger import DefaultLogger, Logger
from tabledbmapper.sql_builder import builder


# the query method result
QueryResult = List[Dict]
CountResult = int
ExecResult = Tuple[int, int]


class ConnBuilder:

    @abstractmethod
    def connect(self) -> Any:
        """
        Gets the database connection method
        """


class ConnHandle:

    @abstractmethod
    def ping(self, conn: Any):
        """
        Test whether the connection is available, and reconnect
        :param conn: database conn
        """

    @abstractmethod
    def commit(self, conn: Any):
        """
        Commit the connection
        :param conn: database conn
        """

    @abstractmethod
    def rollback(self, conn: Any):
        """
        Rollback the connection
        :param conn: database conn
        """


class ExecuteEngine:
    """
    SQL Execution Engine
    """
    @abstractmethod
    def query(self, conn: Any, logger: Logger, sql: str, parameter: list) -> QueryResult:
        """
        Query list information
        :param conn database conn
        :param logger logger
        :param sql: SQL statement to be executed
        :param parameter: parameter
        :return: Query results
        """

    @abstractmethod
    def count(self, conn: Any, logger: Logger, sql: str, parameter: list) -> CountResult:
        """
        Query quantity information
        :param conn database conn
        :param logger logger
        :param sql: SQL statement to be executed
        :param parameter: parameter
        :return: Query results
        """

    @abstractmethod
    def exec(self, conn: Any, logger: Logger, sql: str, parameter: list) -> ExecResult:
        """
        Execute SQL statement
        :param conn database conn
        :param logger logger
        :param sql: SQL statement to be executed
        :param parameter: parameter
        :return: Last inserted ID, affecting number of rows
        """


class TemplateEngine:
    """
    SQL template execution engine
    Using the jinja2 template engine
    """
    _alive = None

    # lock
    _lock = None

    # conn handle
    _conn_handle = None

    # SQL Execution Engine
    _execute_engine = None
    _auto_commit_function = None

    # Database connection
    _conn = None
    # Logger
    _logger = None

    def __init__(self, conn_handle: ConnHandle, execute_engine: ExecuteEngine, conn: Any, auto_commit=True):
        """
        Init SQL Execution Engine
        :param conn_handle: Database connection processing tool
        :param execute_engine: SQL Execution Engine
        :param conn: database conn
        :param auto_commit: Whether to submit automatically
        """
        self._alive = True
        self._lock = Lock()
        self._conn_handle = conn_handle
        self._execute_engine = execute_engine
        if auto_commit:
            def commit():
                self._conn_handle.commit(self._conn)
            self._auto_commit_function = commit
        else:
            def without_commit():
                pass
            self._auto_commit_function = without_commit
        self._conn = conn
        self._logger = DefaultLogger()

    def set_logger(self, logger: Logger):
        """
        Set Logger
        :param logger: log printing
        :return self
        """
        self._logger = logger
        return self

    def query(self, sql_template: str, parameter: Dict) -> QueryResult:
        """
        Query list information
        :param sql_template: SQL template to be executed
        :param parameter: parameter
        :return: Query results
        """
        # lock
        self._lock.acquire()
        self.survival_checks()
        # test conn
        self._conn_handle.ping(self._conn)
        # render and execute
        sql, param = builder(sql_template, parameter)
        result = self._execute_engine.query(self._conn, self._logger, sql, param)
        # auto commit
        self._auto_commit_function()
        # release
        self._lock.release()
        return result

    def count(self, sql_template: str, parameter: Dict) -> CountResult:
        """
        Query quantity information
        :param sql_template: SQL template to be executed
        :param parameter: parameter
        :return: Query results
        """
        # lock
        self._lock.acquire()
        self.survival_checks()
        # test conn
        self._conn_handle.ping(self._conn)
        # render and execute
        sql, param = builder(sql_template, parameter)
        result = self._execute_engine.count(self._conn, self._logger, sql, param)
        # auto commit
        self._auto_commit_function()
        # release
        self._lock.release()
        return result

    def exec(self, sql_template: str, parameter: Dict) -> ExecResult:
        """
        Execute SQL statement
        :param sql_template: SQL template to be executed
        :param parameter: parameter
        :return: Last inserted ID, affecting number of rows
        """
        # lock
        self._lock.acquire()
        self.survival_checks()
        # test conn
        self._conn_handle.ping(self._conn)
        # render and execute
        sql, param = builder(sql_template, parameter)
        lastrowid, rowcount = self._execute_engine.exec(self._conn, self._logger, sql, param)
        # auto commit
        self._auto_commit_function()
        # release
        self._lock.release()
        return lastrowid, rowcount

    def survival_checks(self):
        """
        Survival checks
        """
        if not self._alive:
            raise Exception("The session has been destroyed")

    def destruction(self):
        """
        Self-destruct to avoid crossing the line
        """
        self._alive = False
        # self._lock = None
        self._conn_handle = None
        self._execute_engine = None
        self._auto_commit_function = None
        self._conn = None
        self._logger = None

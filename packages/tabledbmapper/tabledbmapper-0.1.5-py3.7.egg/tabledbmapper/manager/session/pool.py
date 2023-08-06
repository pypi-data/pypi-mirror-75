from threading import Lock

from tabledbmapper.logger import DefaultLogger

from tabledbmapper.engine import ConnHandle, ExecuteEngine, TemplateEngine, ConnBuilder
from tabledbmapper.manager.session.sql_session import SQLSession


class SessionPool:

    # _lock
    _lock = None

    # conn
    _conn_builder = None
    _conn_handle = None
    _execute_engine = None

    # Current number of connections
    _lazy_init = None
    _max_conn_number = 0

    _logger = None

    # conn engines
    _conns = None

    # use flag
    _flags = None

    def __init__(self, conn_builder: ConnBuilder, conn_handle: ConnHandle, execute_engine: ExecuteEngine,
                 lazy_init=True, max_conn_number=10, logger=DefaultLogger()):
        """
        Init session pool
        :param conn_builder: ConnBuilder
        :param conn_handle: ConnHandle
        :param execute_engine: ExecuteEngine
        :param lazy_init: lazy_init
        :param max_conn_number: max_conn_number
        :param logger: Logger
        """
        # lock
        self._lock = Lock()
        # conn
        self._conn_builder = conn_builder
        self._conn_handle = conn_handle
        self._execute_engine = execute_engine

        self._lazy_init = lazy_init
        self._max_conn_number = max_conn_number

        self._logger = logger

        # db conn
        self._conns = []
        # used conn
        self._flags = []
        # lazy loading
        if not lazy_init:
            for i in range(max_conn_number):
                self._conns.append(self._conn_builder.connect())
                self._flags.append(i)

    def get_session(self, auto_commit=True) -> SQLSession:
        """
        Get SQL Session from Session Pool
        :param auto_commit: auto_commit
        :return: SQL Session
        """
        self._lock.acquire()
        while True:
            flags_length = len(self._flags)
            conns_length = len(self._conns)
            # When connections are exhausted and 
            # the maximum number of connections is not exceeded
            if flags_length == 0 and conns_length < self._max_conn_number:
                # init new conn
                conn = self._conn_builder.connect()
                self._conns.append(conn)

                # create template engine
                template_engine = TemplateEngine(
                    self._conn_handle,
                    self._execute_engine,
                    conn,
                    auto_commit
                )
                template_engine.set_logger(self._logger)
                self._lock.release()
                return SQLSession(template_engine, self, conns_length)
            if flags_length > 0:
                # set use flag
                index = self._flags[0]
                self._flags = self._flags[1:]

                # get conn
                conn = self._conns[index]

                # create template engine
                template_engine = TemplateEngine(
                    self._conn_handle,
                    self._execute_engine,
                    conn,
                    auto_commit
                )
                template_engine.set_logger(self._logger)
                self._lock.release()
                return SQLSession(template_engine, self, index)

    def commit_session(self, index: int):
        """
        Commit session
        :param index: The index of the session in the Session pool
        """
        self._conn_handle.commit(self._conns[index])

    def rollback_session(self, index: int):
        """
        Commit session
        :param index: The index of the session in the Session pool
        """
        self._conn_handle.rollback(self._conns[index])

    def give_back_session(self, index: int):
        """
        Return the session to the session pool
        :param index: The index of the session in the Session pool
        """
        self._flags.append(index)

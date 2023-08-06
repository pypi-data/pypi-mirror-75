from functools import wraps
from typing import Callable, Dict

from tabledbmapper.manager.session.sql_session import SQLSession

from tabledbmapper.manager.session.sql_session_factory import SQLSessionFactory


SessionResult = Dict


# Add a decorator to the method to automatically open the session when you enter the method
def sqlsession(factory: SQLSessionFactory) -> Callable:
    # Gets the session factory location
    @wraps(factory)
    def decorator(func):
        # Method to add a decorator
        @wraps(func)
        def wrapper(*args, **kwargs) -> SessionResult:
            session_result = {}

            # Encapsulate as a new method
            def handle(session: SQLSession):
                # Injection of the session
                params = [session]
                for arg in args:
                    params.append(arg)
                new_args = tuple(params)
                session_result["data"] = func(*new_args, **kwargs)

            # Perform the session
            session_result["exception"] = factory.open_session(handle)
            return session_result
        return wrapper
    return decorator

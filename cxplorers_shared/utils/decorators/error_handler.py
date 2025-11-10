from functools import wraps
import logging
from typing import Callable, Any
from cxplorers_shared.domain.exceptions.repository import RepositoryError

logger = logging.getLogger("Error_handler")

def error_handler(module: str, type: str = "python") -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func) 
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(
                    msg=f"Error in {module}.{func.__name__}: {str(e)}"
                )

                match type:
                    case "repository":
                        raise RepositoryError()
                    case _:
                        raise     
        return wrapper
    return decorator
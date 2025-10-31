from functools import wraps
import logging
from typing import Callable, Any
from cxplorers_shared.domain.exceptions.repository import RepositoryError

logger = logging.getLogger("Error_handler")

def service_error_handler(module: str, type: str = "python") -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func) 
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.log(
                    message=f"Error in {func.__name__}",
                    level=logging.ERROR,
                    name=f"{module}.{func.__name__}",
                    exc_info=True,
                    stack_info=2
                )

                match type:
                    case "repository":
                        raise RepositoryError()
                    case _:
                        raise
                  
        return wrapper
    return decorator
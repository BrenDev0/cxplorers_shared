from functools import wraps
import logging
from typing import Callable, Any

logger = logging.getLogger("Error_handler")

def service_error_handler(module: str) -> Callable:
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
                raise  
        return wrapper
    return decorator
import pytest
import logging
from cxplorers_shared.utils.decorators.error_handler import error_handler
from cxplorers_shared.domain.exceptions.repository import RepositoryError

# Test function to apply the decorator
@error_handler(module="test.module", type="repository")
def function_with_repository_error():
    raise ValueError("This is a test error")

@error_handler(module="test.module", type="python")
def function_with_python_error():
    raise KeyError("This is another test error")

def test_error_handler_logs_repository_error(caplog):
    with caplog.at_level(logging.ERROR):
        with pytest.raises(RepositoryError):
            function_with_repository_error()
    
    # Print the captured log messages
    for record in caplog.records:
        print(f"LOGGED: {record.levelname} - {record.message}")
    
    # Check the log message
    assert len(caplog.records) == 1
    log_record = caplog.records[0]
    assert log_record.levelname == "ERROR"
    assert "Error in test.module.function_with_repository_error" in log_record.message
    assert log_record.name == "Error_handler"

def test_error_handler_logs_python_error(caplog):
    with caplog.at_level(logging.ERROR):
        with pytest.raises(KeyError):
            function_with_python_error()
    
    # Print the captured log messages
    for record in caplog.records:
        print(f"LOGGED: {record.levelname} - {record.message}")
    
    # Check the log message
    assert len(caplog.records) == 1
    log_record = caplog.records[0]
    assert log_record.levelname == "ERROR"
    assert "Error in test.module.function_with_python_error" in log_record.message
    assert log_record.name == "Error_handler"
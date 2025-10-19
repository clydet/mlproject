# Test Suite for ML Project

This directory contains comprehensive tests for the ML project modules, specifically focusing on `exception.py` and `logger.py`.

## Test Structure

```
tests/
├── __init__.py              # Test package initialization
├── conftest.py              # Pytest configuration and shared fixtures
├── test_exception.py        # Tests for exception.py module
└── test_logger.py           # Tests for logger.py module
```

## Test Coverage

### Exception Module Tests (`test_exception.py`)

- **TestErrorMessageDetail**: Tests the `error_message_detail` function
  - Valid error handling with traceback information
  - String error message formatting
  - None error handling
  - Complex error object handling

- **TestCustomException**: Tests the `CustomException` class
  - Initialization and inheritance from Exception
  - String representation (`__str__` method)
  - Exception raising and catching
  - Different error message types
  - Error message format validation

- **TestExceptionIntegration**: Integration tests
  - Real-world exception scenarios
  - Exception chaining

### Logger Module Tests (`test_logger.py`)

- **TestLoggerConfiguration**: Tests logger setup and configuration
  - Log file name format validation
  - Logs directory creation
  - Log file path construction
  - Logging basic configuration

- **TestLoggerFunctionality**: Tests logging functionality
  - Info, warning, and error message logging
  - Debug message filtering (INFO level)
  - Log message formatting

- **TestLoggerMainBlock**: Tests main block execution
  - Startup message logging when run as main
  - No execution when imported as module

- **TestLoggerEdgeCases**: Tests edge cases and error conditions
  - Permission errors during directory creation
  - Invalid file paths
  - Multiple module imports

- **TestLoggerIntegration**: Integration tests
  - Real-world logging scenarios
  - Exception logging

## Running Tests

### Prerequisites

Install the required testing dependencies:

```bash
pip install -r requirements.txt
```

### Running All Tests

```bash
# Run all tests
python run_tests.py

# Run with verbose output
python run_tests.py --verbose

# Run with coverage reporting
python run_tests.py --coverage

# Run specific test file
python run_tests.py --test tests/test_exception.py
```

### Alternative Methods

```bash
# Using pytest directly
pytest tests/

# With verbose output
pytest -v tests/

# With coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_exception.py
```

## Test Fixtures

The `conftest.py` file provides several useful fixtures:

- `temp_dir`: Creates a temporary directory for test files
- `mock_sys`: Mocks the sys module for exception testing
- `mock_datetime`: Mocks datetime for consistent log file naming

## Test Features

### Comprehensive Coverage
- Unit tests for individual functions and classes
- Integration tests for realistic scenarios
- Edge case testing for error conditions
- Mocking for isolated testing

### Mocking Strategy
- Uses `unittest.mock` for controlled testing
- Mocks external dependencies (file system, datetime)
- Isolates modules under test

### Error Testing
- Tests both expected and unexpected error conditions
- Validates error message formatting
- Tests exception inheritance and behavior

## Adding New Tests

When adding new tests:

1. Follow the existing naming conventions (`test_*.py`)
2. Use descriptive test class and method names
3. Include docstrings explaining test purpose
4. Use appropriate fixtures from `conftest.py`
5. Mock external dependencies appropriately
6. Test both success and failure cases

## Test Quality Guidelines

- **Isolation**: Each test should be independent
- **Clarity**: Test names should clearly describe what is being tested
- **Coverage**: Aim for comprehensive coverage of all code paths
- **Maintainability**: Tests should be easy to understand and modify
- **Reliability**: Tests should be deterministic and not flaky

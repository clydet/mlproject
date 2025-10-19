"""
Pytest configuration and shared fixtures for the test suite.
"""
import pytest
import sys
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# Add src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def mock_sys():
    """Mock sys module for testing exception handling."""
    with patch('sys.exc_info') as mock_exc_info:
        yield mock_exc_info

@pytest.fixture
def mock_datetime():
    """Mock datetime for consistent log file naming."""
    with patch('src.logger.datetime') as mock_dt:
        mock_dt.now.return_value.strftime.return_value = "01_01_2024_12_00_00"
        yield mock_dt

@pytest.fixture
def mock_logger_setup():
    """Mock the logger setup to avoid file system operations."""
    with patch('src.logger.os.getcwd') as mock_getcwd, \
         patch('src.logger.os.makedirs') as mock_makedirs, \
         patch('src.logger.os.path.join') as mock_join, \
         patch('src.logger.logging.basicConfig') as mock_basic_config:
        
        # Configure mocks
        mock_getcwd.return_value = "/test/directory"
        mock_join.side_effect = lambda *args: "/".join(args)
        
        yield {
            'getcwd': mock_getcwd,
            'makedirs': mock_makedirs,
            'join': mock_join,
            'basic_config': mock_basic_config
        }

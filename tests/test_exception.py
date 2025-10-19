"""
Test suite for exception.py module.

This module tests the CustomException class and error_message_detail function
to ensure proper error handling and message formatting.
"""
import pytest
import sys
from unittest.mock import patch, MagicMock
from src.exception import CustomException, error_message_detail


class TestErrorMessageDetail:
    """Test cases for the error_message_detail function."""
    
    def test_error_message_detail_with_valid_error(self, mock_sys):
        """Test error_message_detail with a valid error and traceback."""
        # Mock the exc_info return value
        mock_tb = MagicMock()
        mock_tb.tb_frame.f_code.co_filename = "/test/path/test_file.py"
        mock_tb.tb_lineno = 42
        
        mock_sys.return_value = (ValueError, ValueError("test error"), mock_tb)
        
        error = ValueError("test error")
        result = error_message_detail(error, sys)
        
        expected_message = "Error occurred in Python script name [/test/path/test_file.py] line number [42] error message [test error]"
        assert result == expected_message
    
    def test_error_message_detail_with_string_error(self, mock_sys):
        """Test error_message_detail with a string error message."""
        mock_tb = MagicMock()
        mock_tb.tb_frame.f_code.co_filename = "/another/path/script.py"
        mock_tb.tb_lineno = 15
        
        mock_sys.return_value = (RuntimeError, RuntimeError("string error"), mock_tb)
        
        error = "string error"
        result = error_message_detail(error, sys)
        
        expected_message = "Error occurred in Python script name [/another/path/script.py] line number [15] error message [string error]"
        assert result == expected_message
    
    def test_error_message_detail_with_none_error(self, mock_sys):
        """Test error_message_detail with None as error."""
        mock_tb = MagicMock()
        mock_tb.tb_frame.f_code.co_filename = "/test/none_error.py"
        mock_tb.tb_lineno = 1
        
        mock_sys.return_value = (TypeError, TypeError(None), mock_tb)
        
        error = None
        result = error_message_detail(error, sys)
        
        expected_message = "Error occurred in Python script name [/test/none_error.py] line number [1] error message [None]"
        assert result == expected_message
    
    def test_error_message_detail_with_complex_error(self, mock_sys):
        """Test error_message_detail with a complex error object."""
        mock_tb = MagicMock()
        mock_tb.tb_frame.f_code.co_filename = "/complex/error.py"
        mock_tb.tb_lineno = 100
        
        mock_sys.return_value = (Exception, Exception("complex error with details"), mock_tb)
        
        error = Exception("complex error with details")
        result = error_message_detail(error, sys)
        
        expected_message = "Error occurred in Python script name [/complex/error.py] line number [100] error message [complex error with details]"
        assert result == expected_message


class TestCustomException:
    """Test cases for the CustomException class."""
    
    def test_custom_exception_initialization(self, mock_sys):
        """Test CustomException initialization."""
        mock_tb = MagicMock()
        mock_tb.tb_frame.f_code.co_filename = "/test/init.py"
        mock_tb.tb_lineno = 5
        
        mock_sys.return_value = (ValueError, ValueError("init error"), mock_tb)
        
        error_message = "Custom error occurred"
        custom_exception = CustomException(error_message, sys)
        
        assert isinstance(custom_exception, Exception)
        assert isinstance(custom_exception, CustomException)
        assert custom_exception.error_message is not None
        assert "Custom error occurred" in custom_exception.error_message
    
    def test_custom_exception_str_method(self, mock_sys):
        """Test CustomException __str__ method."""
        mock_tb = MagicMock()
        mock_tb.tb_frame.f_code.co_filename = "/test/str.py"
        mock_tb.tb_lineno = 10
        
        mock_sys.return_value = (RuntimeError, RuntimeError("str test"), mock_tb)
        
        error_message = "String test error"
        custom_exception = CustomException(error_message, sys)
        
        str_result = str(custom_exception)
        assert str_result == custom_exception.error_message
        assert "String test error" in str_result
        assert "/test/str.py" in str_result
        assert "10" in str_result
    
    def test_custom_exception_inheritance(self, mock_sys):
        """Test that CustomException properly inherits from Exception."""
        mock_tb = MagicMock()
        mock_tb.tb_frame.f_code.co_filename = "/test/inheritance.py"
        mock_tb.tb_lineno = 1
        
        mock_sys.return_value = (Exception, Exception("inheritance test"), mock_tb)
        
        error_message = "Inheritance test"
        custom_exception = CustomException(error_message, sys)
        
        # Test isinstance checks
        assert isinstance(custom_exception, Exception)
        assert isinstance(custom_exception, CustomException)
        
        # Test that it can be raised and caught
        with pytest.raises(CustomException) as exc_info:
            raise custom_exception
        
        assert exc_info.value == custom_exception
        assert str(exc_info.value) == custom_exception.error_message
    
    def test_custom_exception_with_different_error_types(self, mock_sys):
        """Test CustomException with different types of error messages."""
        test_cases = [
            ("Simple string error", "/test/simple.py", 1),
            ("Error with numbers: 123", "/test/numbers.py", 25),
            ("Error with special chars: !@#$%", "/test/special.py", 50),
            ("", "/test/empty.py", 0),  # Empty string
            ("Error with\nnewlines", "/test/newlines.py", 10),
        ]
        
        for error_msg, filename, line_num in test_cases:
            mock_tb = MagicMock()
            mock_tb.tb_frame.f_code.co_filename = filename
            mock_tb.tb_lineno = line_num
            
            mock_sys.return_value = (Exception, Exception(error_msg), mock_tb)
            
            custom_exception = CustomException(error_msg, sys)
            
            assert error_msg in custom_exception.error_message
            assert filename in custom_exception.error_message
            assert str(line_num) in custom_exception.error_message
    
    def test_custom_exception_error_message_format(self, mock_sys):
        """Test the format of the error message."""
        mock_tb = MagicMock()
        mock_tb.tb_frame.f_code.co_filename = "/format/test.py"
        mock_tb.tb_lineno = 33
        
        mock_sys.return_value = (ValueError, ValueError("format test"), mock_tb)
        
        error_message = "Format test error"
        custom_exception = CustomException(error_message, sys)
        
        error_msg = custom_exception.error_message
        
        # Check that the message follows the expected format
        assert error_msg.startswith("Error occurred in Python script name [")
        assert error_msg.endswith("]")
        assert "line number [" in error_msg
        assert "error message [" in error_msg
        
        # Check specific components
        assert "/format/test.py" in error_msg
        assert "33" in error_msg
        assert "Format test error" in error_msg
    
    def test_custom_exception_raises_properly(self, mock_sys):
        """Test that CustomException can be raised and caught properly."""
        mock_tb = MagicMock()
        mock_tb.tb_frame.f_code.co_filename = "/raise/test.py"
        mock_tb.tb_lineno = 7
        
        mock_sys.return_value = (Exception, Exception("raise test"), mock_tb)
        
        error_message = "Raise test error"
        
        # Test raising the exception
        with pytest.raises(CustomException) as exc_info:
            raise CustomException(error_message, sys)
        
        # Verify the exception details
        assert exc_info.value.error_message is not None
        assert "Raise test error" in str(exc_info.value)
        assert "/raise/test.py" in str(exc_info.value)
        assert "7" in str(exc_info.value)


class TestExceptionIntegration:
    """Integration tests for exception handling."""
    
    def test_exception_in_real_scenario(self):
        """Test exception handling in a realistic scenario."""
        def problematic_function():
            """A function that raises an exception."""
            raise ValueError("Something went wrong in the function")
        
        try:
            problematic_function()
        except ValueError as e:
            # Create CustomException with the caught exception
            custom_exception = CustomException(str(e), sys)
            
            # Verify the custom exception contains useful information
            assert "Something went wrong in the function" in custom_exception.error_message
            assert "problematic_function" in custom_exception.error_message or "test_exception" in custom_exception.error_message
    
    def test_exception_chaining(self, mock_sys):
        """Test exception chaining with CustomException."""
        mock_tb = MagicMock()
        mock_tb.tb_frame.f_code.co_filename = "/chain/test.py"
        mock_tb.tb_lineno = 20
        
        mock_sys.return_value = (Exception, Exception("chained error"), mock_tb)
        
        try:
            raise ValueError("Original error")
        except ValueError as original:
            try:
                raise CustomException(f"Wrapped: {str(original)}", sys)
            except CustomException as wrapped:
                assert "Wrapped: Original error" in str(wrapped)
                assert "/chain/test.py" in str(wrapped)
                assert "20" in str(wrapped)


if __name__ == "__main__":
    pytest.main([__file__])

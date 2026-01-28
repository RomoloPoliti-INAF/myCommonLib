import logging
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from MyCommonLib.loginit import logInit
from MyCommonLib.customLogger import CustomLogger, SpecialHandler
from MyCommonLib.constants import FMODE

class TestLogInit:
    """Test suite for logInit function"""

    def test_logInit_default_parameters(self):
        """Test logInit with default parameters"""
        logger = logInit()
        assert isinstance(logger, CustomLogger)
        assert logger.name == "MyLogger"
        assert logger.level == 20
        assert len(logger.handlers) == 1
        assert isinstance(logger.handlers[0], SpecialHandler)

    def test_logInit_with_custom_logger_name(self):
        """Test logInit with custom logger name"""
        logger = logInit(logger="TestLogger")
        assert logger.name == "TestLogger"

    def test_logInit_with_valid_log_levels(self):
        """Test logInit with all valid log levels"""
        valid_levels = [0, 10, 20, 30, 40, 50]
        for level in valid_levels:
            logger = logInit(logLevel=level)
            assert logger.level == level

    def test_logInit_with_invalid_log_level(self):
        """Test logInit with invalid log level defaults to 20 and warns"""
        with patch.object(CustomLogger, 'warning') as mock_warning:
            logger = logInit(logLevel=25)
            assert logger.level == 20
            mock_warning.assert_called_once()
            args = mock_warning.call_args[0][0]
            assert "Log level 25 is not valid" in args

    def test_logInit_with_file_handler(self, tmp_path):
        """Test logInit creates file handler when logFile is provided"""
        log_file = tmp_path / "test.log"
        logger = logInit(logFile=log_file)
        assert len(logger.handlers) == 1
        assert isinstance(logger.handlers[0], logging.FileHandler)
        assert logger.handlers[0].baseFilename == str(log_file)

    def test_logInit_with_custom_file_mode(self, tmp_path):
        """Test logInit with custom file mode"""
        log_file = tmp_path / "test.log"
        logger = logInit(logFile=log_file, fileMode=FMODE.WRITE)
        assert logger.handlers[0].mode == FMODE.WRITE # type: ignore

    def test_logInit_with_custom_format(self):
        """Test logInit with custom output format"""
        custom_format = '{levelname} - {message}'
        logger = logInit(out_format=custom_format)
        handler = logger.handlers[0]
        assert handler.formatter._fmt == custom_format # type: ignore

    def test_logInit_default_format(self):
        """Test logInit uses default format when out_format is None"""
        logger = logInit()
        handler = logger.handlers[0]
        expected_format = '{asctime} | {levelname:8} | {name:10} | {module:12} | {funcName:20} | {lineno:4} | {message}'
        assert handler.formatter._fmt == expected_format # type: ignore

    def test_logInit_formatter_date_format(self):
        """Test logInit sets correct date format"""
        logger = logInit()
        handler = logger.handlers[0]
        assert handler.formatter.datefmt == '%m/%d/%Y %I:%M:%S %p' # type: ignore

    def test_logInit_formatter_style(self):
        """Test logInit uses correct formatter style"""
        logger = logInit()
        handler = logger.handlers[0]
        assert handler.formatter._style._fmt == handler.formatter._fmt # type: ignore

    def test_logInit_sets_logger_class(self):
        """Test logInit sets CustomLogger as logger class"""
        with patch('logging.setLoggerClass') as mock_set_class:
            logInit()
            mock_set_class.assert_called_once_with(CustomLogger)

    def test_logInit_multiple_invalid_levels(self):
        """Test various invalid log levels"""
        invalid_levels = [5, 15, 25, 35, 45, 55, 100, -10]
        for level in invalid_levels:
            logger = logInit(logLevel=level)
            assert logger.level == 20

    def test_logInit_file_creation(self, tmp_path):
        """Test that log file is created when specified"""
        log_file = tmp_path / "new_test.log"
        logger = logInit(logFile=log_file)
        logger.info("Test message")
        assert log_file.exists()

    def test_logInit_returns_custom_logger_instance(self):
        """Test that logInit returns CustomLogger instance"""
        logger = logInit()
        assert type(logger).__name__ == 'CustomLogger' # type: ignore
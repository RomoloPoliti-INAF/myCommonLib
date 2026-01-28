import pytest
import logging
import yaml
from pathlib import Path
from unittest.mock import Mock, patch, mock_open, MagicMock
from MyCommonLib.configuration import Loader, read_yaml, write_yaml, Configure
from MyCommonLib.constants import FMODE

class TestLoader:
    def test_loader_inheritance(self):
        """Test that Loader inherits from yaml.SafeLoader"""
        assert issubclass(Loader, yaml.SafeLoader)

    def test_loader_include_constructor(self, tmp_path):
        """Test the !include constructor"""
        # Create main and included YAML files
        included_file = tmp_path / "included.yaml"
        included_file.write_text("key: value\n")
        
        main_file = tmp_path / "main.yaml"
        main_file.write_text("!include included.yaml\n")
        
        with open(main_file, 'r') as f:
            result = yaml.load(f, Loader=Loader)
        
        assert result == {"key": "value"}


class TestReadYaml:
    def test_read_yaml_success(self, tmp_path):
        """Test successful YAML file reading"""
        test_file = tmp_path / "test.yaml"
        test_data = {"name": "test", "value": 123}
        test_file.write_text(yaml.dump(test_data))
        
        result = read_yaml(test_file)
        assert result == test_data

    def test_read_yaml_with_string_path(self, tmp_path):
        """Test reading YAML with string path"""
        test_file = tmp_path / "test.yaml"
        test_data = {"key": "value"}
        test_file.write_text(yaml.dump(test_data))
        
        result = read_yaml(Path(test_file))
        assert result == test_data

    def test_read_yaml_file_not_found(self):
        """Test FileNotFoundError is raised for non-existent file"""
        with pytest.raises(FileNotFoundError):
            read_yaml(Path("/nonexistent/file.yaml"))


class TestWriteYaml:
    def test_write_yaml_success(self, tmp_path):
        """Test successful YAML file writing"""
        test_file = tmp_path / "output.yaml"
        test_data = {"name": "test", "value": 456}
        
        write_yaml(test_data, test_file)
        
        assert test_file.exists()
        with open(test_file, 'r') as f:
            result = yaml.safe_load(f)
        assert result == test_data

    def test_write_yaml_with_string_path(self, tmp_path):
        """Test writing YAML with string path"""
        test_file = tmp_path / "output.yaml"
        test_data = {"key": "value"}
        
        write_yaml(test_data, str(test_file))
        assert test_file.exists()

    def test_write_yaml_file_exists_no_overwrite(self, tmp_path):
        """Test FileExistsError when file exists and overwrite=False"""
        test_file = tmp_path / "existing.yaml"
        test_file.write_text("existing content")
        
        with pytest.raises(FileExistsError):
            write_yaml({"key": "value"}, test_file, overwrite=False)

    def test_write_yaml_file_exists_with_overwrite(self, tmp_path):
        """Test overwriting existing file"""
        test_file = tmp_path / "existing.yaml"
        test_file.write_text("existing content")
        test_data = {"new": "data"}
        
        write_yaml(test_data, test_file, overwrite=True)
        
        with open(test_file, 'r') as f:
            result = yaml.safe_load(f)
        assert result == test_data

    def test_write_yaml_invalid_data_type(self, tmp_path):
        """Test TypeError for non-dict data"""
        test_file = tmp_path / "output.yaml"
        
        with pytest.raises(TypeError):
            write_yaml("not a dict", test_file) #type:ignore


class TestConfigure:
    def test_configure_initialization(self):
        """Test Configure class initialization"""
        config = Configure()
        
        assert config._name == "Software Configuration"
        assert config._logger == 'MyLogger'
        assert config._debug is False
        assert config._verbose == 0
        assert config.configFile is None
        assert config._logFile is None
        assert config.log is None
        assert config.log_mode == FMODE.APPEND

    @patch('MyCommonLib.configuration.logInit')
    def test_start_log(self, mock_log_init):
        """Test start_log method"""
        config = Configure()
        mock_logger = Mock()
        mock_log_init.return_value = mock_logger
        
        config.start_log(FMODE.WRITE)
        
        mock_log_init.assert_called_once()
        assert config.log == mock_logger

    @patch('MyCommonLib.configuration.logInit')
    def test_logfile_setter(self, mock_log_init, tmp_path):
        """Test logFile setter"""
        config = Configure()
        mock_logger = Mock()
        mock_handler = Mock()
        mock_logger.handlers = [mock_handler]
        config.log = mock_logger
        
        log_file = tmp_path / "test.log"
        config.logFile = log_file
        
        assert config._logFile == log_file
        assert config.log_file == log_file.as_posix()

    @patch('MyCommonLib.configuration.softMode')
    @patch('MyCommonLib.configuration.logInit')
    def test_debug_setter_true(self, mock_log_init, mock_soft_mode, tmp_path):
        """Test debug setter with True value"""
        config = Configure()
        mock_logger = Mock()
        config.log = mock_logger
        config._logFile = tmp_path / "test.log"
        
        config.debug = True
        
        assert config._debug is True
        assert config.debug_status is True
        mock_logger.setLevel.assert_called_with(logging.DEBUG)

    @patch('MyCommonLib.configuration.softMode')
    @patch('MyCommonLib.configuration.logInit')
    def test_debug_setter_false(self, mock_log_init, mock_soft_mode):
        """Test debug setter with False value"""
        config = Configure()
        mock_logger = Mock()
        config.log = mock_logger
        config._logFile = Path("/tmp/test.log")
        
        config.debug = False
        
        assert config._debug is False
        mock_logger.setLevel.assert_called_with(logging.INFO)

    @patch('MyCommonLib.configuration.softMode')
    def test_verbose_setter(self, mock_soft_mode):
        """Test verbose setter"""
        config = Configure()
        
        config.verbose = 3
        
        assert config._verbose == 3
        assert config.verbose_status == "Level 3"

    @patch('MyCommonLib.configuration.softMode')
    def test_verbosity(self, mock_soft_mode):
        """Test verbosity method"""
        config = Configure()
        mock_soft_mode.check.return_value = True
        
        result = config.verbosity(2)
        
        mock_soft_mode.check.assert_called_with(2)
        assert result is True

    def test_to_dict(self):
        """Test toDict method"""
        config = Configure()
        config.debug_status = True
        config.verbose_status = "Level 2"
        
        result = config.toDict()
        
        assert isinstance(result, dict)
        assert 'debug_status' in result
        assert 'log' not in result  # excluded
        assert not any(key.startswith('_') for key in result.keys())

    @patch('MyCommonLib.configuration.softMode')
    def test_to_dict_with_posix_path(self, mock_soft_mode, tmp_path):
        """Test toDict with PosixPath conversion"""
        config = Configure()
        config.configFile = tmp_path / "config.yaml"
        
        result = config.toDict()
        
        assert isinstance(result['configFile'], str)

    @patch('MyCommonLib.configuration.dict2Table')
    @patch('MyCommonLib.configuration.softMode')
    def test_show(self, mock_soft_mode, mock_dict2table):
        """Test Show method"""
        config = Configure()
        mock_console = Mock()
        config.console = mock_console
        
        config.Show()
        
        mock_dict2table.assert_called_once()
        mock_console.print.assert_called_once()

    @patch('MyCommonLib.configuration.logInit')
    def test_set_log_default(self, mock_log_init, tmp_path):
        """Test setLog with default=True"""
        config = Configure()
        mock_logger = Mock()
        mock_handler = Mock()
        mock_logger.handlers = [mock_handler]
        config.log = mock_logger
        
        with patch('MyCommonLib.configuration.defLogFile', 'app.log'):
            config.setLog(default=True)
            
            assert config._logFile == Path('/tmp/log/app.log')

    @patch('MyCommonLib.configuration.logInit')
    def test_set_log_custom(self, mock_log_init, tmp_path):
        """Test setLog with custom path"""
        config = Configure()
        mock_logger = Mock()
        mock_handler = Mock()
        mock_logger.handlers = [mock_handler]
        config.log = mock_logger
        
        log_path = tmp_path / "custom.log"
        if not log_path is None:
            config.setLog(value=Path(log_path))
        
        assert config._logFile == log_path
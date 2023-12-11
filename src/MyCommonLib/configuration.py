import logging
from os import path
from pathlib import Path, PosixPath

import yaml
from rich.console import Console
from rich.panel import Panel
from MyCommonLib.software_mode import softMode

from MyCommonLib.constants import COLOR, FMODE
from MyCommonLib.dictman import dict2Table
from MyCommonLib.loginit import logInit

defLogFile = 'software_logger.log'


class Loader(yaml.SafeLoader):
    """Add to the YAML standar class the command !include to include slave yaml file"""

    def __init__(self, stream):
        self._root = path.split(stream.name)[0]
        super(Loader, self).__init__(stream)

    def include(self, node):
        filename = path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r') as f:
            return yaml.load(f, Loader)


Loader.add_constructor('!include', Loader.include)


def read_yaml(filepath: Path) -> dict:
    ''' Read a yaml file'''
    with open(filepath, 'r') as f:
        # return yaml.safe_load(f)
        return yaml.load(f, Loader)


def write_yamls(data, fileName):
    with open(fileName, FMODE.WRITE) as file:
        documents = yaml.dump(data, file)


class Configure:
    """Configuration class"""

    def __init__(self):
        self._name = "Software Configuration"
        self._logger = 'MyLogger'
        self._debug = False
        self._verbose = 0
        self.configFile = None
        self._logFile = None
        self.console: Console = softMode.console
        self._dict_exclude=['log']
        self.log=logging.Logger('default')

    @property
    def logFile(self):
        return self._logFile

    @logFile.setter
    def logFile(self, value: Path):
        
        self._logFile = value.expanduser()
        self.log = logInit(logFile=value, logger=self._logger,
                           logLevel=logging.INFO, fileMode=FMODE.APPEND)
        self.log_file = value.as_posix()

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value):
        self._debug = value
        if value:
            if self._logFile is not None:
                self.log.setLevel(logging.DEBUG)
                self.log.debug("Set the loglevel to Debug", verbosing=1)
            softMode.debug = value
        else:
            if self._logFile is not None:
                self.log.setLevel(logging.INFO)
            softMode.debug = False
        self.debug_status = value

    @property
    def verbose(self) -> int:
        return self._verbose

    @verbose.setter
    def verbose(self, value: int):
        self._verbose = value
        softMode.verbose = value
        self.verbose_status=f"Level {value}"

    def verbosity(self, level: int = 0) -> bool:
        return softMode.check(level)

    def toDict(self) -> dict:
        ret = {}
        for item in self.__dict__:
            if not item.startswith('_') and not item in self._dict_exclude:
                elem = getattr(self, item)
                if type(elem) is PosixPath:
                    ret[item] = str(elem)
                else:
                    ret[item] = elem
        return dict(sorted(ret.items()))

    def Show(self):
        pn = Panel(dict2Table(self.toDict()), title=self._name,
                   expand=False, border_style=COLOR.panel)
        self.console.print(pn)

    def setLog(self, value: Path = None, default: bool = False):
        if default:
            self.logFile = Path('/val/log').joinpath(defLogFile)
        else:
            self.logFile = value

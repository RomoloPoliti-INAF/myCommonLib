import logging
from pathlib import Path

from MyCommonLib.constants import FMODE
from MyCommonLib.customLogger import CustomLogger

__doc__ = "Inizialize the logger"
__version__ = "2.0.0"


def logInit(logFile: Path= None, logger:str="MyLogger", logLevel:int=20, fileMode:str=FMODE.APPEND) -> logging:

    flag = False
    if not logLevel in [0, 10, 20, 30, 40, 50]:
        oldLevel = logLevel
        flag = True
        logLevel = 20
    logging.setLoggerClass(CustomLogger)
    # logging.basicConfig(filename=logFile,
    #                     level=logLevel,
    #                     filemode=fileMode,
    #                     format='%(asctime)s | %(levelname)-8s | %(name)-7s | %(module)-12s | %(funcName)-20s | %(message)s',
    #                     datefmt='%m/%d/%Y %I:%M:%S %p')
    a1 = CustomLogger(logger)
    a1.setLevel(logLevel)
    # Aggiungi un handler per scrivere nel file di log
    formatter = logging.Formatter('{asctime} | {levelname:8} | {name:10} | {module:12} | {funcName:20} | {lineno:4} | {message}',
                                  datefmt='%m/%d/%Y %I:%M:%S %p',
                                  style="{")
    if logFile is None:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        a1.addHandler(stream_handler)
    else:
        file_handler = logging.FileHandler(logFile, mode=fileMode)
        file_handler.setFormatter(formatter)
        a1.addHandler(file_handler)
    if flag:
        a1.warning(
            f"Log level {oldLevel} is not valid. Used the default value 20")
    return a1  # logging

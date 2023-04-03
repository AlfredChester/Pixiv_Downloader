import time
from loguru import logger
from typing import Any
from libs.Configs import Configs

def getNowTime() -> str:
    return time.strftime(
        Configs.timeConfigs.timeFormat, time.localtime()
    )

def writeLog(data: Any, logType:str = "INFO") -> None:
    logObject = open(
        Configs.logConfigs.fileName, "a" ,
        encoding = Configs.logConfigs.fileEncoding
    )
    funcMap = {
        "INFO":     logger.info,
        "DEBUG":    logger.debug,
        "ERROR":    logger.error,
        "CRITICAL": logger.critical,
        "WARNING":  logger.warning,
        "SUCCESS":  logger.success,
        "TRACE":    logger.trace
    }
    fileOutputTypes = {
        "INFO":     "| INFO     | ",
        "DEBUG":    "| DEBUG    | ",
        "ERROR":    "| ERROR    | ",
        "CRITICAL": "| CRITICAL | ",
        "WARNING":  "| WARNING  | ",
        "SUCCESS":  "| SUCCESS  | ",
        "TRACE":    "| TRACE    | "
    }
    toUseFunc  = funcMap[logType]
    if isinstance(data, list): 
        for item in data:
            item = item.replace("\n", "")
            if (Configs.logConfigs.needFileOutPut):
                logObject.write(
                    getNowTime() + fileOutputTypes[logType] + str(item) + '\n'
                )
            if (Configs.logConfigs.needConsoleOutPut):
                toUseFunc(str(item))
        logObject.close()
        return

    if isinstance(data, str):
        data = data.replace("\n", "")
        if (Configs.logConfigs.needFileOutPut):
            logObject.write(getNowTime() + fileOutputTypes[logType] + data + '\n')
        if (Configs.logConfigs.needConsoleOutPut):
            toUseFunc(data)
        logObject.close()
        return

    else:
        logObject.close()
        writeLog("Error: logType is not supported", "ERROR")
        raise TypeError("Data type not supported")

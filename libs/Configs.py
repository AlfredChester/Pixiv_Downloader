class Configs:
    __name__ = "Configs"
    class logConfigs:
        needConsoleOutPut   = True
        needFileOutPut      = True
        loglevel            = "DEBUG"
        fileName            = "downloader.log"
        fileEncoding        = "utf-8"

    class timeConfigs:
        timeFormat          = "%Y-%m-%d [%H:%M:%S] "
        timeZone            = "Asia/Shanghai"

    class DownloadConfigs:
        DownloadRoute  = "lsp-frontend\\Downloads"
        standard_Input = True
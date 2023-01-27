from libs.Downloader import *
from libs.Rhodeslogger import writeLog
from libs.Configs import Configs
from random import randint

def isInt(val) -> bool:
    try:
        v = int(val)
        return True
    except Exception:
        return False

def main() -> int:
    route = Configs.DownloadConfigs.DownloadRoute
    downloader = Downloader(downloadRoute=route)
    while True:
        pid = input("请输入要下载的图片的pid: ")
        if pid == "exit":
            return 0
        if pid == "cls":
            system("cls")
            continue
        if pid == "uploadGit":
            system("python Git_Uploader.py")
            continue
        if pid == "novel":
            writeLog("Developing this Function!")
            return 0xBADBEEF
        if pid == "rand":
            downloader.download(str(randint(70000000, 104000000)))
            continue
        if isInt(pid):
            downloader.download(pid)
        else:
            writeLog("Invalid Input", "ERROR")

if __name__ == '__main__':
    exitId = main()
    writeLog(f'Exit Id: {exitId}')
    exit(exitId)
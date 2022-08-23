from libs.Downloader import *
from libs.Rhodeslogger import writeLog
from libs.Configs import Configs

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
            return -1
        downloader.download(pid)

if __name__ == '__main__':
    exitId = main()
    writeLog(f'Exit Id: {exitId}')
    exit(exitId)
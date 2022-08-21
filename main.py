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
            system("pause")
        downloader.download(pid)

if __name__ == '__main__':
    exitId = main()
    writeLog(f'Exit Id: {exitId}')
    exit(exitId)
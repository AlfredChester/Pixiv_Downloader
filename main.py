from libs.Downloader import *
from libs.Rhodeslogger import writeLog

def main() -> int:
    route = input("输入下载图片的路径: ")
    downloader = Downloader(downloadRoute=route)
    while True:
        pid = input("请输入要下载的图片的pid: ")
        if pid == "exit":
            return 0
        downloader.download(pid)

if __name__ == '__main__':
    exitId = main()
    writeLog(f'Exit Id: {exitId}')
    exit(exitId)
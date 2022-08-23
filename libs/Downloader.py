from os import system
import time
from libs.Rhodeslogger import writeLog
from requests import get

class Downloader(object):
    def __init__(self ,
        rootPath: str       = "https://pixiv.re", 
        downloadRoute: str  = "Downloads"
    ):
        self.source = rootPath
        self.downloadRoute = downloadRoute
        writeLog('Picture Downloader init success')
        writeLog(f'Source: {self.source}')
        writeLog(f'DownloadRoute: {self.downloadRoute}')

    def singleDownload(self, pid):
        requestURL = f'{self.source}/{pid}.jpg'
        binaryPictureContent = get(requestURL)
        if str(binaryPictureContent) == '<Response [404]>':
            return
        if str(binaryPictureContent) == '<Response [503]>':
            time.sleep(45)
            self.singleDownload(pid)
        file = open(
            f'{self.downloadRoute}\\{pid}\\singlePicture.jpg', 'wb'
        )
        file.write(binaryPictureContent.content)
        file.close()
        writeLog(f'Download {pid}-singlePicture.jpg success')

    def download(self, pid):
        system(f"mkdir {self.downloadRoute} & cd {self.downloadRoute} & mkdir {pid}")
        cnt = 1
        while True:
            requireSleep = False
            try:
                requestURL = f'{self.source}/{pid}-{cnt}.jpg'
                writeLog(f'Request URL: {requestURL}')
                binaryPictureContent = get(requestURL)
                if str(binaryPictureContent) == '<Response [404]>':
                    writeLog(
                        f'Picture {pid}-{cnt}.jpg 404',
                          logType = "WARNING"
                    )
                    if cnt == 1:
                        self.singleDownload(pid)
                    else:
                        writeLog('Download finished')
                    return
                if str(binaryPictureContent) == '<Response [503]>':
                    writeLog(
                        f'Picture {pid}-{cnt}.jpg 503, sleeping for 45 second',
                          logType = "WARNING"
                    )
                    requireSleep = True

                if not requireSleep:
                    file = open(
                        f'{self.downloadRoute}\\{pid}\\{cnt}.jpg', 'wb'
                    )
                    file.write(binaryPictureContent.content)
                    file.close()
                    writeLog(f'Download {pid}-{cnt}.jpg success')
            
            except Exception as e:
                writeLog(f'Download Ended, Error: {e}')
                break

            if requireSleep:
                time.sleep(45)
            else:
                cnt += 1

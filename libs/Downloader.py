from os import system
import time
from libs.Rhodeslogger import writeLog
from requests import get


class Downloader(object):
    def __init__(self,
                 rootUrl: str = "https://pixiv.re",
                 downloadRoute: str = "Downloads"
                 ):
        self.source = rootUrl
        self.downloadRoute = downloadRoute
        writeLog('Picture Downloader init success')
        writeLog(f'Source: {self.source}')
        writeLog(f'DownloadRoute: {self.downloadRoute}')

    def singleDownload(self, pid):
        requestURL = f'{self.source}/{pid}.png'
        binaryPictureContent = get(requestURL)
        if str(binaryPictureContent) == '<Response [404]>':
            # TODO Remove directory
            writeLog(
                'Single Picture Download returned 404, this picture may be deleted or don\'t even exist', 'ERROR')
            return
        if str(binaryPictureContent) == '<Response [503]>':
            time.sleep(45)
            self.singleDownload(pid)
        file = open(
            f'{self.downloadRoute}/{pid}/singlePicture.png', 'wb'
        )
        file.write(binaryPictureContent.content)
        file.close()
        writeLog(f'Download {pid}-singlePicture.png success')

    def download(self, pid):
        system(f"mkdir {self.downloadRoute}/{pid}")
        cnt = 1
        while True:
            requireSleep = False
            try:
                requestURL = f'{self.source}/{pid}-{cnt}.png'
                writeLog(f'Request URL: {requestURL}')
                binaryPictureContent = get(requestURL)
                if str(binaryPictureContent) == '<Response [404]>':
                    writeLog(
                        f'Picture {pid}-{cnt}.png 404',
                        logType="WARNING"
                    )
                    if cnt == 1:
                        self.singleDownload(pid)
                    else:
                        writeLog('Download finished')
                    return
                if str(binaryPictureContent) == '<Response [503]>':
                    writeLog(
                        f'Picture {pid}-{cnt}.png 503, sleeping for 45 second',
                        logType="WARNING"
                    )
                    requireSleep = True

                if not requireSleep:
                    file = open(
                        f'{self.downloadRoute}/{pid}/{cnt}.png', 'wb'
                    )
                    file.write(binaryPictureContent.content)
                    file.close()
                    writeLog(f'Download {pid}-{cnt}.png success')

            except Exception as e:
                writeLog(f'Download Ended, Error: {e}', logType="ERROR")
                break

            if requireSleep:
                time.sleep(45)
            else:
                cnt += 1

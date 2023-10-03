import os.path
import pathlib
import subprocess
from threading import Lock

from DownloadException import DownloadException


class AudioDownloader:
    def __init__(self):
        self.temp_id = 0
        self.file_template = 'TEMP_FILE_{}.{}'
        self.folder = 'temps'
        self.lock = Lock()

    def __get_temp_id(self) -> int:
        self.lock.acquire()
        temp_id = self.temp_id
        self.temp_id += 1
        self.lock.release()
        return temp_id

    def __clear_cache(self):
        result = subprocess.run(
            ['./yt-dlp', "--rm-cache-dir"],
            capture_output=True
        )

        if result.returncode != 0:
            raise DownloadException('Cannot delete cache of yt-dlp!')

    def is_file_larger_than_max(self, result) -> bool:
        return result.stdout.decode('utf-8').find('File is larger than max-filesize') != -1

    def __download_to_temp(self, temp_id, temp_format, yt_link):
        temp_path = os.path.join(self.folder, self.file_template.format(temp_id, temp_format))
        result = subprocess.run(
            ['./yt-dlp', '--extract-audio',
             '--audio-format', temp_format,
             '--max-filesize', '10m',
             '--output', temp_path,
             yt_link],
            capture_output=True
        )

        if self.is_file_larger_than_max(result):
            self.delete(f'{os.path.join(self.folder, self.file_template.format(temp_id, "webm"))}.part')
            raise DownloadException(f'Error when downloading {yt_link}: file too big')

        if result.returncode != 0:
            raise DownloadException(f'Error when downloading {yt_link}: something went wrong')
        return temp_path

    def __temp_to_wav(self, temp_id, temp_path, final_format):
        final_path = os.path.join(self.folder, self.file_template.format(temp_id, final_format))
        result = subprocess.run(
            ['ffmpeg', '-i', temp_path, final_path],
            capture_output=True
        )

        self.delete(temp_path)
        if result.returncode != 0:
            raise DownloadException(f'Error when converting {temp_path} to wav file')
        return final_path

    def download(self, yt_link: str) -> str:
        self.__clear_cache()
        temp_id = self.__get_temp_id()
        temp_path = self.__download_to_temp(temp_id, 'm4a', yt_link)
        final_path = self.__temp_to_wav(temp_id, temp_path, 'wav')
        return final_path

    def delete(self, path):
        file = pathlib.Path(path)
        file.unlink()


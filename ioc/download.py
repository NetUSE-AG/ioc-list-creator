import requests
import json
import os
from datetime import datetime
from pathlib import Path
from concurrent import futures
from urllib.request import url2pathname

class Downloader:
    """
    Class for handling all downloads
    """

    def __init__(self, download_list, download_dir):
        """Constructor for class Downloader

        Args:
            download_list (Path): File with all downloads
            download_dir (Path): Folder to save downloaded files to
        """
        self.download_list = download_list
        self.download_dir = download_dir
        self.files = []
        self.session = requests.Session()
        self.session.mount("file://", LocalFileAdapter())

    def _file_download(self, file, timestamp):
        """Internal function to download a file from the internet

        Args:
            file (json): File to download
            timestamp (str): Download timestamp
        """
        r = self.session.get(file['url'], stream=True)
        if r.status_code == 200:
            file_name = f"{timestamp}_{file['source']}_{file['url'].split('/')[-1]}"
            file_path = os.path.join(self.download_dir.name, file_name)
            with open(file_path, "wb") as fout:
                for chunk in r.iter_content(chunk_size=4096):
                    fout.write(chunk)
            file['path'] = Path(file_path)
            self.files.append(file)
        else:
            print(f"\t[-]\t{file['url']} is not available. Skipping")

    def download_files(self):
        """Function to download all neccessary files
        Starts a Thread for each single file to download
        """
        timestamp = datetime.now().strftime("%m%d%Y-%H%M%S")
        with open(self.download_list, "r") as dl:
            download_data = json.loads(dl.read())
        for file in download_data:
            self._file_download(file, timestamp)

class LocalFileAdapter(requests.adapters.BaseAdapter):
    @staticmethod
    def _check_path(method, path):
        if method.lower() in ("put", "delete", "post"):
            return 501, "Not Implemented"
        elif method.lower() not in ("get", "head"):
            return 405, "Method Not Allowed"
        elif Path(path).is_dir():
            return 400, "Path Is Not A File"
        elif not Path(path).is_file():
            return 404, "File Not Found"
        elif not os.access(path, os.R_OK):
            return 403, "Access Denied"
        else:
            return 200, "OK"

    def send(self, req, **kwargs):
        path = os.path.normcase(os.path.normpath(url2pathname(req.path_url)))
        response = requests.Response()

        response.status_code, response.reason = self._check_path(req.method, path)
        if response.status_code == 200 and req.method.lower() != "head":
            try:
                response.raw = open(path, "rb")
            except (OSError, IOError) as err:
                response.status_code = 500
                response.reason = str(err)

        if isinstance(req.url, bytes):
            response.url = requ.url.decode("utf-8")
        else:
            response.url = req.url

        response.request = req
        response.connection = self

        return response

    def close(self):
        pass

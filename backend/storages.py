from django.core.files.storage import Storage
from django.core.files import File
from django.conf import settings
from urllib.parse import urljoin

FILE_SERVER_EXTERNAL_BASE_URL = settings.FILE_SERVER_EXTERNAL_BASE_URL

class FileServerStorage(Storage):

    def url(self, name):
        relative_path = "file?file={}".format(name)
        return urljoin(FILE_SERVER_EXTERNAL_BASE_URL, relative_path)

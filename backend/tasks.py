from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.conf import settings
from urllib.parse import urlparse

from selenium import webdriver
import tempfile
import base64
import requests
import os

PROXY_URL = settings.PROXY_URL
CELERY_TASKS_TOKEN = settings.CELERY_TASKS_TOKEN
VISIT_RESULT_URL = settings.VISIT_RESULT_URL
DEFAULT_FILE_STORAGE = settings.DEFAULT_FILE_STORAGE
if DEFAULT_FILE_STORAGE == "backend.storages.FileServerStorage":
    FILE_SERVER_INTERNAL_BASE_URL = settings.FILE_SERVER_INTERNAL_BASE_URL

@shared_task
def visit_url(url, ref):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    # Following two options are for Tor proxying
    proxy_url = PROXY_URL
    chrome_options.add_argument('--proxy-server={}'.format(proxy_url))
    proxy_host = urlparse(proxy_url).hostname
    chrome_options.add_argument(
      '--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE {}'.format(proxy_host))
    # Docker /dev/shm is too small, and Chrome does not really need it
    chrome_options.add_argument("--disable-dev-shm-usage")
    # --no-sandbox for Chrome, or crash in Debian Docker container
    # https://github.com/jessfraz/dockerfiles/issues/149
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)
    handle, path  = tempfile.mkstemp(suffix=".png")
    image_mime = "image/png"
    driver.save_screenshot(path)
    f = open(path, 'rb')
    binary_screenshot = f.read()
    f.close()
    os.remove(path) 

    headers = { "Authorization": "Token {}".format(
                                    CELERY_TASKS_TOKEN) }

    filename = ref + ".png"
    backend_url = VISIT_RESULT_URL + ref

    if DEFAULT_FILE_STORAGE == ("django.core.files"
                                ".storage.FileSystemStorage"):
        # Storing file in backend, just send it
        requests.put(backend_url, headers=headers,
                files={'screenshot': (filename, binary_screenshot, image_mime)})

    elif DEFAULT_FILE_STORAGE == "backend.storages.FileServerStorage":
        # Storing reference to file in backend, just send file name
        # ...but send it to file server before
        requests.post(FILE_SERVER_INTERNAL_BASE_URL,
                files={'file': (filename, binary_screenshot, image_mime)})
        requests.put(backend_url, headers=headers,
                data={'screenshot': filename})

    driver.close()

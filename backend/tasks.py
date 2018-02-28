from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.conf import settings
from urllib.parse import urlparse

from selenium import webdriver
import tempfile
import base64
import requests
import os

@shared_task
def visit_url(url, ref):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    # Following two options are for Tor proxying
    proxy_url = settings.PROXY_URL
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
    handle, path  = tempfile.mkstemp()
    driver.save_screenshot(path)
    f = open(path, 'rb')
    binary_screenshot = f.read()
    screenshot = base64.b64encode(binary_screenshot)
    f.close()
    os.remove(path) 

    headers = { "Authorization": "Token {}".format(
                                    settings.TORPEEKER_CELERY_TOKEN) }

    requests.put(settings.VISIT_RESULT_URL + ref, headers=headers,
                 json={'screenshot': str(screenshot, encoding="ascii")})

    driver.close()

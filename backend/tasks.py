from __future__ import absolute_import, unicode_literals
from celery import shared_task

from selenium import webdriver
import tempfile
import base64
import requests
import os

@shared_task
def visit_url(url, ref):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    # --no-sandbox for Chrome, or crash in Debian Docker container
    # https://github.com/jessfraz/dockerfiles/issues/149
    chrome_options.add_argument("no-sandbox")
    chrome_options.add_argument("window-size=1920x1080")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)
    handle, path  = tempfile.mkstemp()
    driver.save_screenshot(path)
    f = open(path, 'rb')
    binary_screenshot = f.read()
    screenshot = base64.b64encode(binary_screenshot)
    f.close()
    os.remove(path) 

    requests.put('http://localhost:8000/visit_result/' + ref,
                 json={'screenshot': str(screenshot, encoding="ascii")})

    driver.close()

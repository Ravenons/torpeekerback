from __future__ import absolute_import, unicode_literals
from celery import shared_task

from selenium import webdriver
import tempfile
import base64
import requests
import os

@shared_task
def visit_url(url, ref):

    driver = webdriver.PhantomJS()
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

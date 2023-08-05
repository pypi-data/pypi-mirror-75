import io

import requests
import base64
import os
from django.conf import settings
from django.core.files.storage import Storage
from django.core.files import File
from django.utils.deconstruct import deconstructible


@deconstructible
class ImageStorage(Storage):

    def __init__(self):
        self.option = settings.CUSTOM_STORAGE_OPTIONS

    def headers(self):
        token = self.option['token']
        headers = {'Authorization': 'Bearer {}'.format(token)}
        return headers

    def url(self, name):
        url = self.option['url']
        rc = requests.get(url + '/' + name, headers=self.headers())
        if rc.status_code != 200:
            return ''
        return rc.json()['url']

    def _open(self, name, mode='rb'):
        if self.exists(name):
            r = requests.get(self.url(name), headers=self.headers())
            return File(io.BytesIO(r.content), name)

    def _save(self, name, content):
        extension = os.path.splitext(name)[1][1:]
        assert extension in ['jpg', 'png'], 'Not allowed extension: {}'.format(extension)
        content_type = {'jpg': 'image/jpeg',
                        'png': 'image/png'}[extension]
        content = content.open('rb').read()
        url = self.option['url']
        rc = requests.post(url,
                           files={'content': (None, content, content_type), 'extension': (None, extension, 'text/plain')},
                           headers=self.headers())
        assert rc.status_code == 201, 'Bad response code: {}'.format(rc.status_code)
        new_name = rc.json()['id']
        return new_name

    def exists(self, name):
        return self.url(name) != ''

    def size(self, name):
        file = self.open(name)
        return file.size


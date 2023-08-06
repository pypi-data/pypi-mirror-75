__author__ = "Wytze Bruinsma"

import logging
import re
import sys
from dataclasses import dataclass, field
from io import BytesIO

import requests
from PIL import Image
from vaknl_gcp.Storage import StorageClient


@dataclass
class Acco:
    @dataclass
    class Image:
        url: str  # original url
        bucket_url: str = None  # bucket url
        width: int = None  # pixel with
        height: int = None  # pixel height
        bytes_size: int = None  # bytes size of image
        labels: list = field(default_factory=list)  # labels of the image
        descriptions: list = field(default_factory=list)  # descriptions of the image

    giataid: str
    source: str  # provider of the data
    images: list = field(default_factory=list)
    timestamp: str = None  # timestamp updated

    def __post_init__(self):
        if isinstance(self.giataid, int):
            self.giataid = str(self.giataid)

        if self.images:
            if not isinstance(self.images[0], Acco.Image):
                self.images = [Acco.Image(**image) for image in self.images]

    def basic_task(self):
        """
        Tasks are limited to 100KB
        So this is the bare minimum we need for a basic task
        :return:
        """
        return {
            'giataid': self.giataid,
            'source': self.source,
            'images': [{'url': image.url, 'descriptions': image.descriptions} for image in self.images]
        }


class ImageClient(object):

    def __init__(self, project_id):
        self.project_id = project_id
        self.storage_client = StorageClient(project=project_id)

    @staticmethod
    def get_image(image_url, auth=None, headers=None):
        for i in range(3):  # try 3 times if necessary
            try:
                response = requests.get(image_url, headers=headers, auth=auth)
                if response.status_code <= 204:
                    with BytesIO() as output:
                        # convert image to webp
                        with Image.open(BytesIO(response.content)).convert('RGB') as img:
                            img.save(output, 'webp')

                        file_name = get_file_name_form_url(image_url)
                        data = output.getvalue()
                        width, height = img.size
                        size = sys.getsizeof(data)

                        return file_name, width, height, size, data

            except Exception as e:
                logging.error(e)

        return None, None, None, None, None

    def upload_image_to_storage(self, id, bucket_name, image_url, auth=None):
        file_name, width, heigth, byte_size, image = self.get_image(image_url, auth)
        if image:
            bucket = self.storage_client.get_bucket(f'{bucket_name}-{self.project_id}')
            blob = bucket.blob(f"{id}/{file_name}")
            blob.upload_from_string(image)
            return width, heigth, byte_size, f'https://storage.cloud.google.com/{bucket.name}/{blob.name}'
        else:
            return None, None, None, None


def get_file_name_form_url(url):
    file_name = re.findall(r'(\w+)\.\w+$', url)
    if file_name:
        return file_name[0] + '.webp'
    else:
        return re.findall(r'\w+$', url)[0] + '.webp'

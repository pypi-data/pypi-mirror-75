# Vaknl
Package for working with Images. Contains the default Image dataclass and methods to get and upload images to gcp.

## Prerequisites
These modules dependant on two things. Firstly the vaknl-gcp package for working with GCP. 
Secondly the environment variable GOOGLE_CLOUD_PROJECT a.k.a. gcp project id. 

## Images

#### Class Acco with Images:
```python
@dataclass
class Acco:
    @dataclass
    class Image:
        url: str  # original url
        bucket_url: str = None  # bucket url
        width: int = None  # pixel with
        height: int = None  # pixel height
        bytes_size: int = None  # bytes size of image
        labels: list = []  # labels of the image
        descriptions: list = []  # descriptions of the image

    giataid: str
    source: str  # provider of the data
    images: list
    timestamp: str = None  # timestamp updated
```

#### get_image(image_url, auth=None):
Gets an images from the internet with a retry fall back of 3 times. 
```
returns width, heigth, size, data
```

#### upload_image_to_storage(id, bucket_name, image_url):
Gets images from the internet and uploads it to storage.
```
returns width, heigth, byte_size, blob_url
```
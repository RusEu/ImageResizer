import os
import requests
import settings
from StringIO import StringIO

from PIL import Image


def generate_name(filename, modified_time, size='', method=''):
    name = ".".join(filename.split('.')[:-1])
    ext = filename.split('.')[-1]
    filename = "_".join([name, modified_time, size, method]) + "." + ext
    return filename


def generate_image(url, full_path, size, method):
    try:
        response = requests.get(url)
        img = Image.open(StringIO(response.content))
        if size:
            size = size.split('x')
            size = (int(size[0]), int(size[1]))
            img.thumbnail(size, Image.ANTIALIAS)
        img.save(full_path)
        return True
    except Exception as e:
        print e
        return False


def get_or_create_file(app, full_path, modified_time, size=None, method=None):
    website = getattr(settings, app.upper())
    url = website + "/" + full_path
    route = full_path.split('/')
    route = route[1:] if route[0] == "" else route
    dir_route = "/".join(route[0:-1])
    filename = generate_name(route[-1], modified_time, size, method)
    full_path = full_path.replace(route[-1], filename)
    if os.path.exists(full_path):
        return dir_route, filename
    else:
        if not os.path.exists(dir_route):
            for i, directory in enumerate(route[:-1]):
                current_dir = "/".join(route[0:i + 1])
                if not os.path.exists(current_dir):
                    os.makedirs(current_dir)
        if generate_image(url, full_path, size, method):
            return dir_route, filename
        else:
            raise

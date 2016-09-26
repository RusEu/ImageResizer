import os
import requests
import settings
from StringIO import StringIO

from PIL import Image
from resizeimage import resizeimage


def generate_name(filename, size='', method=''):
    name = ".".join(filename.split('.')[:-1])
    ext = filename.split('.')[-1]
    filename = "_".join([name, size, method]) + "." + ext
    return filename


def generate_image(full_path, size, method):
    try:
        print full_path
        img = Image.open(full_path)
        if method:
            if size:
                size = size.split('x')
                size = (int(size[0]), int(size[1]))
                img = resizeimage.resize(method, img, size)
            img.save(full_path, img.format)
        return True
    except Exception as e:
        print e
        return False


def get_or_create_file(app, full_path, size=None, method=None):
    storage_route = getattr(settings, app.upper())
    full_path = storage_route + full_path
    route = full_path.split('/')
    route = route[1:] if route[0] == "" else route
    dir_route = "/".join(route[0:-1])
    filename = generate_name(route[-1], size, method)
    full_path = full_path.replace(route[-1], filename)
    if os.path.exists(full_path):
        return dir_route, filename
    else:
        if not os.path.exists(dir_route):
            for i, directory in enumerate(route[:-1]):
                current_dir = "/".join(route[0:i + 1])
                if not os.path.exists(current_dir):
                    os.makedirs(current_dir)
        if generate_image(full_path, size, method):
            return dir_route, filename
        else:
            raise

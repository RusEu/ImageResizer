import os
import settings

from PIL import Image
from resizeimage import resizeimage


def generate_name(filename, size='', method=''):
    name, ext = os.path.splitext(filename)
    filename = "_".join([name, size, method]) + ext
    return filename


def generate_image(file, output_file, size, method):
    try:
        img = Image.open(file)
        if method:
            if size:
                size = [int(s) for s in size.split('x')]
                if len(size) > 1:
                    size = (size[0], size[1])
                else:
                    size = size[0]
                img = resizeimage.resize(method, img, size)
            img.save(output_file, img.format)
        return True
    except Exception as e:
        print e
        return False


def get_or_create_file(app, file_path, size=None, method=None):
    storage_route = getattr(settings, app.upper())
    file_path = storage_route + file_path
    dir_route = os.path.dirname(file_path)
    directories = dir_route.split('/')
    directories = directories[1:] if directories[0] == "" else directories
    filename = os.path.basename(file_path)
    output_filename = generate_name(filename, size, method)
    output_file = file_path.replace(filename, output_filename)
    if os.path.exists(output_file):
        return dir_route, output_filename
    else:
        if not os.path.exists(dir_route):
            for i, directory in enumerate(directories):
                current_dir = "/".join(directories[0:i + 1])
                if not os.path.exists(current_dir):
                    os.makedirs(current_dir)
        if generate_image(file_path, output_file, size, method):
            return dir_route, output_filename
        else:
            raise

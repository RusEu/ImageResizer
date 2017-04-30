import os
import settings

from PIL import Image
from resizeimage import resizeimage


def generate_name(filename1, filename2, method,  width, height):
    name1, ext = os.path.splitext(filename1)
    name2, ext2 = os.path.splitext(filename2) if filename2 else None, None
    size = "{}x{}".format(width, height)
    filename = "{}_{}_{}_{}{}".format(name1, name2, size, method, ext)
    return filename


def generate_image(image1, image2, output_file, method, width, height):
    try:
        img = Image.open(image1)
        style_img = Image.open(image2) if image2 else None
        if method == "unite-resize":
            img_width = 0.4 * style_img.width
            img_pos = (150, int(img_width/2))
            img = resizeimage.resize_width(img, img_width)
            style_img.paste(img, img_pos, img)
            if width:
                style_img = resizeimage.resize_width(style_img, int(width))
            style_img.save(output_file, img.format)
        elif method == "resize":
            if width and height:
                size = [int(width), int(height)]
                img = resizeimage.resize_cover(img, size)
            elif width:
                img = resizeimage.resize_width(img, int(width))
            elif height:
                img = resizeimage.resize_height(img, int(height))
            img.save(output_file, img.format)
        return True
    except Exception as e:
        return False


def get_or_create_file(app, image1, image2, method, width, height):
    storage_route = getattr(settings, app.upper())

    file1_path = storage_route + image1
    file1_filename = os.path.basename(file1_path)

    file2_path, file2_filename = None, None

    if image2:
        file2_path = storage_route + image2
        file2_filename = os.path.basename(file2_path)

    dir_route = os.path.dirname(file1_path)
    directories = dir_route.split('/')
    directories = directories[1:] if directories[0] == "" else directories

    args = (file1_filename, file2_filename, method, width, height)
    output_filename = generate_name(*args)
    output_file = "{}/{}".format(dir_route, output_filename)

    if os.path.exists(output_file):
        return dir_route, output_filename
    else:
        if not os.path.exists(dir_route):
            for i, directory in enumerate(directories):
                current_dir = "/".join(directories[0:i + 1])
                if not os.path.exists(current_dir):
                    os.makedirs(current_dir)
        args = (file1_path, file2_path, output_file, method, width, height)
        if generate_image(*args):
            return dir_route, output_filename
    raise

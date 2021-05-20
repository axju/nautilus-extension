#!/usr/bin/env python3
import os
from pathlib import Path
from datetime import datetime
from filecmp import cmp

from PIL import Image

# This is the file format. You can change it if you like.
FINALE_FORMAT = '%Y-%m-%d_%H-%M-%S'

# A list of all file formats, the items can be,
# 1. a simple format string
# 2. a tuple with a format string and the length.
#    If the filename has some random chars after the format date
FILE_FORMATS = [
    'VID_%Y%m%d_%H%M%S',
    'IMG_%Y%m%d_%H%M%S',
    'VID%Y%m%d%H%M%S',
    (FINALE_FORMAT, 19),
    ('IMG-%Y%m%d-', 13),
]


def try_format(string, formats=FILE_FORMATS):
    """Try to get the datetime from the filename"""
    for item in formats:
        try:
            if isinstance(item, str):
                return datetime.strptime(string, item)
            elif isinstance(item, tuple):
                return datetime.strptime(string[:item[1]], item[0])
        except:
            pass
    return None


def try_meta(filename):
    """Try to get the datetime from the image meta data"""
    try:
        image = Image.open(filename)
        exifdata = image.getexif().get(36867)
        return datetime.strptime(exifdata, '%Y:%m:%d %H:%M:%S')
    except:
        return None


def get_filename(filename, dates):
    """
        Change the filename to the file format. The dates wil by in the list.
        The first thing that is not None is taken
    """
    for date in dates:
        if date:
            return filename.parent / str(date.strftime(FINALE_FORMAT) + filename.suffix)
    return filename


def check_copy(file, items):
    """return ture if file is new"""
    for item in items:
        if cmp(file, item):
            return False
    return True


def rename_file(filename):
    """Rename a single file"""
    file = Path(filename).resolve()
    filedate = datetime.fromtimestamp(file.stat().st_mtime)
    namedate = try_format(file.stem)
    metadate = try_meta(file)
    new_filename = get_filename(file, [metadate, filedate, namedate])

    old = list(file.parent.glob(new_filename.stem + '*'))
    if check_copy(file, old):
        new_filename = file.parent / '{}-{}{}'.format(new_filename.stem, len(old), new_filename.suffix)
        file.rename(new_filename)
    # Maybe you want to delete files that are duplicated?
    # elif try_format(file.name, [(FINALE_FORMAT, 19)]) is None:
    #     file.unlink()


def order_dir(path):
    """Rename all files in a directory"""
    work = Path(path).resolve()
    if not work.is_dir():
        return
    for file in work.iterdir():
        rename_file(file)


def main():
    """Main function that gets the paths from the nautilus variable."""
    for path_str in os.getenv('NAUTILUS_SCRIPT_SELECTED_FILE_PATHS', '').splitlines():
        path = Path(path_str).resolve()
        if path.is_file():
            rename_file(path)
        else:
            order_dir(path)


if __name__ == '__main__':
    main()

from pathlib import Path
import os
import hashlib

from flask import current_app
from PIL import Image


# def get_hash_md5(file_steam):
#     with Image.open(file_steam) as f:
#         m = hashlib.md5()
#         data = f.load()
#         m.update(data)
#         return m.hexdigest()


def save_photo_post(form_photo):
    photo_hash = hashlib.sha256(form_photo.filename.encode('utf-8')).hexdigest()
    # photo_hash = get_hash_md5(form_photo)
    _, f_ext = os.path.splitext(form_photo.filename)
    photo_file_title = f'{photo_hash}{f_ext}'
    photo_path = Path(current_app.root_path, str(Path('static', 'post_photos')), photo_file_title)

    i = Image.open(form_photo)
    i.save(photo_path)

    return photo_file_title

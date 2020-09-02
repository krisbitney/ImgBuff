import os
import typing
import uuid
from pathlib import Path

import numpy as np
from PIL import Image as Image
from fastai.vision import Image as FImage, image2np


async def save_image_to_buffer(img: FImage, fn: typing.IO):
    # save FastAI Image to disk/buffer
    x = image2np(img.data * 255).astype(np.uint8)
    Image.fromarray(x).save(fn, format='jpeg', quality=100)


async def save_image_to_disk(img: FImage, save_directory: Path) -> str:
    # get random filename (almost certain to be unique) and create filepath
    filename = str(uuid.uuid4()) + '.jpg'
    filepath = save_directory / filename
    while os.path.isfile(filepath):
        filename = str(uuid.uuid4()) + '.jpg'
        filepath = save_directory / filename
    # save FastAI Image to disk/buffer
    x = image2np(img.data * 255).astype(np.uint8)
    with open(filepath, 'wb') as file:
        Image.fromarray(x).save(file, format='jpeg', quality=85)
    return filename

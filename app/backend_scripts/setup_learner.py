from pathlib import Path
import aiohttp
import numpy as np
from PIL import Image as Image
from fastai.basic_train import Learner
from fastai.vision import Image as FImage, pil2tensor

from app.backend_scripts.build_nn import refresh_gan


async def setup_learner(download_url: str, target_dir: Path, target_fn: str, load_from_path: Path) -> Learner:
    await download_large_file(download_url, target_dir/target_fn, 4 * 1024 * 1024)
    try:
        learner = refresh_gan(load_from_path)
        return learner
    except RuntimeError as e:
        raise


async def download_large_file(url: str, filepath: Path, chunk_size: int):
    if filepath.exists():
        return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(filepath, 'wb') as f:
                    chunk = await response.content.read(chunk_size)
                    while chunk:
                        f.write(chunk)
                        chunk = await response.content.read(chunk_size)


async def colorize_image(neural_net, img: Image):
    # convert to grayscale if necessary
    if len(img.getbands()) > 1:
        img = img.convert('L')
    # process image with neural net
    fimg = FImage(pil2tensor(img, np.float32).div_(255))
    return neural_net.predict(fimg)[0]

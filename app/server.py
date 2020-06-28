import sys, typing, io, asyncio
import aiohttp
from pathlib import Path
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import Response, HTMLResponse
from PIL import Image as Image
from fastai.basic_train import Learner, load_learner
from fastai.vision import pil2tensor, image2np, Image as FImage
import numpy as np

import load_nn

# paths
path = Path(__file__).parent
colorizer_url = 'https://www.dropbox.com/s/vp5jrg12sz5x9i3/colorizer.pth?dl=1'
colorizer_fn = 'colorizer.pth'
load_path = Path('colorizer')

async def homepage(request: Request) -> Response:
    html_file = path / 'view' / 'index.html'
    return HTMLResponse(html_file.open().read())


async def setup_learner() -> Learner:
    await download_large_file(colorizer_url, path/colorizer_fn, 1024 * 1024)
    try:
        learner = load_nn.refresh_gan(load_path)
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


# set up colorizer neural net
colorizer = asyncio.run(setup_learner())


async def save_jpg(img: FImage, fn: typing.IO):
    # save FastAI Image to disk
    x = image2np(img.data * 255).astype(np.uint8)
    Image.fromarray(x).save(fn, format='jpeg', quality=100)

async def colorize_image(request: Request) -> Response:
    # get image
    content = await request.form()
    img_bytes = await content['image'].read()
    img = Image.open(io.BytesIO(img_bytes))
    # convert to grayscale if necessary
    if len(img.getbands()) > 1:
        img = img.convert('L')
    # process image with neural net
    fimg = FImage(pil2tensor(img, np.float32).div_(255))
    colorized_img = colorizer.predict(fimg)[0]
    # send response with colorized image
    buffer = io.BytesIO()
    await save_jpg(colorized_img, buffer)
    return Response(buffer.getvalue(), media_type='image/jpeg')


# app and routes
routes = [
    Route('/', homepage),
    Mount('/static', StaticFiles(directory=path/'static')),
    Mount('/resources', StaticFiles(directory=path/'resources')),
    Route('/colorizeImage', colorize_image, methods=['POST'])
]
app = Starlette(debug=True, routes=routes)


if __name__ == "__main__":
    if 'serve' in sys.argv:
        uvicorn.run(app, host='0.0.0.0', port=8000)

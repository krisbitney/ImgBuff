import sys, io, asyncio, json
from pathlib import Path
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import Response, HTMLResponse, PlainTextResponse
from PIL import Image as Image

# internal modules
from app.backend_scripts.setup_learner import setup_learner, colorize_image
from app.backend_scripts.ImageDatabase import ImageDatabase
from app.backend_scripts.util import save_image_to_buffer, save_image_to_disk

# paths
path = Path(__file__).parent
colorizer_url = 'https://www.dropbox.com/s/wcfgkllbsgam38r/colorizer_gan.pth?dl=1'
colorizer_fn = 'colorizer.pth'
load_path = path/'colorizer'
images_savepath = path/'images'

# set up colorizer neural net
colorizer = asyncio.run(setup_learner(colorizer_url, path, colorizer_fn, load_path))
# set up database
db = ImageDatabase()


async def homepage(request: Request) -> Response:
    html_file = path / 'view' / 'index.html'
    return HTMLResponse(html_file.open().read())


async def colorize_image_web(request: Request) -> Response:
    # get image
    content = await request.form()
    img_bytes = await content['image'].read()
    img = Image.open(io.BytesIO(img_bytes))
    # colorize image
    colorized_img = await colorize_image(colorizer, img)
    # send response with colorized image
    buffer = io.BytesIO()
    await save_image_to_buffer(colorized_img, buffer)
    return Response(buffer.getvalue(), media_type='image/jpeg')


# TODO: How do I make this secure? Need user authentication
async def colorize_image_mobile(request: Request) -> Response:
    user = request.path_params['username']
    # get image
    content = await request.form()
    img_bytes = await content['image'].read()
    img = Image.open(io.BytesIO(img_bytes))
    # colorize image
    colorized_img = await colorize_image(colorizer, img)
    # save colorized image
    saved_image_fn = await save_image_to_disk(colorized_img, images_savepath)
    image_url = request.url_for('image', filename=saved_image_fn)
    await db.insert_image(user, image_url)
    # send response as image url
    image_dict = await db.get_image(user, image_url)
    image_json = json.dumps(image_dict)
    print(image_json)
    return PlainTextResponse(image_json, media_type='application/json')


# TODO: How do I make this secure? Need user authentication
async def get_image_jpg(request: Request) -> Response:
    filename = request.path_params['filename']
    filepath = images_savepath/filename
    # TODO: handle IO exception
    with open(filepath, 'rb') as f:
        image_bytes = f.read()
    return Response(image_bytes, media_type='image/jpeg')


# TODO: How do I make this secure? Need user authentication
async def get_images_json(request: Request) -> Response:
    user = request.path_params['username']
    images_dict_list = await db.get_user_images(user)
    images_json = json.dumps(images_dict_list)
    return PlainTextResponse(images_json, media_type='application/json')


# app and routes
routes = [
    Route('/', homepage),
    Mount('/static', StaticFiles(directory=path/'static')),
    Mount('/resources', StaticFiles(directory=path/'resources')),
    Route('/colorizeImageWeb', colorize_image_web, methods=['POST']),
    Route('/colorizeImageMobile/{username}', colorize_image_mobile, methods=['POST']),
    Route('/image/{filename}', get_image_jpg, name='image', methods=['GET']),
    Route('/myImages/{username}', get_images_json, methods=['GET'])
]
app = Starlette(debug=True, routes=routes)


if __name__ == "__main__":
    if 'serve' in sys.argv:
        uvicorn.run(app, host='0.0.0.0', port=8000)

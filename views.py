import json
import time

from sanic import Blueprint, response
from jinja2 import Environment, PackageLoader, select_autoescape
from utils.common import saveInfoToMysql, base64ToNumpy
from utils.faceReg import faceReg

# jinja2 config

bp = Blueprint('views')
bp.static('/static', './static')
env = Environment(
    loader=PackageLoader('views', './template'),
    autoescape=select_autoescape(['html', 'xml', 'tpl']),
    enable_async=True)


async def template(tpl, **kwargs):
    template = env.get_template(tpl)
    rendered_template = await template.render_async(**kwargs)
    return response.html(rendered_template)


@bp.route("/")
async def index(request):
    return await template('index.html')


@bp.route("/takePhotos/", methods=['POST'])
async def takePhotos(request):
    app = request.app
    image = app.webcam.getImage()
    await app.redis_pool.zadd('imageInfo', int(time.time()), json.dumps(image))
    await app.redis_pool.expire('imageInfo', 60 * 10)

    return response.json({'status': 'success', 'image': image})


@bp.route("/subInfo/", methods=['POST', ])
async def subInfo(request):
    try:
        app = request.app
        res = await app.redis_pool.zrevrangebyscore('imageInfo', float('inf'), float('-inf'))
        data = request.json
        name = data.get('name')

        faceInfo = res[0].decode('utf-8')

        await saveInfoToMysql(pool=app.mysql_pool, name=name, faceInfo=faceInfo)
    except Exception as e:
        print(e)
        return response.json({'status': 'fail'})

    return response.json({'status': 'success'})


@bp.route("/reg/", methods=['POST', ])
async def reg(request):
    app = request.app

    npData = base64ToNumpy(app.webcam.getImage())

    res = await faceReg(pool=app.mysql_pool, npData=npData)

    return response.json({'status': 'success', 'msg': res})

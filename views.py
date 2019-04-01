from sanic import Blueprint, response
from jinja2 import Environment, PackageLoader, select_autoescape
from utils.common import saveInfo, faceReg, base64ToNumpy

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


@bp.route("/entry/", methods=['POST', ])
async def entry(request):
    try:
        data = request.json
        name = data.get('name')
        image = data.get('image').split(',')[-1]

        await saveInfo(name=name, image=image)
        msg = 'success'

    except Exception as e:
        msg = e.__str__()
    return response.json({'msg': msg})


@bp.route("/reg/", methods=['POST', ])
async def reg(request):
    try:
        data = request.json
        image = data.get('image').split(',')[-1]
        npData = base64ToNumpy(image)
    except Exception as e:
        msg = e.__str__()
    else:
        msg = await faceReg(npData)

    return response.json({'msg': msg})

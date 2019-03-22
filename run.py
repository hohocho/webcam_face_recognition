from sanic import Sanic

from views import bp
import aioredis
import aiomysql
from utils.webcam import Webcam
from settings import *

app = Sanic()
app.blueprint(bp)


@app.listener('before_server_start')
async def init(app, loop):
    '''
    Get the webcam object and initialize the database connection pool
    '''
    app.webcam = Webcam()
    app.redis_pool = await aioredis.create_redis_pool((REDIS_CONF['host'], REDIS_CONF['port']),
                                                      password=REDIS_CONF['password'], loop=loop)
    app.mysql_pool = await aiomysql.create_pool(host=MYSQL_CONF['host'], port=MYSQL_CONF['port'],
                                                user=MYSQL_CONF['user'], password=MYSQL_CONF['password'],
                                                db=MYSQL_CONF['db'])


@app.listener('after_server_stop')
async def close(app, loop):
    '''
    Release resources
    '''
    app.redis_pool.close()
    await app.redis_pool.wait_closed()
    app.mysql_pool.close()
    await app.mysql_pool.wait_closed()
    app.webcam.release()


app.run(host='0.0.0.0', port=8000)

import aiomysql
import base64
import numpy as np
import cv2


async def saveInfoToMysql(pool, name, faceInfo):
    sql = "INSERT INTO `faceReg`.`faceInfo` (`name`, `face`) VALUES ('{}', '{}')".format(
        name,
        faceInfo
    )
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sql)
            await conn.commit()


async def getFaceInfo(pool):
    sql = 'SELECT * FROM faceReg.faceInfo'
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sql)
            res = await cur.fetchall()
    return res


def base64ToNumpy(b64_code):
    '''
    Base64 to numpy array
    '''
    str_decode = base64.b64decode(b64_code.encode('utf-8'))
    img = cv2.imdecode(np.fromstring(str_decode, np.uint8), cv2.IMREAD_COLOR)
    return img


def cvToBase64(img):
    '''
    Numpy array to base64
    '''
    img_str = cv2.imencode('.jpg', img)[1].tostring()
    return base64.b64encode(img_str).decode('utf-8')

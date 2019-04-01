import cv2
import base64
import aiosqlite
import face_recognition

import numpy as np


async def saveInfo(name, image):
    sql = "INSERT INTO `main`.`face` (`name`, `faceInfo`) VALUES ('{}', '{}')".format(name, image)
    async with aiosqlite.connect('./face.db') as db:
        async with db.execute(sql):
            await db.commit()


async def getFaceInfo():
    sql = 'SELECT `name`, `faceInfo` FROM `main`.`face`'
    async with aiosqlite.connect('./face.db') as db:
        async with db.execute(sql) as cursor:
            res = await cursor.fetchall()
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


async def faceReg(npData):
    try:
        knownsEncode = []
        knownsInfo = []
        faceInfo = await getFaceInfo()

        for i in faceInfo:
            knownsInfo.append(i[0])
            knownFacesEncode = face_recognition.face_encodings(base64ToNumpy(i[1]))[0]
            knownsEncode.append(knownFacesEncode)

        unKnownFacesEncode = face_recognition.face_encodings(npData)[0]
        regRes = face_recognition.compare_faces(knownsEncode, unKnownFacesEncode)
        res = knownsInfo[regRes.index(True)]

    except:
        return 'Unknown Person!'

    return res

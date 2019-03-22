import face_recognition
from utils.common import getFaceInfo, base64ToNumpy
import json


async def faceReg(pool, npData):
    '''
    Face comparison by face_recognition
    '''
    try:
        knownsEncode = []
        knownsInfo = []
        faceInfo = await getFaceInfo(pool)
        for i in faceInfo:
            knownsInfo.append(i.get('name'))
            base64 = json.loads(i.get('face'))
            knownFacesEncode = face_recognition.face_encodings(base64ToNumpy(base64))[0]
            knownsEncode.append(knownFacesEncode)

        unKnownFacesEncode = face_recognition.face_encodings(npData)[0]
        regRes = face_recognition.compare_faces(knownsEncode, unKnownFacesEncode)
        res = knownsInfo[regRes.index(True)]
    except Exception as e:
        print(e)
        return 'Unknown Person!'

    return res

import jwt
import time

from oaback import settings


def get_user_id(t):
    """根据token得到当前用户user_id"""
    try:
        decode_data = jwt.decode(t, secret_key=settings.SECRET_KEY, verify=False, algorithms=['HS256'])
        print(decode_data)
        if int(decode_data['exp']) < int(time.time()):
            return "token过期"
        return decode_data['user_id']
    except Exception as e:
        return "token错误:\n"+str(e)


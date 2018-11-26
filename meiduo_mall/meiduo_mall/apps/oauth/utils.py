from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as TJSSerializer, BadData


def generate_save_user_token(openid):
    """
    使用用itsdangerous对原始的openid进行行行签名
    :param openid: 原始的openid
    :return: 签名后的openid
    """
    # 创建序列列化器器对象,指定秘钥和过期时间(10分钟)
    serializer = TJSSerializer(settings.SECRET_KEY, 600)
    # 准备原始的openid
    data = {'openid': openid}
    # 对openid进行行行签名,返回签名之后的bytes类型的字符串串
    token = serializer.dumps(data)
    # 将bytes类型的字符串串转成标准的字符串串,并返回
    return token.decode()


def check_save_token(access_token):
    """
    将access_token还原为openid
    :param access_token: 签名后的openid
    :return: 还原openid
    """
    serializer = TJSSerializer(settings.SECRET_KEY, 600)
    try:
        data = serializer.loads(access_token)
    except BadData:
        return None
    else:
        openid = data.get('openid')
        return openid

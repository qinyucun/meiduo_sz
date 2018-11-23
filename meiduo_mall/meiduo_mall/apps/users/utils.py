def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义我们的JWT返回数据
    :param token:
    :param user:
    :param request:
    :return:
    """
    return {
        'token': token,
        'user_id': user.user_id,
        'username': user.username
    }

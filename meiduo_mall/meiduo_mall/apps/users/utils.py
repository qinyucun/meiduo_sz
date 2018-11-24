import re

from django.contrib.auth.backends import ModelBackend
from .models import User


def get_user_by_account(account):
    try:
        if re.match('^1[3-9]\d{9}$', account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user


class UsernameMobileAuthBackend(ModelBackend):
    """
    修改用户认证系统的后端,支持多用户登陆
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """

        :param request:
        :param username: 就是默认的用户名,但是我们要修改扩展可以匹配手机号
        :param password:
        :param kwargs:
        :return:
        """
        user = get_user_by_account(username)
        if user and user.check_password(password):
            return user


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
        'id': user.id,
        'username': user.username
    }

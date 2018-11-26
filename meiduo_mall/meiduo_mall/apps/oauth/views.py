from django.conf import settings
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from QQLoginTool.QQtool import OAuthQQ
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from .utils import generate_save_user_token
from . import serializers
import logging

from rest_framework_jwt.settings import api_settings

from .models import OAuthQQUser

logger = logging.getLogger('django')


# url(r'^qq/user/$', views.QQAuthUserView.as_view()),
class QQAuthUserView(GenericAPIView):
    """用用户扫码登录的回调处理理"""

    def get(self, request):
        """
        1.提取code参数
        2.使用code向qq服务器请求access_token
        3.使用access_token向qq请求openid
        4.使用openid查询数据库查看是否绑定过
        5.如果已经绑定直接生成jwt
        6.如果没有绑定,创建用户并绑定
        :param request:
        :return:
        """
        code = request.query_params.get('code')
        if not code:
            return Response({'message': '缺少code'}, status=status.HTTP_400_BAD_REQUEST)
        # 创建OAuthQQ对像
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI)
        try:
            access_token = oauth.get_access_token(code)
            openid = oauth.get_open_id(access_token)
        except Exception as e:
            logger.info(e)
            return Response({'message': 'qq服务器异常'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        try:
            oauthqquser_model = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 没有绑定,加密后返回
            access_token_openid = generate_save_user_token(openid)
            return Response({'access_token': access_token_openid})
        else:  # 绑定了
            # 如果openid已绑定美多商城用用户,直接生生成JWT token,并返回
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            """获取关联的user"""
            user = oauthqquser_model.user
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response({'token': token,
                             'user_id': user.id,
                             'username': user.username
                             })

    def post(self, request):
        """使用openid绑定美多账户"""
        serializer = serializers.QQAuthUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # 生成JWT_token,并响应
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return Response({
            'token': token,
            'username': user.username,
            'user_id': user.id
        })


# url(r'^qq/authorization/$', views.QQAuthURLView.as_view())
class QQAuthURLView(APIView):
    """
    各种配置信息,请求qq服务器
    """

    def get(self, request):
        next = request.query_params.get('next')
        if not next:
            next = '/'
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI, state=next)
        login_url = oauth.get_qq_url()
        return Response({"login_url": login_url})

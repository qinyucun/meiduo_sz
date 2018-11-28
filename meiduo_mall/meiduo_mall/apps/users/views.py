from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView

from .serializers import CreateUserSerializer, UserDetailSerializer, EmailSerializer
from .models import User


class VerifyEmailView(APIView):
    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({'message': '缺少token'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.check_verify_email_url(token)
        if not user:
            return Response({'message': '无效的token'}, status=status.HTTP_400_BAD_REQUEST)
        # 修改email_active,完成验证
        user.email_active = True
        user.save()
        return Response({'message': 'OK'})


class EmailView(UpdateAPIView):
    """更新邮箱"""
    serializer_class = EmailSerializer  # 指定序列化器
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UsersDetailView(RetrieveAPIView):
    """用户详情"""
    serializer_class = UserDetailSerializer  # 指定序列化器
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# Create your views here.
class MobileCountView(APIView):
    """判断手机号是否已存在"""

    def get(self, request, mobile):
        # 查询数据库有有没有此手机号
        count = User.objects.filter(mobile=mobile).count()

        data = {
            'mobile': mobile,
            'count': count
        }
        return Response(data)


class UsernameCountView(APIView):
    """判断用户名是否已存在"""

    def get(self, request, username):
        # 查询数据库有有没有此用户名
        count = User.objects.filter(username=username).count()

        data = {
            'username': username,
            'count': count
        }
        return Response(data)


class UserView(CreateAPIView):
    """注册"""

    serializer_class = CreateUserSerializer

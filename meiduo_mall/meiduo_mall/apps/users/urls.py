from django.conf.urls import url
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from . import views

urlpatterns = [
    # 注册路由
    url(r'^users/$', views.UserView.as_view()),

    # 判断用户名是否已存在
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),

    # 判断手机号是否已存在
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
    url(r'^authorizations/$', obtain_jwt_token),
    url(r'^user/$', views.UsersDetailView.as_view()),
    url(r'^email/$', views.EmailView.as_view()),
    url(r'^emails/verification/$', views.VerifyEmailView.as_view()),
    url(r'^browse_histories/$', views.UserBrowseHistoryView.as_view()),

]

router = routers.DefaultRouter()
router.register(r'addresses', views.AddressViewSet, base_name='addresses')
urlpatterns += router.urls

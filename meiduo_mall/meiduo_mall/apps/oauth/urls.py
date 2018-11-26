from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^qq/authorization/$', views.QQAuthURLView.as_view()),
    # qq OAuth2.0 认证
    url(r'^qq/user/$', views.QQAuthUserView.as_view()),
]

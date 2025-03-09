from django.urls import path
from rest_framework_simplejwt.views import token_obtain_pair

from users import views

urlpatterns = [
    path('user/login/', token_obtain_pair, name='token_obtain_pair'),
    path("users/wx_auth/", views.WXAuthUserView.as_view(), name="wx_auth"),  # 微信认证
    path("users/", views.UserView.as_view(), name="user_info"),  # 用户信息
    path("top20_users/", views.GetTop20UserView.as_view(), name="user_top"),  # 用户信息
]

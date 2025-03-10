from django.urls import path
from rest_framework.routers import DefaultRouter

from community import views

urlpatterns = [
    # path('community/', views.CommunityViewSet.as_view()),
]
router = DefaultRouter()
router.register('community', views.CommunityViewSet, basename='community')
urlpatterns += router.urls

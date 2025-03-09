from django.urls import path
from rest_framework import routers

from words import views

urlpatterns = [
    # path('import_wordband/', views.ImportWordBandView.as_view()),
    path('get_word_detail/', views.GetWordDetailView.as_view()),
    path('learn_word/', views.LearningProcessView.as_view()),
    path('daily_record/', views.DailyRecordView.as_view()),
]
router = routers.DefaultRouter()
router.register('category', views.CategoryViewSet, basename='category')
router.register('word_band', views.WordBandViewSet, basename='word_band')
router.register('word_band_user', views.WordBandUserViewSet, basename='word_band_user')
router.register('word', views.WordViewSet, basename='word')
urlpatterns += router.urls

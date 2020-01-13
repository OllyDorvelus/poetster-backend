from django.urls import path, include

from rest_framework.routers import DefaultRouter

from poem import views

app_name = 'poem'

router = DefaultRouter()
router.register('genres', views.GenreViewSet)
router.register('categories', views.CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('poems', views.CreatePoemView.as_view(), name='poem-list')
]


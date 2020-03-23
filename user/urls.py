from django.urls import path

from user import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('me/', views.ManagaeUserView.as_view(), name='me')
]


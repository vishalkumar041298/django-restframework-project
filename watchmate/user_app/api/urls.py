from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from user_app.api.views import user_register, logout
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('register/', user_register, name='register'),
    path('logout/', logout, name='logout'),
    path('api/token/', TokenObtainPairView.as_view(), name='obtain-jwt'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh-token')
]
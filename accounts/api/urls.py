from django.urls import path, include
from .views import SignUpAPIView, SignInAPIView, CurrentUserAPIView, ChangePasswordAPIView, UpdateUserAPIView
from knox import views as knox_views

urlpatterns = [
    path('/auth/', include('knox.urls')),
    path('auth/register/', SignUpAPIView.as_view()),
    path('auth/login/', SignInAPIView.as_view()),
    path('auth/user/', CurrentUserAPIView.as_view()),
    path('auth/logout/', knox_views.LogoutView.as_view(), name="knox-logout"),
    path('auth/change-password/<str:pk>/', ChangePasswordAPIView.as_view(), name='auth-change-password'),
    path('auth/update-user/<str:pk>/', UpdateUserAPIView.as_view(), name='auth-update-user'),
]

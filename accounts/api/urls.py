from django.urls import path, include
from .views import SignUpAPIView, SignInAPIView, CurrentUserAPIView, ChangePasswordAPIView, UpdateUserAPIView, \
    RequestResetPasswordEmailAPIView, SetNewPasswordAPIView, CheckPasswordTokenAPIView, KnoxGoogleSocialLoginView
from knox import views as knox_views

urlpatterns = [
    path('/auth/', include('knox.urls')),
    path('auth/register/', SignUpAPIView.as_view()),
    path('auth/login/', SignInAPIView.as_view()),
    path('auth/user/', CurrentUserAPIView.as_view()),
    path('auth/logout/', knox_views.LogoutView.as_view(), name="knox-logout"),
    path('auth/change-password/<str:pk>/', ChangePasswordAPIView.as_view(), name='auth-change-password'),
    path('auth/request-reset-email/', RequestResetPasswordEmailAPIView.as_view(),
         name="request-reset-email"),
    path('auth/password-reset/<uidb64>/<token>/',
         CheckPasswordTokenAPIView.as_view(), name='password-reset-confirm'),
    path('auth/password-reset-complete', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),
    path('auth/update-user/<str:pk>/', UpdateUserAPIView.as_view(), name='auth-update-user'),
    path('auth/rest-auth/google_auth/', KnoxGoogleSocialLoginView.as_view(), name='google_login'),
]

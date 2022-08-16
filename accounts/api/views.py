from django.contrib.auth import get_user_model
from knox.settings import knox_settings
from rest_framework import generics
from rest_framework.response import Response
from knox.models import AuthToken
from .permissions import IsUser
from .serializers import CurrentUserSerializer, RegisterSerializer, LoginSerializer, ChangePasswordSerializer,\
    UpdateUserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.serializers import DateTimeField

User = get_user_model()


class BaseAuthSignAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny, ]

    def get_expiry_datetime_format(self):
        return knox_settings.EXPIRY_DATETIME_FORMAT

    def format_expiry_datetime(self, expiry):
        datetime_format = self.get_expiry_datetime_format()
        return DateTimeField(format=datetime_format).to_representation(expiry)


class SignUpAPIView(BaseAuthSignAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = AuthToken.objects.create(user)
        return Response({
            "user": CurrentUserSerializer(user, context=self.get_serializer_context()).data,
            "token": token[1],
            'expiry': self.format_expiry_datetime(token[0].expiry)
        })


class SignInAPIView(BaseAuthSignAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = AuthToken.objects.create(user)
        return Response({
            "user": CurrentUserSerializer(user, context=self.get_serializer_context()).data,
            "token": token[1],
            'expiry': self.format_expiry_datetime(token[0].expiry)
        })


class ChangePasswordAPIView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()
    permission_classes = [IsUser, ]


class UpdateUserAPIView(generics.UpdateAPIView):
    serializer_class = UpdateUserSerializer
    queryset = User.objects.all()
    permission_classes = [IsUser, ]


class CurrentUserAPIView(generics.RetrieveAPIView):
    serializer_class = CurrentUserSerializer

    def get_object(self):
        return self.request.user



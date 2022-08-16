from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.utils.translation import gettext_lazy as _
User = get_user_model()

error_messages = {
    "password_mismatch": _("The two password fields didn’t match."),
    "not_authorized": _("You are not authorized to complete this action"),
    "old_password": _("Old password is incorrect"),
    "invalid_login": _("Please enter a correct username and password")
}


class CurrentUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        exclude = ["password", "groups", "user_permissions"]

    @staticmethod
    def get_full_name(instance):
        return instance.get_full_name()


class PlayerSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["username", "full_name"]

    @staticmethod
    def get_full_name(instance):
        return instance.get_full_name()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(code=_("password_mismatch"), detail=error_messages["password_mismatch"])

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user_from_api(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
            validated_data['first_name'],
            validated_data['last_name']
        )
        user.dpc = True
        user.save()
        return user


# noinspection PyAbstractClass
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError(code=_("invalid_login"), detail=error_messages['invalid_login'])


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(code=_("password_mismatch"), detail=error_messages["password_mismatch"])
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(code=_("old_password"),  detail=error_messages['old_password'])
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user.pk != instance.pk:
            raise serializers.ValidationError(code=_("not_authorized"), detail=error_messages['not_authorized'])
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'gender', 'birth_date')

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError(code="not_authorized", detail=error_messages['not_authorized'])

        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.gender = validated_data['gender']
        instance.birth_date = validated_data['birth_date']

        instance.save()

        return instance

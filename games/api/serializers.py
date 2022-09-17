from django.contrib.auth import get_user_model
from rest_framework import serializers
from games.models import MultiplayerGame

User = get_user_model()


class PlayerSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["username", "full_name"]

    @staticmethod
    def get_full_name(instance):
        return instance.get_full_name()


class MultiplayerGameSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(read_only=True, many=True)
    created = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    completed = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")

    class Meta:
        model = MultiplayerGame
        fields = '__all__'

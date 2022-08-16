from rest_framework import serializers
from accounts.api.serializers import PlayerSerializer
from games.models import MultiplayerGame


class MultiplayerGameSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(read_only=True, many=True)
    created = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    completed = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")

    class Meta:
        model = MultiplayerGame
        fields = '__all__'

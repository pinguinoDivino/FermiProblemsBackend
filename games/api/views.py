from django.db.models import Count
from rest_framework.views import APIView
from games.api.serializers import MultiplayerGameSerializer
from games.models import MultiplayerGame
from rest_framework.response import Response


class StartMultiplayerGameApiView(APIView):
    def get(self, request):
        player = request.user
        params = request.query_params
        time_per_problems = int(params.get("time_per_problems"))
        number_of_problems = int(params.get("number_of_problems"))
        game = MultiplayerGame.objects.annotate(players_count=Count('players')).filter(is_started=False,
                                                                                       time_per_problems=time_per_problems,
                                                                                       number_of_problems=number_of_problems,
                                                                                       players_count=1).first()
        if not game:
            game = MultiplayerGame.objects.create(time_per_problems=time_per_problems, number_of_problems=number_of_problems,)
        game.players.add(player)
        serializer = MultiplayerGameSerializer(game)
        return Response(data=serializer.data)

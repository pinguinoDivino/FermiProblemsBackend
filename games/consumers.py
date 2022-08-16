from django.shortcuts import get_object_or_404
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
import datetime
from .decorators import UseMultiplayerGame
from django.db import transaction
from games.models import MultiplayerGame, PlayerInMultiplayerGame
from problems.models import Problem, UserAnswer
from games.utilities import model_to_dict

AVOID_DUPLICATES = True


class BaseGameConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.current_problem = None
        self.problem_ids = []

    async def is_user_authenticated(self):
        user = self.scope['user']

        if user is None or not user.is_authenticated:
            await self.close(code="User must be authenticated")
            return

    async def set_current_problem_and_get_obj(self):
        self.current_problem = await self.get_random_problem()

        return await self.get_obj_from_instance(self.current_problem)

    @database_sync_to_async
    def get_random_problem(self):
        problem_id = None
        problem = None
        while problem_id is None or (problem_id in self.problem_ids and AVOID_DUPLICATES):
            problem = Problem.objects.random()
            problem_id = problem.id
        else:
            self.problem_ids.append(problem.id)
            return problem

    @database_sync_to_async
    def get_problem_by_id(self, pk):
        return Problem.objects.get(pk=pk)

    @database_sync_to_async
    def get_obj_from_instance(self, instance):
        return model_to_dict(instance)

    @database_sync_to_async
    def add_answer(self, user, problem, **kwargs):
        return UserAnswer.objects.create(user=user, problem=problem, **kwargs)


class SoloGameConsumer(BaseGameConsumer):
    async def connect(self):
        await self.is_user_authenticated()

        await self.accept()

        obj = await self.set_current_problem_and_get_obj()

        await self.send_json({
            'type': 'problem',
            'content': obj
        })

    async def disconnect(self, close_code):
        self.current_problem = None
        self.problem_ids = []

    # Receive message from WebSocket

    async def receive_json(self, content, **kwargs):

        action = content['action']

        if action == 'user_answer':
            answer = await self.add_answer(user=self.scope['user'], problem=self.current_problem, **content['data'])

            if answer is None:
                await self.send_json({
                    'type': 'error',
                    'content': 'Risposta non salvata, verrà chiusa la sessione'
                })
                await self.close()
        elif action == "next_problem":
            obj = await self.set_current_problem_and_get_obj()

            await self.send_json({
                'type': 'problem',
                'content': obj
            })


class MultiplayerGameConsumer(BaseGameConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.game_group_name = None
        self.game_id = None
        self.game_number_of_problems = None
        self.game_time_per_problems = None
        self.current_turn = None
        self.is_in_time_out = False
        self.current_problem_starting_time = None

    async def connect(self):
        await self.is_user_authenticated()

        self.game_id = self.scope['url_route']['kwargs']['game_id']
        players_count = await UseMultiplayerGame(self.verify, self.game_id)()
        self.game_group_name = 'multiplayer_game_%s' % self.game_id

        await UseMultiplayerGame(self.initialize_game, self.game_id)()

        await self.channel_layer.group_add(
            self.game_group_name,
            self.channel_name
        )
        await self.accept()

        if players_count == 2:
            await UseMultiplayerGame(self.set_game_started, self.game_id)()
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'starting'
                }
            )
            obj = await self.set_current_problem_and_get_obj()
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'problem',
                    'content': obj
                }
            )
        else:
            await self.send_json({
                'type': 'WAITING'
            })

    async def disconnect(self, close_code):
        game = await database_sync_to_async(get_object_or_404)(MultiplayerGame, pk=self.game_id)
        content = None
        if game.is_started:
            winner = await UseMultiplayerGame(self.get_other_player, self.game_id)(user=self.scope['user'])
            content = winner.username
            await UseMultiplayerGame(self.game_over_by_disconnect, self.game_id)(winner=winner)
        else:
            await UseMultiplayerGame(self.delete_game, self.game_id)()

        await self.channel_layer.group_send(
            self.game_group_name,
            {
                'type': 'ending',
                'content': content
            }
        )

        await self.channel_layer.group_discard(
            self.game_group_name,
            self.channel_name
        )

    # Receive message from WebSocket

    async def receive_json(self, content, **kwargs):
        user = self.scope['user']

        action = content['action']

        if self.is_in_time_out:
            await UseMultiplayerGame(self.reset_time_out_counter, self.game_id)()
            self.is_in_time_out = False

        if action == 'user_answer':

            if not self.validate_user_answer():
                await self.send_json({
                    'type': 'error',
                    'content': 'Risposta inviata in ritardo, verrà chiusa la sessione'
                })
                await self.close()
                return

            answer = await self.add_answer(user=user, problem=self.current_problem, **content['data'])

            if answer is None:
                await self.send_json({
                    'type': 'error',
                    'content': 'Risposta non salvata, verrà chiusa la sessione'
                })
                await self.close()
                return

            payload = {
                "header": self.current_problem.id,
                "content": {
                    "time_out": False,
                    "id": answer.id,
                    "value": answer.value,
                    "correct_value": self.current_problem.value
                }
            }
            await UseMultiplayerGame(self.update_log, self.game_id)(text=payload)

            if self.current_turn == user:
                await self.call_new_problem()
            else:
                other_player = await UseMultiplayerGame(self.get_other_player, self.game_id)(user=user)
                await self.send_json({
                    'type': 'waiting',
                    'content': 'In attesa dello sfidante'
                })
                await self.channel_layer.group_send(
                    self.game_group_name,
                    {
                        'type': 'turn',
                        'content': other_player
                    }
                )

        if action == 'time_out':

            payload = {
                "header": self.current_problem.id,
                "content": {
                    "time_out": True
                }
            }

            await UseMultiplayerGame(self.update_log, self.game_id)(text=payload)

            if self.current_turn:
                await self.call_new_problem()
                return
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'timeout',
                }
            )

    # Receive message from room group
    async def starting(self, event):
        await self.send_json(content={
            'type': 'starting'
        })

    async def ending(self, event):
        await self.send_json(content={
            'type': 'ending',
            'content': event['content']
        })

    async def problem(self, event):
        content = event['content']
        self.current_problem = await self.get_problem_by_id(content['id'])
        if content['id'] not in self.problem_ids:
            self.problem_ids.append(content['id'])
        # Send message to WebSocket
        await self.send_json(content={
            'type': 'problem',
            'content': content
        })
        self.current_turn = None
        self.current_problem_starting_time = datetime.datetime.now()

    async def turn(self, event):
        content = event['content']
        self.current_turn = content

    async def timeout(self, event):
        counter = await UseMultiplayerGame(self.increment_time_out_counter, obj_id=self.game_id)()
        if counter == 1 and not self.is_in_time_out:
            self.is_in_time_out = True
            await self.call_new_problem()

    # Methods

    def validate_user_answer(self):
        return (datetime.datetime.now() - self.current_problem_starting_time).total_seconds() < self.game_time_per_problems

    async def verify(self, *args, **kwargs):
        if args[0].is_started:
            await self.close(code="The game has already started!")
            return

        players_count = await UseMultiplayerGame(self.get_players_count, self.game_id)()

        if players_count > 2 \
                or not self.check_if_player_in_game(game=args[0], player=self.scope['user']):
            await self.close(code="This game already has enough participants. Try joining another")
            return

        return players_count

    async def initialize_game(self, *args, **kwargs):
        self.game_number_of_problems = args[0].number_of_problems
        self.game_time_per_problems = args[0].time_per_problems

    async def call_new_problem(self):
        if len(self.problem_ids) >= self.game_number_of_problems:
            await self.set_winner()  # TODO è il posto giusto?
            return
        obj = await self.set_current_problem_and_get_obj()
        await self.channel_layer.group_send(
            self.game_group_name,
            {
                'type': 'problem',
                'content': obj
            }
        )

    async def set_winner(self):
        winner = await UseMultiplayerGame(self.game_over, self.game_id)()
        await self.channel_layer.group_send(
            self.game_group_name,
            {
                'type': 'ending',
                'content': winner.username
            }
        )

    @database_sync_to_async
    @transaction.atomic
    def increment_time_out_counter(self, *args, **kwargs):
        game = MultiplayerGame.objects.filter(id=self.game_id).select_for_update().first()
        counter = game.increment_time_out_counter()
        return counter

    @database_sync_to_async
    def reset_time_out_counter(self, *args, **kwargs):
        args[0].reset_time_out_counter()

    @database_sync_to_async
    def get_players_count(self, *args, **kwargs):
        return args[0].players.count()

    @database_sync_to_async
    def check_if_player_in_game(self, *args, **kwargs):
        return kwargs.get('player') in kwargs.get('game').players.all()

    @database_sync_to_async
    def set_game_started(self, *args, **kwargs):
        args[0].start_game()

    @database_sync_to_async
    def update_log(self, log, user_answer):
        log.update(user_answer)

    @database_sync_to_async
    def get_other_player(self, *args, **kwargs):
        player = PlayerInMultiplayerGame.objects.filter(game=args[0]).exclude(user=kwargs.get('user')).first()
        return player.user

    @database_sync_to_async
    def delete_game(self, *args, **kwargs):
        args[0].delete()

    @database_sync_to_async
    def game_over(self, *args, **kwargs):
        return args[0].set_winner(self.problem_ids)

    @database_sync_to_async
    def game_over_by_disconnect(self, *args, **kwargs):
        args[0].mark_complete(winner=kwargs.get('winner'))

    @database_sync_to_async
    def update_log(self, *args, **kwargs):
        game = args[0]
        game.update_log(user=self.scope['user'], **kwargs)

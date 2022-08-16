from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from games.services.utilitis import calculate_score_from_logs

User = get_user_model()


class MultiplayerGame(models.Model):
    players = models.ManyToManyField(
        User, related_name='multiplayer_games', verbose_name=_("giocatori"),
        through='PlayerInMultiplayerGame',
        through_fields=('game', 'user'),
    )
    completed = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    is_started = models.BooleanField(_('iniziato?'), default=False)
    time_out_counter = models.IntegerField(default=0)

    time_per_problems = models.IntegerField(_("tempo per domanda (secondi)"), default=60)

    number_of_problems = models.IntegerField(_("numero di problemi"), default=5)

    objects = models.Manager()

    class Meta:
        db_table = 'multiplayer_games'
        verbose_name = 'Partita multigiocatore'
        verbose_name_plural = 'Partite multigiocatore'

    def __str__(self):
        return 'Game #{0}'.format(self.pk)

    def start_game(self):
        self.isStarted = True
        for user in self.players.all():
            MultiplayerGameLog.objects.create(game=self, player=user)
        self.save()

    def increment_time_out_counter(self):
        self.time_out_counter = self.time_out_counter + 1
        self.save()
        return self.time_out_counter

    def reset_time_out_counter(self):
        self.time_out_counter = 0
        self.save()
        return self.time_out_counter

    def update_log(self, text, user):
        """
        Adds a text log associated with this game.
        """
        log = MultiplayerGameLog.objects.get(game=self, player=user)
        log.update(text=text)

    def set_winner(self, problem_ids):
        logs = MultiplayerGameLog.objects.filter(game=self)
        winner = calculate_score_from_logs(logs, problem_ids)
        self.mark_complete(winner)
        return winner

    def mark_complete(self, winner):
        """
        Sets a game to completed status and records the winner
        """
        self.completed = timezone.now()
        self.save()

        w = PlayerInMultiplayerGame.objects.get(game=self, user=winner)
        w.type = "Winner"
        w.save()

        losers = PlayerInMultiplayerGame.objects.filter(game=self).exclude(user=winner)
        for loser in losers:
            loser.type = "Loser"
            loser.save()

    def get_winner(self):
        player = PlayerInMultiplayerGame.objects.filter(game=self, type="Winner").first()
        if player:
            return player.user
        return None


class PlayerInMultiplayerGame(models.Model):
    WINNER = 'Winner'
    LOSER = 'Loser'
    UKNOWN = 'Unknown'
    PLAYER_TYPE_CHOICES = [
        (WINNER, 'Winner'),
        (LOSER, 'Loser'),
        (UKNOWN, 'Unknown')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('giocatore'))
    game = models.ForeignKey(MultiplayerGame, on_delete=models.CASCADE)
    type = models.CharField(choices=PLAYER_TYPE_CHOICES, max_length=10)

    objects = models.Manager()

    class Meta:
        db_table = 'player_in_multiplayer_games'
        verbose_name = 'Utente in gioco'
        verbose_name_plural = 'Utente in gioco'

    def __str__(self):
        return 'Giocatore #{1} nella sfida #{0}'.format(self.pk, self.game.id)


class MultiplayerGameLog(models.Model):
    game = models.ForeignKey(MultiplayerGame, related_name="logs", on_delete=models.CASCADE, verbose_name=_('partita'))
    text = models.JSONField(null=True, blank=True, default=dict)
    player = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        db_table = 'multiplayer_game_logs'
        verbose_name = 'Log partita multiplayer'
        verbose_name_plural = 'Logs partite multiplayer'

    def __str__(self):
        return 'Game #{0} Log di {1}'.format(self.game.id, self.player.get_full_name())

    def update(self, text):
        if str(text['header']) in list(self.text.keys()):
            self.text[str(text['header'])].append(text['content'])
        else:
            self.text[str(text['header'])] = [text['content'], ]
        self.save()

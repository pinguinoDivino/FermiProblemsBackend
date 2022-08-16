from django.contrib import admin
from .models import MultiplayerGame, MultiplayerGameLog, PlayerInMultiplayerGame
# Register your models here.


class MultiplayerGameAdmin(admin.ModelAdmin):

    def get_players(self, obj):
        return ", ".join([p.get_full_name() for p in obj.players.all()])

    def get_winner(self, obj):
        if obj.get_winner():
            return obj.get_winner().get_full_name()
        else:
            return 'Non disponibile'

    get_players.short_description = "Giocatori"

    get_winner.short_description = "Vincitore"

    readonly_fields = ['get_players', 'created', 'get_winner']

    list_display = ['id', 'created', 'completed', 'get_players', 'get_winner']


class PlayerInMultiplayerGameAdmin(admin.ModelAdmin):
    pass


class MultiplayerGameLogAdmin(admin.ModelAdmin):
    pass


admin.site.register(MultiplayerGame, MultiplayerGameAdmin)
admin.site.register(PlayerInMultiplayerGame, PlayerInMultiplayerGameAdmin)
admin.site.register(MultiplayerGameLog, MultiplayerGameLogAdmin)
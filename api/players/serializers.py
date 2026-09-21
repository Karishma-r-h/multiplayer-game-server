from rest_framework import serializers
from .models import Player, Match

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["id", "username", "wins", "losses", "created_at"]


class MatchSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)
    winner = PlayerSerializer(read_only=True)

    class Meta:
        model = Match
        fields = ["id", "match_id", "winner", "players", "started_at", "ended_at"]
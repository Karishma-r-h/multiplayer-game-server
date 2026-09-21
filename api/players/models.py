from django.db import models

class Player(models.Model):
    username = models.CharField(max_length=50, unique=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Match(models.Model):
    match_id = models.CharField(max_length=100, unique=True)
    winner = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, related_name="matches_won")
    players = models.ManyToManyField(Player, related_name="matches_played")
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.match_id
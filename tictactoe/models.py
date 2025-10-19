from django.db import models
import json

class Player(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class GameResult(models.Model):
    player_x = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_x_games')
    player_o = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_o_games')
    board = models.TextField(default=json.dumps([""]*9))
    current_turn = models.CharField(max_length=1, default='X')
    winner = models.CharField(max_length=1, choices=[('X','X'),('O','O'),('D','Draw')], blank=True, null=True)
    vs_bot = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.player_x} vs {self.player_o} - {self.winner or 'In progress'}"

    def get_board(self):
        return json.loads(self.board)

    def set_board(self, board_list):
        self.board = json.dumps(board_list)

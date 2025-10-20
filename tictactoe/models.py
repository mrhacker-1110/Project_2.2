from django.db import models
import json

class Player(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class GameResult(models.Model):
    player_x = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="as_x")
    player_o = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="as_o")
    board = models.TextField(default=json.dumps([""] * 9))
    current_turn = models.CharField(max_length=1, default="X")
    winner = models.CharField(max_length=1, choices=[("X","X"),("O","O"),("D","Draw")], blank=True, null=True)
    vs_bot = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.player_x} vs {self.player_o} – {self.winner or 'In progress'}"

    def get_board(self):
        return json.loads(self.board)

    def set_board(self, board_list):
        self.board = json.dumps(board_list)

    # ---------- метод для проверки победителя ----------
    def check_winner(self):
        b = self.get_board()
        WIN_COMBOS = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6],
        ]
        for a,b_,c in WIN_COMBOS:
            if b[a] == b[b_] == b[c] != "":
                return b[a]
        if "" not in b:
            return "D"
        return None

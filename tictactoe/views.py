import random
import time
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Player, GameResult


def index(request):
    games = GameResult.objects.all().order_by("-id")
    return render(request, "tictactoe/index.html", {"games": games})


def new_game(request):
    if request.method == "POST":
        px = request.POST.get("player_x")
        po = request.POST.get("player_o")
        vs_bot = request.POST.get("vs_bot") == "on"

        player_x, _ = Player.objects.get_or_create(name=px)
        if vs_bot:
            player_o, _ = Player.objects.get_or_create(name="Bot")
        else:
            player_o, _ = Player.objects.get_or_create(name=po or "Guest")

        game = GameResult.objects.create(
            player_x=player_x, player_o=player_o, vs_bot=vs_bot
        )
        return redirect("play_game", game_id=game.id)

    return render(request, "tictactoe/new_game.html")


def play_game(request, game_id):
    game = get_object_or_404(GameResult, id=game_id)
    board = game.get_board()

    # --------------------------------------------
    # 1️⃣ Ход игрока (или второго человека)
    # --------------------------------------------
    if request.method == "POST" and not game.winner:
        cell_idx = request.POST.get("cell")
        if cell_idx is not None:
            idx = int(cell_idx)

            if board[idx] == "":
                # Ход текущего игрока (X или O)
                board[idx] = game.current_turn
                game.set_board(board)
                game.winner = game.check_winner()

                # Если нет победителя — меняем очередь
                if not game.winner:
                    game.current_turn = "O" if game.current_turn == "X" else "X"

                game.save()

                # Если играет против бота — бот отвечает сам
                if game.vs_bot and game.current_turn == "O" and not game.winner:
                    empty = [i for i, v in enumerate(board) if v == ""]
                    if empty:
                        time.sleep(0.5)
                        move = random.choice(empty)
                        board[move] = "O"
                        game.set_board(board)
                        game.winner = game.check_winner()
                        if not game.winner:
                            game.current_turn = "X"
                        game.save()

                return redirect("play_game", game_id=game.id)

    # --------------------------------------------
    # 2️⃣ Формируем 3×3 сетку для шаблона
    # --------------------------------------------
    rows = []
    for i in range(3):
        row = []
        for j in range(3):
            idx = i * 3 + j
            row.append((idx, board[idx]))
        rows.append(row)

    context = {
        "game": game,
        "rows": rows,
    }
    return render(request, "tictactoe/play_game.html", context)


def results(request):
    games = GameResult.objects.exclude(winner__isnull=True)
    return render(request, 'tictactoe/results.html', {'games': games})


def clear_all(request):
    from .models import GameResult, Player
    GameResult.objects.all().delete()
    Player.objects.all().delete()
    return redirect('index')

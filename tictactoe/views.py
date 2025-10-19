from django.shortcuts import render, redirect, get_object_or_404
from .models import Player, GameResult
import random

WIN_COMBOS = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
]

def index(request):
    games = GameResult.objects.all()
    return render(request, 'tictactoe/index.html', {'games': games})

def new_game(request):
    if request.method == 'POST':
        player_x_name = request.POST.get('player_x')
        player_o_name = request.POST.get('player_o')
        vs_bot = request.POST.get('vs_bot') == 'on'

        player_x, _ = Player.objects.get_or_create(name=player_x_name)
        if vs_bot:
            player_o, _ = Player.objects.get_or_create(name="Bot")
        else:
            player_o, _ = Player.objects.get_or_create(name=player_o_name)

        game = GameResult.objects.create(player_x=player_x, player_o=player_o, vs_bot=vs_bot)
        return redirect('play_game', game_id=game.id)

    return render(request, 'tictactoe/new_game.html')

def play_game(request, game_id):
    game = get_object_or_404(GameResult, id=game_id)
    board = game.get_board()

    def check_winner(b):
        for combo in WIN_COMBOS:
            if b[combo[0]] == b[combo[1]] == b[combo[2]] != "":
                return b[combo[0]]
        if "" not in b:
            return "D"
        return None

    # Ход игрока
    if request.method == 'POST' and not game.winner:
        cell = int(request.POST.get('cell'))
        if board[cell] == "":
            board[cell] = game.current_turn
            winner = check_winner(board)
            if winner:
                game.winner = winner
            else:
                game.current_turn = 'O' if game.current_turn == 'X' else 'X'
            game.set_board(board)
            game.save()

    # Ход бота
    if game.vs_bot and not game.winner and game.current_turn == 'O':
        empty_cells = [i for i, v in enumerate(board) if v == ""]
        if empty_cells:
            bot_move = random.choice(empty_cells)
            board[bot_move] = 'O'
            winner = check_winner(board)
            if winner:
                game.winner = winner
            else:
                game.current_turn = 'X'
            game.set_board(board)
            game.save()

    # Формируем таблицу 3x3 с индексами
    rows = []
    for i in range(3):
        row = []
        for j in range(3):
            idx = i*3 + j
            row.append((idx, board[idx]))
        rows.append(row)

    return render(request, 'tictactoe/play_game.html', {'game': game, 'rows': rows})


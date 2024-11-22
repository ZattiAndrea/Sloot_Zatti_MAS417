import berserk
import chess.pgn
import io

def count_moves(pgn_string):
    pgn = io.StringIO(pgn_string)
    game = chess.pgn.read_game(pgn)
    moves_count = 0

    for move in game.mainline_moves():
        moves_count += 1

    return moves_count

class ChessAnalyzer:
    def __init__(self, token):
        self.session = berserk.TokenSession(token)
        self.client = berserk.Client(self.session)

    def get_games(self, player1, player2, max_games=100):
        games = self.client.games.export_by_player(player1, vs=player2, max=max_games)
        return games

    def get_game_details(self, game_id):
        game = self.client.games.export(game_id=game_id)
        return game['moves']

    def analyze_moves(self, moves, stop_at_move):
        pgn = chess.pgn.read_game(io.StringIO(moves))
        board = pgn.board()
        move_count = 0
        for move in pgn.mainline_moves():
            if move_count == stop_at_move:
                break
            board.push(move)
            move_count += 1
        return board.fen()

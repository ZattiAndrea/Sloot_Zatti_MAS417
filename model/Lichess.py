import berserk
import chess.pgn
import io

def count_moves(pgn_string):
    """
        Counts the total number of moves in a PGN (Portable Game Notation) string.
        Args:
            pgn_string (str): The PGN string representing a chess game.
        Returns:
            int: The total number of moves in the mainline of the game.
    """
    pgn = io.StringIO(pgn_string)
    game = chess.pgn.read_game(pgn)
    moves_count = 0

    for move in game.mainline_moves():
        moves_count += 1

    return moves_count

class ChessAnalyzer:
    def __init__(self, token):
        """
                Initializes the ChessAnalyzer with an authentication token for the Lichess API.
                Args:
                    token (str): Lichess API token for authentication.
                Attributes:
                    session (berserk.TokenSession): A session object authenticated with the token.
                    client (berserk.Client): A client object for interacting with the Lichess API.
        """
        self.session = berserk.TokenSession(token)
        self.client = berserk.Client(self.session)

    def get_games(self, player1, player2, max_games=100):
        """
                Fetches games played between two players from Lichess.
                Args:
                    player1 (str): Lichess username of the first player.
                    player2 (str): Lichess username of the second player.
                    max_games (int, optional): Maximum number of games to retrieve. Defaults to 100.
                Returns:
                    iterator: An iterator of game objects retrieved from Lichess.
        """
        games = self.client.games.export_by_player(player1, vs=player2, max=max_games)
        return games

    def get_game_details(self, game_id):
        """
                Retrieves the details of a specific game from Lichess by its ID.
                Args:
                    game_id (str): The unique identifier for the game on Lichess.
                Returns:
                    str: A string of moves in PGN format.
        """
        game = self.client.games.export(game_id=game_id)
        return game['moves']

    def analyze_moves(self, moves, stop_at_move):
        """
                Analyzes the board's position after a specific number of moves in a chess game.
                Args:
                    moves (str): A string of moves in PGN format.
                    stop_at_move (int): The move number to stop at and analyze the board's position.
                Returns:
                    str: The FEN (Forsyth-Edwards Notation) string representing the board's position.
        """
        pgn = chess.pgn.read_game(io.StringIO(moves))
        board = pgn.board()
        move_count = 0
        for move in pgn.mainline_moves():
            if move_count == stop_at_move:
                break
            board.push(move)
            move_count += 1
        return board.fen()



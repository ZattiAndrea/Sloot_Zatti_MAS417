import cloudscraper
import chess.pgn
import io
import requests

scraper = cloudscraper.create_scraper()

def get_games_between_players(player1, player2):
    """
        Retrieves all chess games played between two players from Chess.com.
        Args:
            player1 (str): The username of the first player on Chess.com.
            player2 (str): The username of the second player on Chess.com.
        Returns:
            list: A list of game objects (dict) where the specified players played against each other.
        Workflow:
            - Fetches the archive of games for player1 from Chess.com.
            - Iterates through the archives to find games where player2 participated.
            - Adds matching games to the result list.
    """
    games_between = []

    archives_response = scraper.get(f"https://api.chess.com/pub/player/{player1}/games/archives")
    if archives_response.status_code != 200:
        print("Error obtaining archives.")
        return []

    archives = archives_response.json().get("archives", [])

    for archive_url in archives:
        games_response = scraper.get(archive_url)
        if games_response.status_code != 200:
            print(f"Error retrieving games from archive: {archive_url}")
            continue

        games = games_response.json().get("games", [])
        for game in games:
            if game["white"]["username"].lower() == player2.lower() or game["black"]["username"].lower() == player2.lower():
                games_between.append(game)

    return games_between

def analyze_game_and_get_fen(moves_pgn, stop_at_move):
    """
        Analyzes a game in PGN format and returns the board's FEN after a specific number of moves.
        Args:
            moves_pgn (str): The PGN string representing the game moves.
            stop_at_move (int): The move number to stop at and analyze the board position.
        Returns:
            str: The FEN string representing the board's position after the specified number of moves.
        Workflow:
            - Parses the PGN string to create a game object.
            - Iterates through the moves and updates the board.
            - Stops after the specified number of moves and returns the resulting FEN.
    """
    pgn = chess.pgn.read_game(io.StringIO(moves_pgn))
    board = pgn.board()
    moves_count = 0

    for move in pgn.mainline_moves():
        if moves_count == stop_at_move:
            break
        board.push(move)
        moves_count += 1

    return board.fen()

def analyze_game_and_get_moves_by_id(game_id):
    """
        This function is used for the GUI so it is not properly needed for the main project
    """
    url = f"https://www.chess.com/callback/live/game/{game_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        game_data = response.json()
        move_list = game_data.get("game", {}).get("moveList", "")
        return game_data
    except requests.exceptions.HTTPError as http_err:
        print(f"Errore HTTP: {http_err}")
    except Exception as err:
        print(f"Errore: {err}")





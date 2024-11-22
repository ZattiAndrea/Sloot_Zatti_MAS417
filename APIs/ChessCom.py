import cloudscraper
import chess.pgn
import io

scraper = cloudscraper.create_scraper()

def get_games_between_players(player1, player2):
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
    pgn = chess.pgn.read_game(io.StringIO(moves_pgn))
    board = pgn.board()
    moves_count = 0

    for move in pgn.mainline_moves():
        if moves_count == stop_at_move:
            break
        board.push(move)
        moves_count += 1

    return board.fen()


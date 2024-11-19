from APIs.ChessCom import get_games_between_players, analyze_game_and_get_fen
from APIs.Lichess import ChessAnalyzer, count_moves

def lichess_API():
    token = 'lip_vSJWl0oP0i4PQzxhZa3h'
    analyzer = ChessAnalyzer(token)

    games_list = []

    while not games_list:
        player1 = input("Choose the white player (or type 'exit' to quit): ")
        if player1.lower() == "exit":
            print("Exit from the program.")
            return

        player2 = input("Choose the black player (or type 'exit' to quit): ")
        if player2.lower() == "exit":
            print("Exit from the program.")
            return

        try:
            games = analyzer.get_games(player1, player2)
            games_list = list(games)

            if games_list:
                print(f"Found {len(games_list)} games between {player1} and {player2}.")
            else:
                print(f"No games found between {player1} and {player2}. Please try again.")
        except Exception as e:
            print(f"Error during the request: {e}")
            print("Please try again with valid names.")

    while True:
        try:
            game_number = int(input("Choose the game number: "))
            if game_number < 0 or game_number >= len(games_list):
                print(f"Error: the number must be positive and not larger than {len(games_list)}.")
            else:
                break
        except ValueError:
            print("Error: please enter a valid numeric value.")

    game_id = games_list[game_number]['id']
    moves = analyzer.get_game_details(game_id)
    link = (f"https://lichess.org/{game_id}")
    print(link)
    print(moves)
    print(f"This game has {count_moves(moves)} moves.")

    while True:
        try:
            position = int(input("Please enter the move number where you want the position to stop: "))
            if position < 0 or position > count_moves(moves):
                print(f"Error: the number must be positive and not greater than {count_moves(moves)}")
            else:
                break
        except ValueError:
            print("Error: please enter a valid numeric value.")

    fen = analyzer.analyze_moves(moves, position)
    print(f"This is the position FEN: {fen}")

    return fen, link

def chess_com_API():
    games_list = []

    while not games_list:
        player1 = input("Choose the white player (or type 'exit' to quit): ")
        if player1.lower() == "exit":
            print("Exit from the program.")
            return

        player2 = input("Choose the black player (or type 'exit' to quit): ")
        if player2.lower() == "exit":
            print("Exit from the program.")
            return

        try:
            games = get_games_between_players(player1, player2)
            games_list = list(games)

            if games_list:
                print(f"Found {len(games_list)} games between {player1} and {player2}.")
            else:
                print(f"No games found between {player1} and {player2}. Please try again.")
        except Exception as e:
            print(f"Error during the request: {e}")
            print("Please try again with valid names.")

    while True:
        try:
            game_number = int(input("Please enter the game number you want: "))
            if game_number < 0 or game_number >= len(games_list):
                print(f"Error: the number must be positive and less than {len(games_list)}.")
            else:
                break
        except ValueError:
            print("Error: please enter a valid numeric value.")

    game = games[game_number]
    moves_pgn = game["pgn"]
    link = game['url']
    print(link)
    print(moves_pgn)
    print(f"This game has {count_moves(moves_pgn)} moves.")

    while True:
        try:
            position = int(input("Please enter the move number where you want the position to stop: "))
            if position < 0 or position > count_moves(moves_pgn):
                print(f"Error: the number must be positive and not greater than {count_moves(moves_pgn)}")
            else:
                break
        except ValueError:
            print("Error: please enter a valid numeric value.")

    fen = analyze_game_and_get_fen(moves_pgn, position)
    print(f"This is the position FEN: {fen}")
    return fen, link
from abc import ABC, abstractmethod
from model.Lichess import ChessAnalyzer, count_moves
from model.ChessCom import get_games_between_players, analyze_game_and_get_fen
from model.TDFunctions import qr_code_creation, board_creation
from datetime import datetime
import re

class ChessAPI(ABC):
    """
        Abstract base class that defines the interface for chess API interactions.
    """
    @abstractmethod
    def get_games(self, player1, player2):
        pass

    @abstractmethod
    def get_game_details(self, game_id):
        pass

    @abstractmethod
    def analyze_moves(self, moves, position):
        pass


class LichessAPI(ChessAPI):
    def __init__(self, token):
        self.analyzer = ChessAnalyzer(token)

    def get_games(self, player1, player2):
        return self.analyzer.get_games(player1, player2)

    def get_game_details(self, game_id):
        return self.analyzer.get_game_details(game_id)

    def analyze_moves(self, moves, position):
        return self.analyzer.analyze_moves(moves, position)


class ChessComAPI(ChessAPI):
    def get_games(self, player1, player2):
        return get_games_between_players(player1, player2)

    def get_game_details(self, game_id):
        raise NotImplementedError("Chess.com does not use game IDs directly.")

    def analyze_moves(self, moves, position):
        return analyze_game_and_get_fen(moves, position)


class ChessAPIFactory:
    @staticmethod
    def create_api(api_type):
        if api_type == "lichess":
            token = 'lip_vSJWl0oP0i4PQzxhZa3h'
            return LichessAPI(token)
        elif api_type == "chess.com":
            return ChessComAPI()
        else:
            raise ValueError(f"Unknown API type: {api_type}")


def main():
    """
        Main function that drives the program workflow:
            1. Prompts the user to choose a chess API (Lichess or Chess.com).
            2. Fetches games between two players.
            3. Analyzes a specific game chosen by the user.
            4. Computes the board position after a user-specified number of moves.
            5. Generates a QR code and 3D chessboard model based on the game's details.

        To try:
            -Select lichess.
            -Player 1: themoonsman.
            -Player 2: Rofy2.
            -Choose a random game and a random position.

            -Select chess.com
            -Player 1: them00nsman.
            -Player 2: Scarophy.
            (Wait a little bit more, the public API is slow)
            -Choose a random game and a random position.
    """
    print("Choose the Chess API:")
    print("1. Lichess")
    print("2. Chess.com")

    choice = input("Enter your choice (1 or 2): ")
    if choice == "1":
        api = ChessAPIFactory.create_api("lichess")
    elif choice == "2":
        api = ChessAPIFactory.create_api("chess.com")
    else:
        print("Invalid choice. Exiting.")
        return

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
            games = api.get_games(player1, player2)
            games_list = list(games)

            if games_list:
                print(f"Found {len(games_list)} games between {player1} and {player2}.")

                for game in games_list:
                    if choice == "1":  # Lichess
                        game_id = game['id']
                        moves = api.get_game_details(game_id)
                        link = f"https://lichess.org/{game_id}"
                        welo = game["players"]["white"]["rating"]
                        belo = game["players"]["black"]["rating"]
                        date = game["createdAt"]
                        date = date.strftime("%Y-%m-%d")
                        white = game["players"]["white"]["user"]["name"]
                        black = game["players"]["black"]["user"]["name"]
                        print(f"Game {games_list.index(game)}° played on {date} between: {white} - {black} vs {player2} - {welo} vs {belo}")

                    elif choice == "2":  # Chess.com
                        moves = game["pgn"]
                        link = game["url"]
                        white = game["white"]["username"]
                        black = game["black"]["username"]
                        date_match = re.search(r'\[Date "(\d{4}\.\d{2}\.\d{2})"\]', moves)
                        print(f"Game {games_list.index(game)}° played on {date_match.group(1)} between: {white} vs {black}")
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

    if choice == "1":  # Lichess
        game = games_list[game_number]
        game_id = game['id']
        moves = api.get_game_details(game_id)
        link = f"https://lichess.org/{game_id}"
        welo = game["players"]["white"]["rating"]
        belo = game["players"]["black"]["rating"]
        result = game["winner"]
        date = game["createdAt"]
        date = date.strftime("%Y-%m-%d")

    elif choice == "2":  # Chess.com
        game = games_list[game_number]
        moves = game["pgn"]
        link = game["url"]
        date_match = re.search(r'\[Date "(\d{4}\.\d{2}\.\d{2})"\]', moves)

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

    fen = api.analyze_moves(moves, position)
    print(f"This is the position FEN: {fen}")

    qr_code_creation(link)
    board_creation(fen)
    return

if __name__ == "__main__":
    main()

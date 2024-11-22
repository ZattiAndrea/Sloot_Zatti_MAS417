from abc import ABC, abstractmethod
from APIs.Lichess import ChessAnalyzer, count_moves
from APIs.ChessCom import get_games_between_players, analyze_game_and_get_fen
from TDModeling.TDFunctions import qr_code_creation, board_creation

class ChessAPI(ABC):
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
        game_id = games_list[game_number]['id']
        moves = api.get_game_details(game_id)
        link = f"https://lichess.org/{game_id}"
    elif choice == "2":  # Chess.com
        game = games_list[game_number]
        moves = game["pgn"]
        link = game["url"]

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

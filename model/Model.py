from model.APIFunction import lichess_API, chess_com_API
from model.TDFunctions import qr_code_creation, board_creation

class ChessModel:
    def __init__(self):
        self.current_fen = None
        self.current_link = None
        self.selected_database = None

    def select_database(self, database_choice):
        """
        Seleziona il database scelto dall'utente.
        """
        if database_choice.lower() == "lichess":
            self.selected_database = "lichess"
        elif database_choice.lower() == "chess.com":
            self.selected_database = "chess.com"
        else:
            raise ValueError("Database non valido. Scegli tra lichess e chess.com.")

    def fetch_game_data(self, player1, player2):
        """
        Recupera la lista delle partite tra due giocatori.
        """
        if not self.selected_database:
            raise ValueError("Nessun database selezionato.")

        if self.selected_database == "lichess":
            # Chiama l'API di Lichess
            games = self.fetch_from_lichess(player1, player2)
        elif self.selected_database == "chess.com":
            # Chiama l'API di Chess.com
            games = self.fetch_from_chesscom(player1, player2)
        else:
            raise ValueError("Database non valido.")

        return games

    def fetch_from_lichess(self, player1, player2):
        """
        Recupera le partite da Lichess.
        """
        from model.Lichess import ChessAnalyzer  # Import specifico per evitare loop
        analyzer = ChessAnalyzer("lip_vSJWl0oP0i4PQzxhZa3h")  # Inserisci il token
        return analyzer.get_games(player1, player2)

    def fetch_from_chesscom(self, player1, player2):
        """
        Recupera le partite da Chess.com.
        """
        from model.ChessCom import get_games_between_players  # Import specifico
        return get_games_between_players(player1, player2)

    def generate_qr_code(self):
        if not self.current_link:
            raise ValueError("Nessun link disponibile per generare il QR code.")
        qr_code_creation(self.current_link)

    def generate_board_model(self):
        if not self.current_fen:
            raise ValueError("Nessuna posizione FEN disponibile per generare il modello della scacchiera.")
        board_creation(self.current_fen)

    def get_moves_from_game(self, game):
        """
        Recupera le mosse dalla partita selezionata.
        :param game: Dati della partita selezionata.
        :return: Lista delle mosse.
        """
        if self.selected_database == "lichess":
            from model.Lichess import ChessAnalyzer
            analyzer = ChessAnalyzer("lip_vSJWl0oP0i4PQzxhZa3h")
            return analyzer.get_game_details(game['id'])
        elif self.selected_database == "chess.com":
            from model.ChessCom import analyze_game_and_get_moves
            return analyze_game_and_get_moves(game['pgn'])
        else:
            raise ValueError("Database non valido.")

    def get_moves_from_game_id(self, game_id):
        if self.selected_database.lower() == "lichess":
            from model.Lichess import ChessAnalyzer
            analyzer = ChessAnalyzer("lip_vSJWl0oP0i4PQzxhZa3h")
            game_details = analyzer.get_game_details(game_id)
            return game_details
        elif self.selected_database.lower() == "chess.com":
            from model.ChessCom import analyze_game_and_get_moves_by_id
            game_details = analyze_game_and_get_moves_by_id(game_id)
            return game_details["moves"].split()  # Supponendo che le mosse siano in formato PGN
        else:
            raise ValueError("Database non valido.")








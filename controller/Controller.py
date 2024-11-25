from model.APIFunction import lichess_API, chess_com_API
from model.TDFunctions import qr_code_creation, board_creation

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.selected_database = None

    def set_selected_database(self, database_choice):
        if database_choice.lower() not in ["lichess", "chess.com"]:
            raise ValueError("Invalid database.")
        self.selected_database = database_choice.lower()
        self.model.select_database(database_choice.lower())

    def handle_database_selection(self, database_choice):
        if database_choice.lower() == "lichess":
            self.fetch_and_generate("lichess")
        elif database_choice.lower() == "chess.com":
            self.fetch_and_generate("chess.com")
        else:
            self.view.show_error("Invalid database. Choose between lichess and chess.com.")


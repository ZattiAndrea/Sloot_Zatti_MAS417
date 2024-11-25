from controller.Controller import Controller
from model.TDFunctions import qr_code_creation, board_creation
from model.Model import ChessModel
import re
import chess
import chess.svg
import os
from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QWidget, QComboBox, QLineEdit, QListWidget, QMessageBox, QTextEdit, QFileDialog
)

from PyQt6.QtCore import Qt


class Page1(QWidget):
    def __init__(self, switch_page_callback, controller):
        super().__init__()
        self.switch_page_callback = switch_page_callback
        self.controller = controller

        layout = QVBoxLayout()

        self.label = QLabel("Choose a database to search for matches:")
        self.combo_box = QComboBox()
        self.combo_box.addItems(["-- Choose an option --", "lichess", "chess.com"])
        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.handle_confirm)

        layout.addWidget(self.label)
        layout.addWidget(self.combo_box)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

    def handle_confirm(self):
        selected_option = self.combo_box.currentText()
        if selected_option == "-- Choose an option --":
            self.show_error("Choose a valid option.")
        else:
            try:
                self.controller.set_selected_database(selected_option)
                self.switch_page_callback("page2", selected_option)
            except ValueError as e:
                self.show_error(str(e))

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

class Page2(QWidget):
    def __init__(self, switch_page_callback, model, selected_database):
        super().__init__()
        self.switch_page_callback = switch_page_callback
        self.model = model
        self.selected_database = selected_database

        layout = QVBoxLayout()

        self.label = QLabel(f"Selected Database: {self.selected_database}")
        self.player1_input = QLineEdit()
        self.player1_input.setPlaceholderText("Player 1")
        self.player2_input = QLineEdit()
        self.player2_input.setPlaceholderText("Player 2")
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.handle_search)

        self.games_list = QListWidget()

        self.game_id_input = QLineEdit()
        self.game_id_input.setPlaceholderText("Enter Game ID")

        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.handle_confirm_game_id)

        id_layout = QHBoxLayout()
        id_layout.addWidget(self.game_id_input)
        id_layout.addWidget(self.confirm_button)

        layout.addWidget(self.label)
        layout.addWidget(self.player1_input)
        layout.addWidget(self.player2_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.games_list)
        layout.addLayout(id_layout)

        self.setLayout(layout)

    def handle_search(self):
        player1 = self.player1_input.text()
        player2 = self.player2_input.text()

        if not player1 or not player2:
            QMessageBox.warning(self, "Error", "Enter both player names.")
            return

        try:
            self.games_list.clear()
            if (self.selected_database == "lichess"):
                games = self.model.fetch_from_lichess(player1, player2)
                for game in games:
                    date = game["createdAt"]
                    date = date.strftime("%Y-%m-%d")
                    white = game["players"]["white"]["user"]["name"]
                    black = game["players"]["black"]["user"]["name"]
                    self.games_list.addItem(f"Game played: {date} - {white} vs {black} - Game ID: {game['id']}")
            else:
                games = self.model.fetch_from_chesscom(player1, player2)
                for game in games:
                    moves = game["pgn"]
                    date = re.search(r'\[Date "(\d{4}\.\d{2}\.\d{2})"\]', moves)
                    white = game["white"]["username"]
                    black = game["black"]["username"]
                    game_id = game["url"][-10:]
                    self.games_list.addItem(f"Game played: {date.group(1)} - {white} vs {black} - Game ID: {game_id}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to retrieve games: {str(e)}")

    def handle_confirm_game_id(self):
        game_id = self.game_id_input.text().strip()

        if not game_id:
            QMessageBox.warning(self, "Error", "Please enter a valid Game ID.")
            return

        try:
            self.switch_page_callback("page3", game_id)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to switch to game view: {str(e)}")



class Page3(QWidget):
    def __init__(self, switch_page_callback, model, game_id):
        super().__init__()
        self.switch_page_callback = switch_page_callback
        self.model = model
        self.game_id = game_id
        self.moves = []
        self.current_move_index = 0
        self.board = chess.Board()

        layout = QVBoxLayout()

        self.details_label = QLabel(f"Game ID: {self.game_id}")

        self.chessboard_output = QTextEdit()
        self.chessboard_output.setReadOnly(True)
        self.chessboard_output.setStyleSheet("font-family: Courier; font-size: 23px;")
        self.update_board_output()

        self.current_move_label = QLabel("Loading moves...")

        self.button_layout = QHBoxLayout()
        self.previous_button = QPushButton("◀️")
        self.previous_button.clicked.connect(self.previous_move)
        self.confirm_button = QPushButton("✔️")
        self.confirm_button.clicked.connect(self.confirm_position)
        self.next_button = QPushButton("▶️")
        self.next_button.clicked.connect(self.next_move)

        self.button_layout.addWidget(self.previous_button)
        self.button_layout.addWidget(self.confirm_button)
        self.button_layout.addWidget(self.next_button)

        layout.addWidget(self.details_label)
        layout.addWidget(self.chessboard_output)
        layout.addWidget(self.current_move_label)
        layout.addLayout(self.button_layout)

        self.setLayout(layout)

        if self.game_id:
            self.load_game_details()

    def parse_moves(self, moves_string):
        return moves_string.strip().split()

    def load_game_details(self):
        try:
            raw_moves = self.model.get_moves_from_game_id(self.game_id)
            self.moves = self.parse_moves(raw_moves)
            if not self.moves:
                raise ValueError("No moves found for the given Game ID.")
            self.update_move_display()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load game details: {str(e)}")
            self.switch_page_callback("page2")

    def get_current_move_text(self):
        if 0 <= self.current_move_index < len(self.moves):
            return f"Current move: {self.moves[self.current_move_index]}"
        return "No moves available."

    def previous_move(self):
        if self.current_move_index > 0:
            self.current_move_index -= 1
            self.update_board_state()
            self.update_move_display()

    def next_move(self):
        if self.current_move_index < len(self.moves) - 1:
            self.current_move_index += 1
            self.update_board_state()
            self.update_move_display()

    def confirm_position(self):
        try:
            fen_position = self.board.fen()
            game_link = f"https://lichess.org/{self.game_id}"
            qr_code_creation(game_link)

            directory = QFileDialog.getExistingDirectory(self, "Select Directory to Save Final Model")
            if not directory:
                QMessageBox.warning(self, "Save Cancelled", "No directory selected. File not saved.")
                return

            output_file = os.path.join(directory, "final_model.stl")

            board_creation(fen_position, output_file)

            QMessageBox.information(
                self,
                "Model Saved",
                f"The final model has been successfully saved to:\n{output_file}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while generating or saving the file: {str(e)}")

    def update_board_state(self):
        self.board.reset()
        for move in self.moves[:self.current_move_index + 1]:
            self.board.push_san(move)
        self.update_board_output()

    def update_board_output(self):
        board_text = self.board.unicode(borders=True)
        self.chessboard_output.clear()
        self.chessboard_output.setText(board_text)

    def update_move_display(self):
        self.current_move_label.setText(self.get_current_move_text())



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chess App")
        self.setGeometry(100, 100, 800, 600)

        self.model = ChessModel()
        self.controller = Controller(self.model, self)

        self.pages = {
            "page1": Page1(self.switch_page, self.controller),
            "page2": None,
            "page3": None,
        }

        self.current_page = None
        self.switch_page("page1")

    def switch_page(self, page_name, data=None):
        if self.current_page:
            self.current_page.setParent(None)

        if page_name == "page2":
            print(f"Switching to Page2 with database: {self.controller.selected_database}")
            self.pages["page2"] = Page2(self.switch_page, self.model, self.controller.selected_database)
            self.current_page = self.pages["page2"]
        elif page_name == "page3":
            print(f"Switching to Page3 with Game ID: {data} and database: {self.controller.selected_database}")
            self.pages["page3"] = Page3(self.switch_page, self.model, game_id=data)
            self.current_page = self.pages["page3"]
        elif page_name == "page1":
            self.current_page = self.pages["page1"]

        self.setCentralWidget(self.current_page)


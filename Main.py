from chessdotcom import ChessDotComClient, ChessDotComClientError
from stl import mesh

import berserk
import chess
import chess.pgn
import io
import datetime
import time
import numpy as np
import cloudscraper
import qrcode
from PIL import Image, ImageDraw, ImageFont

from APIs.APIFunction import lichess_API, chess_com_API
from TDModeling.TDFunctions import qr_code_creation, board_creation

def main():

    while True:
        try:
            api = int(input("If you want to search the game in lichess database digit 0, if you prefer chesscom digit 1: "))
            if api == 0 or api == 1:
                if api == 0:
                    fen, link = lichess_API()
                    qr_code_creation(link)
                    board_creation(fen)
                    break
                else:
                    fen, link = chess_com_API()
                    qr_code_creation(link)
                    board_creation(fen)
                    break
        except ValueError:
            print("Error: please enter a valid numeric value.")


if __name__ == "__main__":
    main()




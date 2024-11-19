from APIs.APIFunction import lichess_API, chess_com_API

def main():

    while True:
        try:
            api = int(input("If you want to search the game in lichess database digit 0, if you prefer chesscom digit 1: "))
            if api == 0 or api == 1:
                if api == 0:
                    fen, link = lichess_API()
                    #qr_code_creation(link)
                    #board_creation(fen)
                    break
                else:
                    fen, link = chess_com_API()
                    #qr_code_creation(link)
                    #board_creation(fen)
                    break
        except ValueError:
            print("Error: please enter a valid numeric value.")


if __name__ == "__main__":
    main()
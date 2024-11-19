from APIs.APIFunction import lichess_API

def main():

    while True:
        try:
            fen, link = lichess_API()
            qr_code_creation(link)
            board_creation(fen)
            break
        except ValueError:
            print("Error: please enter a valid numeric value.")


if __name__ == "__main__":
    main()

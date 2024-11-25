from model.QRCode import qr_code_matrix, matrix_to_stl, position_qrcode
from model.Board import position_realizer

def qr_code_creation(link):
    """
        Generates a 3D STL file of a QR code for the given link.
        Args:
            link (str): The URL or text to encode in the QR code.
        Workflow:
            - Creates a binary QR code matrix using `qr_code_matrix` with a specified version.
            - Converts the QR code matrix into a 3D model using `matrix_to_stl`.
            - Saves the 3D model as an STL file in a specific directory.
        Returns:
            None: The STL file is saved at "TridimensionalModels/qr-code/qrcode.stl".
    """
    qr_matrix = qr_code_matrix(link, version=2)

    output_file = "TridimensionalModels/qr-code/qrcode.stl"
    matrix_to_stl(qr_matrix, dimension_cm=10, height_mm=5, output_file=output_file)

def board_creation(fen, output_file="default"):
    """
        Generates a 3D STL model of a chessboard, places a QR code on it, and saves the final model.
        Args:
            fen (str): A FEN (Forsyth-Edwards Notation) string describing the chessboard's configuration.
            output_file (str, optional): Path for the final STL file. Defaults to "default", which uses a standard path.
        Workflow:
            - Creates a 3D model of the chessboard using `position_realizer` and the given FEN.
            - Retrieves the pre-generated QR code STL file.
            - Combines the chessboard and QR code models into one STL file using `position_qrcode`.
        Returns:
            None: The STL file is saved at the specified or default location.
    """
    board_file = "Models/TridimensionalModels/board.stl"
    position_realizer(board_file, fen)

    qr_file = "Models/TridimensionalModels/qr-code/qrcode.stl"
    if (output_file == "default"):
        output_file = "Models/TridimensionalModels/final-product/final_model.stl"
    position_qrcode("Models/TridimensionalModels/boards/chessMoment.stl", qr_file, output_file)
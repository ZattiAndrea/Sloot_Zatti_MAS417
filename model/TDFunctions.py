from model.QRCode import qr_code_matrix, matrix_to_stl, position_qrcode
from model.Board import position_realizer

def qr_code_creation(link):
    qr_matrix = qr_code_matrix(link, version=2)

    output_file = "TridimensionalModels/qr-code/qrcode.stl"
    matrix_to_stl(qr_matrix, dimension_cm=10, height_mm=5, output_file=output_file)

def board_creation(fen, output_file="default"):
    board_file = "Models/TridimensionalModels/board.stl"
    position_realizer(board_file, fen)

    qr_file = "Models/TridimensionalModels/qr-code/qrcode.stl"
    if (output_file == "default"):
        output_file = "Models/TridimensionalModels/final-product/final_model.stl"
    position_qrcode("Models/TridimensionalModels/boards/chessMoment.stl", qr_file, output_file)
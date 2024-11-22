from TDModeling.QRCode import qr_code_matrix, matrix_to_stl, position_qrcode
from TDModeling.Board import position_realizer

def qr_code_creation(link):
    qr_matrix = qr_code_matrix(link, version=2)

    output_file = "models/qr-code/qrcode.stl"
    matrix_to_stl(qr_matrix, dimension_cm=10, height_mm=5, output_file=output_file)

def board_creation(fen):
    board_file = "models/board.stl"
    position_realizer(board_file, fen)

    qr_file = "models/qr-code/qrcode.stl"
    output_file = "models/final-product/final_model.stl"
    position_qrcode("models/boards/chessMoment.stl", qr_file, output_file)
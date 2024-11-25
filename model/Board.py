import numpy as np
from stl import mesh

#Minimum and maximum coordinates of the chessboard model
min_x, max_x = -8.0, 8.0
min_y, max_y = -1.0, 15.0
min_z, max_z = -1.0, 1.0

def get_square_center(column, row):
    """
        Calculates the center coordinates of a specific square on the chessboard.
        Args:
            column (int): The column index of the square.
            row (int): The row index of the square.
        Returns:
            tuple: A tuple (center_x, center_y, center_z) representing the 3D coordinates of the square's center.
        Notes:
            - Accounts for a height difference between light and dark squares.
            - Uses the predefined minimum and maximum coordinates of the chessboard.
    """
    board_width_x = max_x - min_x
    board_height_y = max_y - min_y
    square_width_x = board_width_x / 8
    square_height_y = board_height_y / 8

    center_x = min_x + square_width_x * (column + 0.5)
    center_y = min_y + square_height_y * (7 - row + 0.5)
    center_z = 1 if (column + row) % 2 == 0 else 0.7

    return center_x, center_y, center_z

def place_piece_on_board(board_mesh, piece_stl_file, column, row):
    """
        Positions a 3D chess piece on a specific square of the chessboard.
        Args:
            board_mesh (mesh.Mesh): The STL mesh of the chessboard.
            piece_stl_file (str): Path to the STL file of the chess piece.
            column (int): The column index of the square.
            row (int): The row index of the square.
        Returns:
            mesh.Mesh: The combined STL mesh of the chessboard and the placed piece.
        Workflow:
            - Loads the STL file for the chess piece.
            - Calculates the target square's center coordinates.
            - Determines the piece's bounding box and centers it on the target square.
            - Combines the chessboard and piece meshes.
    """
    piece_mesh = mesh.Mesh.from_file(piece_stl_file)
    center_x, center_y, center_z = get_square_center(column, row)

    piece_min_x, piece_min_y, piece_min_z = np.min(piece_mesh.vectors, axis=(0, 1))
    piece_max_x, piece_max_y, piece_max_z = np.max(piece_mesh.vectors, axis=(0, 1))
    piece_center_x = (piece_min_x + piece_max_x) / 2
    piece_center_y = (piece_min_y + piece_max_y) / 2
    piece_center_z = piece_min_z

    translation_x = center_x - piece_center_x
    translation_y = center_y - piece_center_y
    translation_z = center_z - piece_center_z

    piece_mesh.translate([translation_x, translation_y, translation_z])
    combined_mesh = mesh.Mesh(np.concatenate([board_mesh.data, piece_mesh.data]))
    return combined_mesh

def position_realizer(board_stl_file, fen):
    """
        Places chess pieces on a chessboard based on a FEN string and saves the resulting STL model.
        Args:
            board_stl_file (str): Path to the STL file of the chessboard.
            fen (str): FEN string describing the initial setup of the chessboard.
        Returns:
            None: Saves the combined STL model as 'chessMoment.stl'.
        Workflow:
            - Loads the chessboard STL file.
            - Parses the FEN string to determine piece positions.
            - Uses `place_piece_on_board` to position each piece on the chessboard.
            - Saves the final combined STL model.
    """
    board_mesh = mesh.Mesh.from_file(board_stl_file)
    piece_files = {
        'p': 'Models/TridimensionalModels/pieces/black_pawn.stl',
        'r': 'Models/TridimensionalModels/pieces/black_rook.stl',
        'n': 'Models/TridimensionalModels/pieces/black_knight.stl',
        'b': 'Models/TridimensionalModels/pieces/black_bishop.stl',
        'q': 'Models/TridimensionalModels/pieces/black_queen.stl',
        'k': 'Models/TridimensionalModels/pieces/black_king.stl',
        'P': 'Models/TridimensionalModels/pieces/white_pawn.stl',
        'R': 'Models/TridimensionalModels/pieces/white_rook.stl',
        'N': 'Models/TridimensionalModels/pieces/white_knight.stl',
        'B': 'Models/TridimensionalModels/pieces/white_bishop.stl',
        'Q': 'Models/TridimensionalModels/pieces/white_queen.stl',
        'K': 'Models/TridimensionalModels/pieces/white_king.stl'
    }

    rows = fen.split(' ')[0].split('/')
    combined_mesh = board_mesh

    for row_idx, row in enumerate(rows):
        col_idx = 0
        for char in row:
            if char.isdigit():
                col_idx += int(char)
            else:
                piece_file = piece_files.get(char)
                if piece_file:
                    combined_mesh = place_piece_on_board(combined_mesh, piece_file, col_idx, row_idx)
                col_idx += 1

    combined_mesh.save('Models/TridimensionalModels/boards/chessMoment.stl')
    print("Model saved.")

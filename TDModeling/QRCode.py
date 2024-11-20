import qrcode
import numpy as np
from stl import mesh

def qr_code_matrix(link, version=1):
    qr = qrcode.QRCode(
        version=version,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    matrix = qr.get_matrix()
    return np.array(matrix, dtype=np.uint8)

def matrix_to_stl(matrix, dimension_cm=10, height_mm=5, output_file="qrcode_3d.stl"):
    rows, cols = matrix.shape
    dimension_mm = dimension_cm * 10
    block_size = dimension_mm / max(rows, cols)

    vertices = []
    faces = []

    for i in range(rows):
        for j in range(cols):
            if matrix[i, j]:
                x, y = j * block_size, i * block_size
                z = 0

                vert = [
                    [x, y, z],
                    [x + block_size, y, z],
                    [x + block_size, y + block_size, z],
                    [x, y + block_size, z],
                    [x, y, z + height_mm],
                    [x + block_size, y, z + height_mm],
                    [x + block_size, y + block_size, z + height_mm],
                    [x, y + block_size, z + height_mm],
                ]
                offset = len(vertices)
                vertices.extend(vert)

                face = [
                    [offset, offset + 1, offset + 2],
                    [offset, offset + 2, offset + 3],
                    [offset + 4, offset + 5, offset + 6],
                    [offset + 4, offset + 6, offset + 7],
                    [offset, offset + 1, offset + 5],
                    [offset, offset + 5, offset + 4],
                    [offset + 1, offset + 2, offset + 6],
                    [offset + 1, offset + 6, offset + 5],
                    [offset + 2, offset + 3, offset + 7],
                    [offset + 2, offset + 7, offset + 6],
                    [offset + 3, offset + 0, offset + 4],
                    [offset + 3, offset + 4, offset + 7],
                ]
                faces.extend(face)

    vertices = np.array(vertices)
    faces = np.array(faces)

    qr_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            qr_mesh.vectors[i][j] = vertices[f[j], :]

    qr_mesh.save(output_file)
    print(f"STL Model saved as '{output_file}'.")


def position_qrcode(board_file, qrcode_file, output_file):
    board = mesh.Mesh.from_file(board_file)
    qrcode = mesh.Mesh.from_file(qrcode_file)

    angle = np.radians(180)
    rotation_matrix = np.array([
        [1, 0, 0],
        [0, np.cos(angle), -np.sin(angle)],
        [0, np.sin(angle), np.cos(angle)]
    ])
    qrcode.rotate_using_matrix(rotation_matrix)

    max_x, min_x = 8, -8
    max_y, min_y = 15, -1
    max_z, min_z = 1, -2.2

    target_qrcode_width = max_x - min_x
    qrcode_limits = qrcode.vectors.max(axis=(0, 1)) - qrcode.vectors.min(axis=(0, 1))
    qrcode_scale_factor = target_qrcode_width / qrcode_limits[0]
    qrcode.vectors *= qrcode_scale_factor

    qrcode_min = qrcode.vectors.min(axis=(0, 1))
    qrcode_max = qrcode.vectors.max(axis=(0, 1))
    qrcode_center_x = (qrcode_max[0] + qrcode_min[0]) / 2
    qrcode_center_y = (qrcode_max[1] + qrcode_min[1]) / 2
    board_center_x = (max_x + min_x) / 2
    board_center_y = (max_y + min_y) / 2

    translation_x = board_center_x - qrcode_center_x
    translation_y = board_center_y - qrcode_center_y
    translation_z = min_z - qrcode_min[2]

    qrcode.vectors += np.array([translation_x, translation_y, translation_z])
    combined_data = np.concatenate([board.data, qrcode.data])
    final_model = mesh.Mesh(np.copy(combined_data))

    final_model.save(output_file)
    print(f"The model has been saved as: '{output_file}'.")


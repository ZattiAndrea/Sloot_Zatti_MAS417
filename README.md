# Best Chess Moments

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)

## Overview

**Best Chess Moments** is a tool designed to encapsulate and enhance the experience of analyzing and preserving chess games. It allows users to retrieve chess game data, visualize the key position in 3D, and create printable 3D models of the chessboard along with additional game details.

This project leverages APIs from the two largest chess platforms, [Chess.com](https://www.chess.com/news/view/published-data-api) and [Lichess](https://lichess.org/api), to fetch dynamic game data. The application supports both CLI and GUI for diverse user preferences.

## Features

- **Game Data Retrieval**: Fetch chess games using player names and match details via Chess.com and Lichess APIs.
- **3D Model Generation**: Create printable 3D models of the chessboard and final game positions.
- **QR Code Integration**: Attach a QR code linking to a webpage for deeper game analysis.
- **Interactive GUI**: Explore positions, and customize 3D output with a user-friendly interface.
- **Design Patterns**: Implements Factory Design and Model-View-Controller (MVC) patterns for maintainability and scalability.

## Technology Stack

- **Python**: Core programming language.
- **NumPy**: For handling Forsyth-Edwards Notation (FEN) structures.
- **PyQt6**: To build the graphical user interface.
- **APIs**: Data fetched from [Chess.com](https://www.chess.com/news/view/published-data-api) and [Lichess](https://lichess.org/api).

## Installation

1. Clone the repository:
   '''python
   git clone https://github.com/ZattiAndrea/Sloot_Zatti_MAS417.git
   cd Sloot_Zatti_MAS417
   '''

2. Install requirements:
   '''bash
   pip install -r requirements.txt
   '''
   
python mainTherminal.py

python mainGUI.py

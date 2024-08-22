import chess
from chess import engine
import random
import csv
import os

# Path to Stockfish executable
STOCKFISH_PATH = 'stockfish.exe'
OUTPUT_FILE = 'chess_data.csv'

# Generate random board positions
def generate_board():
    board = chess.Board()
    move_number = random.randint(0, 40)
    for _ in range(move_number):
        all_valid_moves = list(board.legal_moves)
        if not all_valid_moves:
            break
        random_move = random.choice(all_valid_moves)
        board.push(random_move)
        if board.is_game_over():
            break
    return board

# Find evaluation of the board using Stockfish
def find_evaluation(board, depth, stockfish_path):
    with engine.SimpleEngine.popen_uci(stockfish_path) as stockfish:
        result = stockfish.analyse(board, limit=engine.Limit(depth=depth))
        cp_eval = result['score'].white().score()
        W_D_L = result['score'].white().wdl()
        draw_expectation = W_D_L.draws / 1000
        win_expectation = W_D_L.wins / 1000
        return cp_eval, win_expectation, draw_expectation

# Check if output file exists and initialize data
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, 'r', newline='') as file:
        reader = csv.reader(file)
        data = list(reader)
else:
    data = []

# Continue generating data
start_index = 0 if data == [] else len(data)  # Adjust start index based on existing data
del data # To free my ram
for i in range(start_index, 500001):
    position = generate_board()
    cp_eval, win_expectation, draw_expectation = find_evaluation(position, 15, STOCKFISH_PATH)
    fen = position.fen()
    

    # Save after each evaluation
    with open(OUTPUT_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        if i == 0:
            writer.writerow(['Position', 'Centipawn Evaluation', 'White Win Expectation', 'Draw Expectation'])
        writer.writerow([fen, cp_eval, win_expectation, draw_expectation])

    print(f"Processed {i} / 500000 positions")






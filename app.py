from flask import Flask, request, jsonify
from flask_cors import CORS
import chess
import logging
import random
from positional_table import Postional_tables
from chess import Board

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Initialize a chess board
board = Board()

transposition_table = {}

def load_book(file_path):
    book = {}
    with open(file_path, "r") as f:
        current_position = None
        for line in f:
            line = line.strip()
            if line.startswith("pos"):
                current_position = line[4:].strip()
                book[current_position] = []
            else:
                move, weight = line.split()
                book[current_position].append((move, int(weight)))
    print("book is loaded")
    return book

opening_book = load_book("Book.txt")



def get_book_move( board, book):
    """Retrieve a move from the opening book if available."""
    # Normalize the FEN to match the book format (strip halfmove clock and fullmove number)
    fen = " ".join(board.fen().split()[:4])
    
    if fen in book:
        moves = book[fen]
        total_weight = sum(weight for _, weight in moves)
        choice = random.uniform(0, total_weight)
        cumulative_weight = 0
        for move, weight in moves:
            cumulative_weight += weight
            if choice <= cumulative_weight:
                return move
    return None


def is_capture_move( move):
    """
    Check if the move captures a piece.
    
    :param move: The move to be checked (of type chess.Move).
    :return: True if the move captures a piece, False otherwise.
    """     
    if (board.piece_at(move.to_square) is not None and board.piece_at(move.to_square).color != board.turn):
        logger.debug(f"Move {move} is a capture move")
        return True
    return False

def is_checkmate_move( move):
    """
    Check if the move leads to checkmate.
    
    :param move: The move to be checked (of type chess.Move).
    :return: True if the move leads to checkmate, False otherwise.
    """
    board.push(move)
    is_checkmate = board.is_checkmate()
    board.pop()

    if is_checkmate:
        logger.debug(f"Move {move} leads to checkmate")
    return is_checkmate

def minimax_move( depth):
    best_move = None
    best_score = -float('inf')
    alpha = -float('inf')
    beta = float('inf')

    # Adjust the search depth based on the material situation
    if is_low_material(board, 10, 2) or is_low_material(board, 2, 1):
        depth += 1  # Increase depth when the material is low to search more thoroughly
        logger.info(f"Adjusted depth: {depth}")

    fen = board.fen()
    if fen in transposition_table:
        stored_score, stored_depth = transposition_table[fen]
        if stored_depth >= depth:
            logger.debug(f"Using stored score {stored_score} for FEN {fen} at depth {depth}")
            return stored_score

    capture_moves = []
    non_capture_moves = []
    for move in board.legal_moves:
        if is_capture_move(move):
            capture_moves.append(move)
        else:
            non_capture_moves.append(move)

    # Evaluate capture moves with full depth
    for move in capture_moves:
        capturing_piece = board.piece_at(move.from_square)
        captured_piece = board.piece_at(move.to_square)

        capturing_value = get_piece_value(capturing_piece)
        captured_value = get_piece_value(captured_piece)

        if captured_value > capturing_value:
            logger.info(f"Automatically playing favorable capture: {move}")
            return move
        board.push(move)
        score = minimax(depth - 1, False, alpha, beta)
        board.pop()
        if score > best_score:
            best_score = score
            best_move = move

    # Evaluate non-capture moves with reduced depth
    reduced_depth = max(1, depth - 2)  # Reduce depth for non-capture moves
    for move in non_capture_moves:
        board.push(move)
        score = minimax(reduced_depth, False, alpha, beta)
        board.pop()
        if score > best_score:
            best_score = score
            best_move = move

    return best_move

def minimax( depth, is_maximizing, alpha, beta):
    if depth == 0 or board.is_game_over():
        evaluation = evaluate_board()
        return evaluation

    fen = board.fen()

    if fen in transposition_table:
        stored_score, stored_depth = transposition_table[fen]
        if stored_depth >= depth:
            return stored_score
        else:
            logger.debug(f"Stored depth {stored_depth} is less than current depth {depth}")
            alpha = max(alpha, stored_score)
            beta = min(beta, stored_score)
            new_depth = max(1, depth - stored_depth)
            return minimax(new_depth, is_maximizing, alpha, beta)

    capture_moves = []
    non_capture_moves = []

    for move in board.legal_moves:
        if is_capture_move(move):
            capture_moves.append(move)
        else:
            non_capture_moves.append(move)

    best_score = -float('inf') if is_maximizing else float('inf')

    for move in capture_moves + non_capture_moves:
        board.push(move)
        score = minimax(depth - 1, not is_maximizing, alpha, beta)
        board.pop()

        if is_maximizing:
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
        else:
            best_score = min(best_score, score)
            beta = min(beta, best_score)

        if beta <= alpha:  # Prune
            break

    transposition_table[fen] = (best_score, depth)
    return best_score

def evaluate_board():
    if board.is_checkmate():
        return 100000000 if board.turn == chess.WHITE else -100000000
    elif board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves():
        return 0

    material_score = 0
    positional_score = 0
    endgame = is_low_material(board, 10)
        
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            if piece.color == chess.BLACK:
                material_score += get_piece_value(piece) * 100
                positional_score += get_positional_value(piece, square, endgame)
            else:
                material_score -= get_piece_value(piece) * 100
                positional_score -= get_positional_value(piece, square, endgame)

    if board.is_check():
        material_score += 200 if board.turn == chess.WHITE else -200

    return material_score + positional_score

def is_low_material( board, num, players=2):
    """Check if the player has low material."""
    if players == 2:
        piece_count = sum(1 for square in chess.SQUARES if board.piece_at(square))
    else:
        piece_count = sum(1 for square in chess.SQUARES if board.piece_at(square) and board.piece_at(square).color == chess.WHITE)
    return piece_count <= num

def get_positional_value( piece, square, endgame=False):
    piece_tables = {
        chess.PAWN: Postional_tables.PAWN_TABLE,
        chess.KNIGHT: Postional_tables.KNIGHT_TABLE,
        chess.BISHOP: Postional_tables.BISHOP_TABLE,
        chess.ROOK: Postional_tables.ROOK_TABLE,
        chess.QUEEN: Postional_tables.QUEEN_TABLE,
        chess.KING: Postional_tables.KING_TABLE_END if endgame else Postional_tables.KING_TABLE_MID
    }
    table = piece_tables.get(piece.piece_type, [0] * 64)
    return table[square] if piece.color == chess.WHITE else table[chess.square_mirror(square)]

def get_piece_value( piece):
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }
    return piece_values.get(piece.piece_type, 0)

def restart_board():
    global board
    board = Board()

@app.route('/get_legal_moves', methods=['POST'])
def get_legal_moves():
    data = request.get_json()
    square = data.get('square')
    
    if square:
        # Convert square notation (e.g., 'e2') to chessboard coordinates
        square_idx = chess.parse_square(square)  # e.g., 'e2' -> 52
        
        # Generate legal moves for the piece at the given square
        legal_moves = [move.uci() for move in board.legal_moves if move.from_square == square_idx]
        
        return jsonify({"legal_moves": legal_moves})
    return jsonify({"error": "Invalid square"}), 400

@app.route('/get_board_state', methods=['GET'])
def get_board_state():
    # Return the current board state in FEN format
    return jsonify({"board_state": board.fen()})

@app.route('/make_move', methods=['POST'])
def make_move():
    move = request.json.get('move')
    try:
        print(move)
        # Make the move using the provided UCI notation
        board.push_uci(move)
        if board.is_checkmate():
            print("checkmate")
            return jsonify({"success": True, "checkmate": True, "board_state": board.fen()})
        return jsonify({"success": True, "board_state": board.fen()})
    except ValueError:
        return jsonify({"success": False, "error": "Invalid move"})

@app.route('/get_ai_move', methods=['GET'])
def get_ai_move():
    logger.info("It's my turn, checking for book move...")

    try:
        # Check for a book move
        book_move = get_book_move(board, opening_book)
        if book_move:
            logger.info(f"Playing book move: {book_move}")
            move = chess.Move.from_uci(book_move)  # Convert UCI string to a Move object
        else:
            logger.info("No book move found, calculating best move using minimax...")
            move = minimax_move(depth=5)

        if move:
            # Ensure move is converted to UCI string if it's a chess.Move object
            if isinstance(move, chess.Move):
                move = move.uci()
            
            board.push_uci(move)
            
            if board.is_checkmate():
                
                logger.info("Checkmate detected.")
                # Send the checkmate state without resetting the board yet
                return jsonify({
                    "success": True,
                    "checkmate": True,
                    "board_state": board.fen(),
                    "move": move,
                    "message": "Checkmate! AI wins."
                })
            
            return jsonify({
                "success": True,
                "board_state": board.fen(),
                "move": move
            })
        
        return jsonify({"error": "No valid move found"}), 400

    except Exception as e:
        logger.error(f"Error in /get_ai_move: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.route('/reset_board', methods=['POST'])
def reset_board():
    restart_board()
    print("Board reset to:", board.fen())  # Debug log
    return jsonify({
        "success": True,
        "message": "Board has been reset.",
        "board_state": board.fen()
    })


if __name__ == '__main__':
    app.run(debug=True)

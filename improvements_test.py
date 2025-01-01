import time
import chess
import tkinter as tk
from positional_table import Postional_tables
from PIL import Image, ImageTk


class ChessAI:

    def __init__(self):
        self.board = chess.Board()
        self.transposition_table = {}
        self.total_time = 0  # Initialize total time
        self.move_count = 0  # Initialize move count
        self.available_moves = []  # Placeholder for available moves
        self.piece_images = {}  # Placeholder for piece images (e.g., {'wp': 'white_pawn_image', 'bq': 'black_queen_image'})
        
        # Set up the Tkinter window and canvas for rendering
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=480, height=560)  # Height 480 for the board, 80 for score
        self.canvas.pack()
        self.piece_images = {}
        self.load_piece_images()
    def load_piece_images(self):
        """Load chess piece images."""
        piece_types = ['p', 'n', 'b', 'r', 'q', 'k']  # pawn, knight, bishop, rook, queen, king
        colors = ['w', 'b']  # white, black
        for color in colors:
            for piece in piece_types:
                file_name = f"{color}{piece}.png"
                try:
                    image = Image.open(file_name).resize((50, 50))  # Resize to fit squares
                    self.piece_images[f"{color}{piece}"] = ImageTk.PhotoImage(image)
                except FileNotFoundError:
                    print(f"Image file {file_name} not found.")

    def render_board(self):
        """Render the chessboard and pieces on the canvas."""
        self.canvas.delete("all")
        square_size = 480 // 8  # Size of each square
        for row in range(8):
            for col in range(8):
                color = "#edcbb7" if (row + col) % 2 == 0 else "#4f342e"
                x1 = col * square_size
                y1 = row * square_size
                x2 = x1 + square_size
                y2 = y1 + square_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

        # Draw pieces
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                col = chess.square_file(square)
                row = 7 - chess.square_rank(square)  # Invert row to match canvas orientation
                x = col * square_size + square_size // 2
                y = row * square_size + square_size // 2
                piece_key = f"{'w' if piece.color == chess.WHITE else 'b'}{piece.symbol().lower()}"
                if piece_key in self.piece_images:
                    self.canvas.create_image(x, y, image=self.piece_images[piece_key])

        # Display score
        score = self.evaluate_board_simple()
        self.canvas.create_text(240, 500, text=f"Score: {score}", font=("Arial", 16), fill="black")

    def evaluate_board_simple(self):
        """A simple evaluation function for the board."""
        # Add your custom evaluation logic here, just an example:
        return 0
    def evaluate_board(self):
        # Checkmate or Stalemate conditions
        if self.board.is_checkmate():
            return 100000000 if self.board.turn == chess.WHITE else -100000000
        elif self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.is_seventyfive_moves():
            return 0  # Draw conditions

        material_score = 0
        positional_score = 0
        endgame = self.is_low_material(self.board, 10)  # Detecting low material scenario
        
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                if piece.color == chess.BLACK:
                    material_score += self.get_piece_value(piece) * 100
                    positional_score += self.get_positional_value(piece, square, endgame)
                else:
                    material_score -= self.get_piece_value(piece) * 100
                    positional_score -= self.get_positional_value(piece, square, endgame)

        if self.board.is_check():
            material_score += 200 if self.board.turn == chess.WHITE else -200
        return material_score + positional_score

    def is_low_material(self, board, num, players=2):
        """Check if the player has low material."""
        if players == 2:
            piece_count = sum(1 for square in chess.SQUARES if board.piece_at(square))
        else:
            piece_count = sum(1 for square in chess.SQUARES if board.piece_at(square) and board.piece_at(square).color == chess.WHITE)
        return piece_count <= num  # Adjust this threshold based on your preference

    def get_positional_value(self, piece, square, endgame=False):
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

    def get_piece_value(self, piece):
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }
        return piece_values.get(piece.piece_type, 0)

    def is_capture_move(self, move):
        """Check if the move captures a piece."""
        if (self.board.piece_at(move.to_square) is not None and self.board.piece_at(move.to_square).color != self.board.turn) or self.board.is_checkmate():
            return True
        return False

    def minimax_before_optimization(self, depth, is_maximizing, alpha, beta):
        """Minimax without optimization (transposition table)"""
        if depth == 0 or self.board.is_game_over():
            return self.evaluate_board()

        best_score = -float('inf') if is_maximizing else float('inf')

        for move in self.board.legal_moves:
            self.board.push(move)
            score = self.minimax_before_optimization(depth - 1, not is_maximizing, alpha, beta)
            self.board.pop()

            if is_maximizing:
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
            else:
                best_score = min(best_score, score)
                beta = min(beta, best_score)

            if beta <= alpha:  # Alpha-Beta pruning
                break

        return best_score

    def minimax_move_before(self, depth):
        best_move = None
        best_score = -float('inf')
        alpha = -float('inf')
        beta = float('inf')

        # Adjust the search depth based on the material situation
        if self.is_low_material(self.board, 10, 2) or self.is_low_material(self.board, 2, 1):
            depth += 1  # Increase depth when the material is low to search more thoroughly

        capture_moves = []
        non_capture_moves = []
        for move in self.board.legal_moves:
            if self.is_capture_move(move):
                capture_moves.append(move)
            else:
                non_capture_moves.append(move)

        # Evaluate capture moves with full depth
        for move in capture_moves:
            self.board.push(move)
            score = self.minimax_before_optimization(depth - 1, False, alpha, beta)
            self.board.pop()
            if score > best_score:
                best_score = score
                best_move = move

        # Evaluate non-capture moves with reduced depth
        reduced_depth = max(1, depth - 2)  # Reduce depth for non-capture moves
        for move in non_capture_moves:
            self.board.push(move)
            score = self.minimax_before_optimization(reduced_depth, False, alpha, beta)
            self.board.pop()
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def minimax_after_optimization(self, depth, is_maximizing, alpha, beta):
        if depth == 0 or self.board.is_game_over():
            evaluation = self.evaluate_board()
            return evaluation

        fen = self.board.fen()

        # Transposition table lookup
        if fen in self.transposition_table:
            stored_score, stored_depth = self.transposition_table[fen]

            # If the stored depth is less than the current depth, continue searching deeper
            if stored_depth >= depth:
                return stored_score
            else:
                alpha = max(alpha, stored_score)
                beta = min(beta, stored_score)  # Update beta to prevent worse moves for minimizing
                new_depth = max(1, depth - stored_depth)  # Ensure positive depth
                return self.minimax_after_optimization(new_depth, is_maximizing, alpha, beta)

        capture_moves = []
        non_capture_moves = []

        # Categorize moves
        for move in self.board.legal_moves:
            if self.is_capture_move(move):
                capture_moves.append(move)
            else:
                non_capture_moves.append(move)

        best_score = -float('inf') if is_maximizing else float('inf')

        # Evaluate capture moves first
        for move in capture_moves + non_capture_moves:
            self.board.push(move)
            score = self.minimax_after_optimization(depth - 1, not is_maximizing, alpha, beta)
            self.board.pop()

            if is_maximizing:
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
            else:
                best_score = min(best_score, score)
                beta = min(beta, best_score)

            if beta <= alpha:  # Prune
                break

        # Store result in transposition table
        self.transposition_table[fen] = (best_score, depth)
        return best_score

    def minimax_move_after(self, depth):
        best_move = None
        best_score = -float('inf')
        alpha = -float('inf')
        beta = float('inf')

        # Adjust the search depth based on the material situation
        if self.is_low_material(self.board, 10, 2) or self.is_low_material(self.board, 2, 1):
            depth += 1  # Increase depth when the material is low to search more thoroughly

        fen = self.board.fen()
        if fen in self.transposition_table:
            stored_score, stored_depth = self.transposition_table[fen]

            # If the stored depth is greater than or equal to the current depth, return the stored score
            if stored_depth >= depth:
                return stored_score

        capture_moves = []
        non_capture_moves = []
        for move in self.board.legal_moves:
            if self.is_capture_move(move):
                capture_moves.append(move)
            else:
                non_capture_moves.append(move)

        # Evaluate capture moves with full depth
        for move in capture_moves:
            self.board.push(move)
            score = self.minimax_after_optimization(depth - 1, False, alpha, beta)
            self.board.pop()
            if score > best_score:
                best_score = score
                best_move = move

        # Evaluate non-capture moves with reduced depth
        reduced_depth = max(1, depth - 2)  # Reduce depth for non-capture moves
        for move in non_capture_moves:
            self.board.push(move)
            score = self.minimax_after_optimization(reduced_depth, False, alpha, beta)
            self.board.pop()
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def play_game(self, depth=3):
        """Simulate a game between two AI players."""
        while not self.board.is_game_over():
            # Make a move (simulated)
            move = self.minimax_move_after(depth)
            self.board.push(move)
            self.available_moves = list(self.board.legal_moves)  # Get available moves for current player
            
            self.render_board()  # Render the updated board after the move
            self.root.update()  # Update the Tkinter window

        # Show result after the game
        print("Game Over!")
        result = self.board.result()
        print(f"Final result: {result}")
        if result == "1-0":
            print("Winner: White")
        elif result == "0-1":
            print("Winner: Black")
        else:
            print("Game ended in a draw")

    def play(self):
        """Start the game loop in the Tkinter window."""
        self.play_game(depth=5)
        self.root.mainloop()  # Run the Tkinter event loop

# Initialize and run the game
if __name__ == "__main__":
    ai = ChessAI()
    ai.play()
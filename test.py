import chess
import berserk
import logging
import random
from positional_table import Postional_tables

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Authenticate with Lichess API
API_TOKEN = "lip_NT9NAQZUbXWEfqd2hgOZ"
session = berserk.TokenSession(API_TOKEN)
client = berserk.Client(session)

class LichessBot:
    def __init__(self):
        self.board = chess.Board()
        self.transposition_table = {}
        self.is_white = None  # To track if the bot plays white or black
        self.opening_book = self.load_book("Book.txt")


    def load_book(self, file_path):
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
    
    def get_book_move(self, board, book):
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
    def play_game(self, game_id):
        logger.info(f"Playing game: {game_id}")
        for game_state in client.bots.stream_game_state(game_id):
            if 'gameStart' in game_state:
                # Determine if bot is white or black
                if game_state['game']['players']['white']['id'] == "bot-id":
                    self.is_white = True  # Bot is white
                else:
                    self.is_white = False  # Bot is black
                logger.info(f"Bot is {'white' if self.is_white else 'black'}.")
            
            if 'moves' in game_state:
                moves = game_state['moves'].split()
                self.board = chess.Board()
                for move in moves:
                    self.board.push_uci(move)

                # Check if it's the bot's turn and the game is still ongoing
                logger.info(f"Current board: {self.board.fen()}")
                logger.info(f"Is it my turn? (bot is {'white' if self.is_white else 'black'}): {self.is_white and self.board.turn == chess.WHITE or not self.is_white and self.board.turn == chess.BLACK}")

                if not self.board.is_game_over():
                    # If bot is white and it's its turn
                    if (self.is_white and self.board.turn == chess.WHITE) or (not self.is_white and self.board.turn == chess.BLACK):
                        logger.info("It's my turn, checking for book move...")

                        # Check for a book move
                        book_move = self.get_book_move(self.board, self.opening_book)
                        if book_move:
                            logger.info(f"Playing book move: {book_move}")
                            move = chess.Move.from_uci(book_move)  # Convert UCI string to a move object
                        else:
                            logger.info("No book move found, calculating best move using minimax...")
                            move = self.minimax_move(depth=5)

                        # Play the move
                        logger.info(f"Playing move: {move}")
                        client.bots.make_move(game_id, move.uci())
                    else:
                        logger.info("Not my turn or game is over.")



    def is_capture_move(self, move):
        """
        Check if the move captures a piece.
        
        :param move: The move to be checked (of type chess.Move).
        :return: True if the move captures a piece, False otherwise.
        """     
        if (self.board.piece_at(move.to_square) is not None and self.board.piece_at(move.to_square).color != self.board.turn):
            logger.debug(f"Move {move} is a capture move")
            return True
        return False

    def is_checkmate_move(self, move):
        """
        Check if the move leads to checkmate.
        
        :param move: The move to be checked (of type chess.Move).
        :return: True if the move leads to checkmate, False otherwise.
        """
        self.board.push(move)
        is_checkmate = self.board.is_checkmate()
        self.board.pop()

        if is_checkmate:
            logger.debug(f"Move {move} leads to checkmate")
        return is_checkmate

    def minimax_move(self, depth):
        best_move = None
        best_score = -float('inf')
        alpha = -float('inf')
        beta = float('inf')

        # Adjust the search depth based on the material situation
        if self.is_low_material(self.board, 10, 2) or self.is_low_material(self.board, 2, 1):
            depth += 1  # Increase depth when the material is low to search more thoroughly
            logger.info(f"Adjusted depth: {depth}")

        fen = self.board.fen()
        if fen in self.transposition_table:
            stored_score, stored_depth = self.transposition_table[fen]
            if stored_depth >= depth:
                logger.debug(f"Using stored score {stored_score} for FEN {fen} at depth {depth}")
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
            capturing_piece = self.board.piece_at(move.from_square)
            captured_piece = self.board.piece_at(move.to_square)

            capturing_value = self.get_piece_value(capturing_piece)
            captured_value = self.get_piece_value(captured_piece)

            if captured_value > capturing_value:
                logger.info(f"Automatically playing favorable capture: {move}")
                return move
            self.board.push(move)
            score = self.minimax(depth - 1, False, alpha, beta)
            self.board.pop()
            if score > best_score:
                best_score = score
                best_move = move

        # Evaluate non-capture moves with reduced depth
        reduced_depth = max(1, depth - 2)  # Reduce depth for non-capture moves
        for move in non_capture_moves:
            self.board.push(move)
            score = self.minimax(reduced_depth, False, alpha, beta)
            self.board.pop()
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def minimax(self, depth, is_maximizing, alpha, beta):
        if depth == 0 or self.board.is_game_over():
            evaluation = self.evaluate_board()
            return evaluation

        fen = self.board.fen()

        if fen in self.transposition_table:
            stored_score, stored_depth = self.transposition_table[fen]
            if stored_depth >= depth:
                return stored_score
            else:
                logger.debug(f"Stored depth {stored_depth} is less than current depth {depth}")
                alpha = max(alpha, stored_score)
                beta = min(beta, stored_score)
                new_depth = max(1, depth - stored_depth)
                return self.minimax(new_depth, is_maximizing, alpha, beta)

        capture_moves = []
        non_capture_moves = []

        for move in self.board.legal_moves:
            if self.is_capture_move(move):
                capture_moves.append(move)
            else:
                non_capture_moves.append(move)

        best_score = -float('inf') if is_maximizing else float('inf')

        for move in capture_moves + non_capture_moves:
            self.board.push(move)
            score = self.minimax(depth - 1, not is_maximizing, alpha, beta)
            self.board.pop()

            if is_maximizing:
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
            else:
                best_score = min(best_score, score)
                beta = min(beta, best_score)

            if beta <= alpha:  # Prune
                break

        self.transposition_table[fen] = (best_score, depth)
        return best_score

    def evaluate_board(self):
        if self.board.is_checkmate():
            return 100000000 if self.board.turn == chess.WHITE else -100000000
        elif self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.is_seventyfive_moves():
            return 0

        material_score = 0
        positional_score = 0
        endgame = self.is_low_material(self.board, 10)
            
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
        return piece_count <= num

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

# Start listening for incoming challenges
bot = LichessBot()
try:
    logger.info("Bot is now running and listening for challenges...")
    for event in client.bots.stream_incoming_events():
        if event['type'] == 'challenge':
            challenge_id = event['challenge']['id']
            logger.info(f"Accepting challenge: {challenge_id}")
            client.bots.accept_challenge(challenge_id)
        elif event['type'] == 'gameStart':
            bot.play_game(event['game']['id'])
except Exception as e:
    logger.error(f"An error occurred: {e}")

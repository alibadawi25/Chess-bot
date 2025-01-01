import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import chess
import random
from PIL import Image, ImageTk
import time
import multiprocessing
from positional_table import Postional_tables
import threading


class ChessApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Chess Game")

        self.board = chess.Board()
        self.canvas = tk.Canvas(root, width=480, height=520, bg="#ada397")
        self.canvas.pack_forget()  # Initially, hide the canvas

        self.selected_square = None
        self.available_moves = []
        self.player_color = chess.WHITE  # Human plays White by default
        self.ai_difficulty = 'medium'  # Default AI difficulty
        self.is_1v1 = False  # Game mode: False = 1vAI, True = 1v1
        self.mode = "game"
        self.solutions = []
        self.index = 0
        self.transposition_table = {}
        self.puzzles = {
            "4r1rk/5K1b/7R/R7/8/8/8/8 w - - 0 1": "Rxh7+ Kxh7 Rh5#",
            "8/1r6/8/3R4/k7/p1K5/4r3/R7 w - - 0 1": "Rxa3+ Kxa3 Ra5#",
            "6k1/8/6K1/8/8/3r4/4r3/5R1R w - - 0 1": "Rh8+ Kxh8 Rf8#",
            "2rkr3/2ppp3/2n1n3/R2R4/8/8/3K4/8 w - - 0 1": "Rxd7+ Kxd7 Rd5#",
            "4rkr1/1R1R4/4bK2/8/8/8/8/8 w - - 0 1": "Rf7+ Bxf7 Rxf7#",
            "5K1k/6pp/7R/8/8/8/8/6R1 w - - 0 1": "Rgg6 gxh6 Rg8#",
            "2k5/1q4b1/3K4/8/7R/8/7R/8 w - - 0 1": "Rh8+ Bxh8 Rxh8#",
            "8/8/q5b1/7k/5Kp1/1R1R4/8/8 w - - 0 1": "Rh3+ gxh3 Rxh3#",
            "k7/3b4/1K6/8/8/5q2/2R1R3/8 w - - 0 1": "Re8+ Bxe8 Rc8#",
            "8/1R1R4/8/p7/k1K5/r5r1/8/8 w - - 0 1": "Rb4+ axb4 Ra7#",
            "kr6/1p6/8/1p5R/6R1/8/1r6/5K2 w - - 0 1": "Ra4+ bxa4 Ra5#",
            "6R1/8/8/7p/5K1k/r6r/8/6R1 w - - 0 1": "R1g4+ hxg4 Rh8#",
            "kb6/p4q2/2K5/8/8/8/8/1R1R4 w - - 0 1": "Rxb8+ Kxb8 Rd8#",
            "8/6p1/6rk/6np/R6R/6K1/8/8 w - - 0 1": "Rxh5+ Kxh5 Rh4#",
            "kn1R4/ppp5/2q5/8/8/8/8/3RK3 w - - 0 1": "Rxb8+ Kxb8 Rd8#",
            "1kb4R/1npp4/8/8/8/8/8/R5K1 w - - 0 1": "Rxc8+ Kxc8 Ra8#",
            "8/8/1b6/kr6/pp6/1n6/7R/R3K3 w Q - 0 1": "Rxa4+ Kxa4 Ra2#",
            "5K1k/7p/8/2p5/2rp4/8/p7/1B4B1 w - - 0 1": "Bh2 axb8/Q Be5#",
            "k7/p7/B2K4/8/8/8/3p2p1/4B3 w - - 0 1": "Kc7 dxe1/Q Bb7#",
            "8/5n2/8/6B1/8/4K3/7p/5B1k w - - 0 1": "Kf2 Nxg5 Bg2#",
            "8/5p2/7p/5Kpk/4BB1p/7r/8/8 w - - 0 1": "Bd5 gxf4 Bxf7#",
            "8/6N1/8/pp6/kp6/pp5K/2N5/8 w - - 0 1": "Ne6 bxc2 Nc5#",
            "8/8/8/7N/8/8/1p5p/N3K2k w - - 0 1": "Kf2 bxa1/Q Ng3#",
            "4K3/8/8/4N1pr/4b1pk/4N1nr/8/8 w - - 0 1": "Ng2+ Bxg2 Ng6#",
            "k7/ppK5/2N5/3N4/8/8/7p/8 w - - 0 1": "Kc8 bxc6 Nc7#",
            "7k/4K1pp/6pn/6N1/6N1/8/8/8 w - - 0 1": "Kf8 Nxg4 Nf7#",
            "8/8/7p/5K1k/7p/8/2pn1N2/3N4 w - - 0 1": "Nh3 cxd1/Q Nf4#",
            "8/4PKPk/5n1p/4b3/8/8/p7/q7 w - - 0 1": "e8/Q+ Nxe8 g8/Q#",
            "2b5/7P/4Pp2/7p/5K1k/7p/p6n/8 w - - 0 1": "h8/N a1/Q Ng6#",
            "1k1B4/8/1K6/1n6/q7/8/8/3R4 w - - 0 1": "Bc7+ Nxc7 Rd8#",
            "7k/B7/6K1/8/8/2b5/7r/R7 w - - 0 1": "Bd4+ Bxd4 Ra8+",
            "6Bk/R4K2/8/8/8/8/8/8 w - - 0 1": "Kg6 Kxg8 Ra8#",
            "5Knk/7b/R7/8/7B/8/8/8 w - - 0 1": "Rh6 Nxh6 Bf6#",
            "7k/5ppr/K5p1/8/8/8/2B5/2R5 w - - 0 1": "Bxg6 fxg6 Rc8#",
            "6B1/p1K5/k7/pp6/8/8/8/R7 w - - 0 1": "Ra4 bxa4 Bc4#",
            "r7/kp6/pR1Q4/5q2/8/8/8/3K4 w - - 0 1": "Rxa6+ bxa6 Qc7#",
            "4Q3/kr6/pp6/8/8/8/6q1/R2K4 w - - 0 1": "Rxa6+ Kxa6 Qa4#",
            "6rk/6n1/1R1Q4/7r/8/8/8/3K4 w - - 0 1": "Qh6+ Rxh6 Rxh6#",
            "1k4r1/ppp5/8/8/2q5/8/5Q2/3K1R2 w - - 0 1": "Qf8+ Rxf8 Rxf8#",
            "3R4/2q5/8/rpn5/kp5Q/2n5/1K6/8 w - - 0 1": "Qxb4+ Kxb4 Rd4#",
            "1q1r3k/7p/7K/8/4R3/2p5/8/1Q6 w - - 0 1": "Re8+ Rxe8 Qxh7#",
            "kr6/1p6/p5R1/8/1q6/8/Q7/2K5 w - - 0 1": "Rxa6+ bxa6 Qxa6#",
            "k7/p2bR3/Q7/8/3q4/8/8/2K5 w - - 0 1": "Re8+ Bxe8 Qc8#",
            "k3r3/pR6/K7/2b5/8/8/1Q3q2/8 w - - 0 1": "Rxa7+ Bxa7 Qb7#",
            "3rkr2/R3p3/8/4K3/8/7Q/5q2/8 w - - 0 1": "Rxe7+ Kxe7 Qe6#",
            "2k5/1ppn4/1q6/8/Q7/8/5R2/4K3 w - - 0 1": "Rf8+ Nxf8 Qe8#",
            "k1r5/p1p5/N1K5/8/3q4/8/8/1R6 w - - 0 1": "Rb8+ Rxb8 Nxc7#",
            "8/8/6Nr/5Kbk/R7/8/8/8 w - - 0 1": "Rh4+ Bxh4 Nf4#",
            "kr6/pp6/8/8/2N4R/8/8/3K4 w - - 0 1": "Nb6+ axb6 Ra4#",
            "4nrkr/5pp1/8/7N/8/8/8/3K2R1 w - - 0 1": "Rxg7+ Nxg7 Nf6#",
            "2Nnkr2/3p3R/8/5n2/8/8/8/7K w - - 0 1": "Re7+ Nxe7 Nd6#",
            "2R5/8/pn6/k1N5/8/1K6/6q1/8 w - - 0 1": "Nb7+ Qxb7 Rc5#",
            "5Kbk/R7/4q1P1/8/8/8/8/8 w - - 0 1": "Rh7+ Bxh7 g7#",
            "5Kbk/6pp/6pR/5P2/8/8/8/8 w - - 0 1": "fxg6 gxh6 g7#",
            "3k4/1P6/3K4/8/8/8/1q6/7R w - - 0 1": "Rh8+ Qh8 b8/Q#",
            "qkb5/4p3/1K1p4/8/5Q2/6B1/8/8 w - - 0 1": "Qxd6+ exd6 Bxd6#",
            "B7/8/8/7K/4b3/Q7/7p/1q4bk w - - 0 1": "Qf3+ Bxf3 Bxf3#",
            "8/8/B7/3qp3/2ppkpp1/8/4K3/3Q4 w - - 0 1": "Qd3+ cxd3+ Bxd3#",
            "6bk/7p/7K/4N3/8/8/7B/8 w - - 0 1": "Ng6+ hxg6 Be5#",
            "5K1k/6pp/6p1/6B1/6N1/8/8/8 w - - 0 1": "Nh6 gxh6 Bf6#",
            "8/8/5B2/8/2pN4/K7/pp6/kb6 w - - 0 1": "Nb3+ cxb3 Bxb2#",
            "kbK5/p7/2pN4/3p4/8/8/8/5B2 w - - 0 1": "Ba6 Bxd6 Bb7#",
            "7B/8/pb6/kpn5/b1p5/1P6/1K6/8 w - - 0 1": "b4+ Kxb4 Bc3#",
            "kb1n4/8/KP6/8/B7/8/8/8 w - - 0 1": "Bc6+ Nxc6 b7#",
            "3B1K1k/6pp/4b3/7P/8/8/8/8 w - - 0 1": "h6 gxh6 Bf6#",
            "8/8/8/6pp/5p1k/5K1b/5P1B/8 w - - 0 1": "Bg3+ fxg3 fxg3#",
            "k1r2q2/ppQ5/N7/8/8/8/8/3K4 w - - 0 1": "Qb8+ Rxb8 Nc7#",
            "4q2k/4N1pr/8/8/2Q5/8/4K3/8 w - - 0 1": "Qg8+ Qxg8 Ng6#",
            "rknN4/2p5/1rQ5/8/8/8/1q6/3K4 w - - 0 1": "Qb7+ Rxb7 Nc6#",
            "4r1kr/5b1p/5KN1/8/8/Q7/3q4/8 w - - 0 1": "Qf8+ Rxf8 Ne7#",
            "7k/4NKpp/4Q3/8/8/2q2p2/8/6r1 w - - 0 1": "Ng6+ hxg6 Qh3#",
            "k1b5/8/NKn5/8/4q3/8/7Q/8 w - - 0 1": "Qb8+ Nxb8 Nc7#",
            "k4K2/p7/1bP5/8/8/8/8/6qQ w - - 0 1": "c7+ Qxh1 c8/Q#",
            "5rkr/5ppp/8/4K3/6N1/2Q5/q7/8 w - - 0 1": "Nh6+ gxh6 Qg3#",
            "krQ5/p7/8/4q3/N7/8/8/3K4 w - - 0 1": "Nb6+ axb6 Qa6#",
            "8/1q6/4NQ1r/5npk/8/7K/8/6r1 w - - 0 1": "Qxg5+ Rxg5 Nf4#",
            "k1r5/p1pq4/Qp1p4/8/3N4/8/3K4/8 w - - 0 1": "Nc6 Qxc6 Qxc8#",
            "3q2rk/5Q1p/6bK/4N3/8/8/8/8 w - - 0 1": "Qxh7+ Bxh7 Nf7#",
            "8/8/5Q2/2q3pk/7b/8/4K1P1/8 w - - 0 1": "g4+ Kxg4 Qf3#",
            "8/b2Q4/kp2p3/p2q4/1P6/K7/8/8 w - - 0 1": "b5+ Qxb5 Qc8#",
            "8/8/8/pq6/kpp5/7Q/K1P5/8 w - - 0 1": "Qb3+ cxb3+ cxb3#",
            "5K1k/7b/8/4ppP1/8/6bQ/7q/8 w - - 0 1": "g6 Qxh3 g7#",
            "8/p7/kPK5/p7/n7/8/8/8 w - - 0 1": "b7 Nc3 b8/N#",
            "8/8/6nq/3p2b1/7k/7p/5Kpp/3BB3 w - - 0 1": "Kf3+ Kh5 Kg3#",
        }
        
        self.opening_book = self.load_book("book.txt")
        # Initialize player names
        self.player1_name = ""
        self.player2_name = ""

        self.captured_pieces = {}

        # Load piece images
        self.piece_images = {}
        self.load_piece_images()

        # Display the main menu screen
        self.show_mode_selection_screen()

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

    def load_background_image(self):
        """Load and display background image."""
        bg_image = Image.open("background.jpg!w700wp") 
        bg_image = bg_image.resize((900, 600))
        self.bg_image_tk = ImageTk.PhotoImage(bg_image)
        bg_canvas = tk.Canvas(self.root, width=900, height=600)
        bg_canvas.pack(fill="both", expand=True)
        bg_canvas.create_image(0, 0, anchor="nw", image=self.bg_image_tk)

    def set_background(self):
        """Set the background image for the main window."""
        bg_image = Image.open("background.jpg!w700wp")  # Replace with the path to your image
        bg_image = bg_image.resize((900, 600))
        self.bg_image_tk = ImageTk.PhotoImage(bg_image)
    
        bg_canvas = tk.Canvas(self.root, width=900, height=600)
        bg_canvas.pack(fill="both", expand=True)
        bg_canvas.create_image(0, 0, anchor="nw", image=self.bg_image_tk)
    
        return bg_canvas


    def show_mode_selection_screen(self):
        """Display a screen to choose the game mode."""
        self.clear_screen()
        self.load_background_image()

        label = tk.Label(self.root, text="Choose Game Mode", font=("Arial", 16), bg="#ada397")
        label.place(relx=0.5, rely=0.1, anchor="center")

        btn_instructions = tk.Button(self.root, text="Instructions", font=("Arial", 14), command=self.show_instructions, bg="#ada397")
        btn_instructions.place(relx=0.5, rely=0.3, anchor="center")

        btn_1v1 = tk.Button(self.root, text="1v1 (Local)", font=("Arial", 14), command=self.show_name_entry_1v1, bg="#ada397")
        btn_1v1.place(relx=0.5, rely=0.7, anchor="center")

        btn_1vai = tk.Button(self.root, text="1vAI (Computer)", font=("Arial", 14), command=self.show_difficulty_selection, bg="#ada397")
        btn_1vai.place(relx=0.5, rely=0.9, anchor="center")

        btn_instructions = tk.Button(self.root, text="Puzzles", font=("Arial", 14), command=self.show_puzzles, bg="#ada397")
        btn_instructions.place(relx=0.5, rely=0.5, anchor="center")


    def show_puzzles(self):
        self.mode = "puzzle"

        self.clear_screen()
        self.load_background_image()

        label = tk.Label(self.root, text="Enter Player Names", font=("Arial", 16), bg="#ada397")
        label.place(relx=0.5, rely=0.2, anchor="center")

        self.name_entry1 = tk.Entry(self.root, font=("Arial", 14), width=20, bg="#ada397")
        self.name_entry1.place(relx=0.5, rely=0.4, anchor="center")
        self.name_entry1.insert(0, "Player 1")

        start_button = tk.Button(self.root, text="Start Game", font=("Arial", 14), command=self.start_puzzles_with_names, bg="#ada397")
        start_button.place(relx=0.5, rely=0.7, anchor="center")

        back_button = tk.Button(self.root, text="Back", font=("Arial", 14), command=self.back_to_main_page, bg="#ada397")
        back_button.place(relx=0.5, rely=0.9, anchor="center")        

    def start_puzzle(self):
        self.index = 0
        """Initialize the game and render the chessboard."""
        self.clear_screen()
        self.canvas = tk.Canvas(self.root, width=480, height=520, bg="#ada397")
        self.canvas.pack(pady=25)
        label = tk.Label(self.root, text="Checkmate in 2!", font=("Arial", 16), bg="#ada397")
        label.place(relx=0.5, rely=0.02, anchor="center")

        
        # Get a random FEN and initialize the board
        random_puzzle = self.random_fen()
        fen = random_puzzle[0]
        solutions = random_puzzle[1]
        self.board = chess.Board(fen)
        # Render the board
        self.render_board()
        solutions=solutions.strip().split(' ')
        self.solutions = solutions
        print(self.solutions)
        self.canvas.bind("<Button-1>", lambda event: self.handle_puzzle_click(event, self.solutions))

        self.show_game_controls(mode="puzzle")

        


        # Show game controls (e.g., Reset, Back to Main Menu)


    def random_fen(self):
        random_puzzle_fen = random.choice(list(self.puzzles.keys()))
        solution = self.puzzles[random_puzzle_fen]
        return random_puzzle_fen, solution




    def show_instructions(self):
        """Show chess instructions in a messagebox."""
        instructions = (
            "Chess Game Instructions:\n\n"
            "1. The game is played on an 8x8 grid. Each player has 16 pieces: 8 pawns, 2 rooks, 2 knights, 2 bishops, 1 queen, and 1 king.\n"
            "2. The objective is to checkmate the opponent's king.\n"
            "3. Each player moves their pieces according to specific rules:\n"
            "   - Pawns move one square forward, but capture diagonally.\n"
            "   - Rooks move horizontally or vertically any number of squares.\n"
            "   - Knights move in an L-shape and can jump over other pieces.\n"
            "   - Bishops move diagonally any number of squares.\n"
            "   - Queens can move horizontally, vertically, or diagonally any number of squares.\n"
            "   - Kings move one square in any direction.\n"
            "4. A player wins by checkmating the opponent's king.\n"
            "5. The game ends in a draw if there is no way for either player to checkmate.\n"
            "6. For more detailed rules, refer to standard chess rulebooks."
        )
        messagebox.showinfo("Chess Instructions", instructions)

    def show_name_entry_1v1(self):
        """Display name entry screen for 1v1 mode."""
        self.is_1v1 = True
        self.show_name_entry_screen()

    def show_difficulty_selection(self):
        
        """Display difficulty selection screen for 1vAI mode."""
        self.clear_screen()
        self.load_background_image()

        label = tk.Label(self.root, text="Choose AI Difficulty", font=("Arial", 16), bg="#ada397")
        label.place(relx=0.5, rely=0.2, anchor="center")

        btn_easy = tk.Button(self.root, text="Easy", font=("Arial", 14), command=lambda: self.start_1vai("easy"), bg="#ada397")
        btn_easy.place(relx=0.5, rely=0.4, anchor="center")

        btn_medium = tk.Button(self.root, text="Medium", font=("Arial", 14), command=lambda: self.start_1vai("medium"), bg="#ada397")
        btn_medium.place(relx=0.5, rely=0.5, anchor="center")

        btn_hard = tk.Button(self.root, text="Hard", font=("Arial", 14), command=lambda: self.start_1vai("hard"), bg="#ada397")
        btn_hard.place(relx=0.5, rely=0.6, anchor="center")

        back_button = tk.Button(self.root, text="Back", font=("Arial", 14), command=self.show_mode_selection_screen, bg="#ada397")
        back_button.place(relx=0.5, rely=0.8, anchor="center")


    def show_name_entry_screen(self):
        """Display a screen to enter player names."""
        self.clear_screen()
        self.load_background_image()

        label = tk.Label(self.root, text="Enter Player Names", font=("Arial", 16), bg="#ada397")
        label.place(relx=0.5, rely=0.2, anchor="center")

        self.name_entry1 = tk.Entry(self.root, font=("Arial", 14), width=20, bg="#ada397")
        self.name_entry1.place(relx=0.5, rely=0.4, anchor="center")
        self.name_entry1.insert(0, "Player 1")

        if self.is_1v1:
            self.name_entry2 = tk.Entry(self.root, font=("Arial", 14), width=20, bg="#ada397")
            self.name_entry2.place(relx=0.5, rely=0.5, anchor="center")
            self.name_entry2.insert(0, "Player 2")

        start_button = tk.Button(self.root, text="Start Game", font=("Arial", 14), command=self.start_game_with_names, bg="#ada397")
        start_button.place(relx=0.5, rely=0.7, anchor="center")

        back_button = tk.Button(self.root, text="Back", font=("Arial", 14), command=self.back_to_main_page, bg="#ada397")
        back_button.place(relx=0.5, rely=0.9, anchor="center")


    def start_game_with_names(self):
        """Start the game with player names."""
        self.player1_name = self.name_entry1.get()
        if self.is_1v1:
            self.player2_name = self.name_entry2.get()
        self.captured_pieces = {self.player1_name: [], self.player2_name: [], "Computer": []}  # Captured pieces tracking
        self.start_game()

    def start_puzzles_with_names(self):
        """Start the game with player names."""
        self.player1_name = self.name_entry1.get()
        if self.is_1v1:
            self.player2_name = self.name_entry2.get()
        self.captured_pieces = {self.player1_name: [], self.player2_name: [], "Computer": []}  # Captured pieces tracking
        self.start_puzzle()

    def start_1vai(self, difficulty):
        """Start a 1vAI game with the selected difficulty.""" 
        self.is_1v1 = False
        self.ai_difficulty = difficulty
        self.show_name_entry_screen()

    def start_game(self):
        """Initialize the game and render the chessboard."""
        self.mode = "game"
        self.clear_screen()
        self.canvas = tk.Canvas(self.root, width=480, height=520, bg="#ada397")
        self.canvas.pack(pady=20)
        self.render_board()
        self.canvas.bind("<Button-1>", self.handle_click)

        # Show game controls (e.g., Reset, Back to Main Menu)
        self.show_game_controls()

    import tkinter as tk

    def show_game_controls(self, mode="game"):
        """Display game controls like Restart, Back to Main Page, and View Captured Pieces."""
        controls_frame = tk.Frame(self.root)
        controls_frame.pack(pady=20)
        if mode == "game":
            restart_button = tk.Button(controls_frame, text="Restart Game", font=("Arial", 14), command=self.restart_game, bg="#ada397")
            restart_button.pack(side="left", padx=10)

            captured_button = tk.Button(controls_frame, text="View Captured Pieces", font=("Arial", 14), command=self.show_captured_pieces, bg="#ada397")
            captured_button.pack(side="left", padx=10)

        if mode == "puzzle":
            restart_button = tk.Button(controls_frame, text="Another Puzzle", font=("Arial", 14), command=self.start_puzzle, bg="#ada397")
            restart_button.pack(side="left", padx=10)
        back_button = tk.Button(controls_frame, text="Back to Main Page", font=("Arial", 14), command=self.back_to_main_page, bg="#ada397")
        back_button.pack(side="right", padx=10)

        

    def show_captured_pieces(self):
        """Display the captured pieces in a styled popup window."""
        captured_window = tk.Toplevel(self.root)
        captured_window.title("Captured Pieces")
        captured_window.geometry("400x300")  # Define the size of the window
        captured_window.config(bg="#ada397")  # Light gray background color

        # Add a header with a title
        header_label = tk.Label(captured_window, text="Captured Pieces", font=("Arial", 16, "bold"), bg="#ada397")
        header_label.pack(pady=10)

        # Create a frame for the pieces display area
        pieces_frame = tk.Frame(captured_window, bg="#ada397")
        pieces_frame.pack(fill="both", expand=True)

        # Create a Canvas for horizontal scrolling
        canvas = tk.Canvas(pieces_frame, bg="#ada397")
        canvas.pack(side="left", fill="both", expand=True)

        # Create a horizontal scrollbar linked to the canvas
        scrollbar = tk.Scrollbar(pieces_frame, orient="horizontal", command=canvas.xview)
        scrollbar.pack(side="bottom", fill="x")

        # Configure the canvas to use the scrollbar
        canvas.config(xscrollcommand=scrollbar.set)

        # Create a frame within the canvas to hold the content
        content_frame = tk.Frame(canvas, bg="#ada397")
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        # Create a frame for each player's captured pieces
        if self.is_1v1:
            players = [self.player1_name, self.player2_name]
        else:
            players = [self.player1_name, "Computer"]

        for player in players:
            player_frame = tk.Frame(content_frame, bg="#ada397")
            player_frame.pack(pady=10, fill="x")

            # Label for the player
            player_label = tk.Label(player_frame, text=f"{player}:", font=("Arial", 14, "bold"), bg="#ada397")
            player_label.pack(side="top", anchor="w", padx=10)

            pieces_display_frame = tk.Frame(player_frame, bg="#ada397")
            pieces_display_frame.pack(fill="x", padx=10)

            # Add each captured piece's image
            for piece_symbol in self.captured_pieces.get(player, []):
                # Map piece symbols to their image keys
                color = "w" if piece_symbol.isupper() else "b"
                piece_key = f"{color}{piece_symbol.lower()}"
                if piece_key in self.piece_images:
                    piece_image = self.piece_images[piece_key]
                    piece_label = tk.Label(pieces_display_frame, image=piece_image, bg="#ada397")
                    piece_label.pack(side="left", padx=5, pady=5)

        # Update the scroll region to include all content
        content_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Create a close button at the bottom
        close_button = tk.Button(captured_window, text="Close", font=("Arial", 12), command=captured_window.destroy, bg="#6c7a89", fg="white")
        close_button.pack(pady=15)

        # Center the popup window
        self.center_window(captured_window, 400, 300)

    def center_window(self, window, width, height):
        """Center a window on the screen."""
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def restart_game(self):
        """Restart the game."""
        self.captured_pieces.clear()
        self.captured_pieces = {self.player1_name: [], self.player2_name: [], "Computer": []}  # Captured pieces tracking
        self.board.reset()
        self.render_board()

    def back_to_main_page(self):
        """Go back to the main page to choose the game mode."""
        self.board.reset()  # Reset the board state
        self.selected_square = None  # Reset selected square
        self.available_moves = []  # Clear available moves
        self.captured_pieces = {}  # Reset captured pieces
        self.clear_screen()  # Clear all widgets from the screen
        self.canvas.pack_forget()  # Hide the chessboard canvas
        self.show_mode_selection_screen()  # Show the main page


    def clear_screen(self):
        """Clear all widgets from the screen."""
        for widget in self.root.winfo_children():
            widget.destroy()
        # self.root.geometry("900x600")

    def render_board(self):
        """Render the chessboard and pieces on the canvas."""
        self.canvas.delete("all")
        square_size = 480 // 8
        for row in range(8):
            for col in range(8):
                color = "#edcbb7" if (row + col) % 2 == 0 else "#4f342e"
                x1 = col * square_size
                y1 = row * square_size
                x2 = x1 + square_size
                y2 = y1 + square_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)


        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                col = chess.square_file(square)
                row = 7 - chess.square_rank(square)
                x = col * square_size + square_size // 2
                y = row * square_size + square_size // 2
                piece_key = f"{'w' if piece.color == chess.WHITE else 'b'}{piece.symbol().lower()}"
                if piece_key in self.piece_images:
                    self.canvas.create_image(x, y, image=self.piece_images[piece_key])
        score = self.evaluate_board_simple()
        self.canvas.create_text(240, 500, text=f"Score: {score}", font=("Arial", 16), fill="black")


        # Highlight available moves
        for move in self.available_moves:
            to_square = move.to_square
            col = chess.square_file(to_square)
            row = 7 - chess.square_rank(to_square)
            x1 = col * square_size
            y1 = row * square_size
            x2 = x1 + square_size
            y2 = y1 + square_size
            if self.board.is_capture(move):  # Check if the move is a capture
                # Draw a highlight for captures
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="#260501", width=6)  # Red border highlight
            else:
                # Draw the oval for regular moves
                self.canvas.create_oval(x1 + 20, y1 + 20, x2 - 20, y2 - 20, fill="#331b04")


    def handle_click(self, event):
        """Handle mouse clicks for selecting and moving pieces."""
        square_size = 480 // 8
        col = event.x // square_size
        row = 7 - (event.y // square_size)
        clicked_square = chess.square(col, row)

        if self.selected_square is None:
            # Select a piece
            piece = self.board.piece_at(clicked_square)
            if piece and piece.color == self.board.turn:
                self.selected_square = clicked_square
                self.available_moves = [move for move in self.board.legal_moves if move.from_square == clicked_square]
                self.render_board()
        else:
            move = chess.Move(self.selected_square, clicked_square)
            if self.is_pawn_promotion(move):
                move.promotion = chess.QUEEN  
                if move in self.board.legal_moves:
                    self.prompt_pawn_promotion(move)
            else:
                self.attempt_move(move)

    def handle_puzzle_click(self, event, right_move):
        """Handle mouse clicks for selecting and moving pieces."""
        square_size = 480 // 8
        col = event.x // square_size
        row = 7 - (event.y // square_size)
        clicked_square = chess.square(col, row)

        if self.selected_square is None:
            # Select a piece
            piece = self.board.piece_at(clicked_square)
            if piece and piece.color == self.board.turn:
                self.selected_square = clicked_square
                self.available_moves = [move for move in self.board.legal_moves if move.from_square == clicked_square]
                self.render_board()
        else:
            move = chess.Move(self.selected_square, clicked_square)
            move_san = self.convert_to_san(move, self.board)
            print(self.index)
            if right_move[self.index] == move_san:
                if self.index == 0:
                    messagebox.showinfo("wadyyyyy","3ash👏")
                elif self.index == 2:
                    messagebox.showinfo("wadyyyyy","bravoooo, YOU SOLVED IT!!🎉")
                self.index += 2
                if move in self.board.legal_moves and self.is_pawn_promotion(move):
                    self.prompt_pawn_promotion(move)
                else:
                    self.attempt_move(move)
            elif move in self.board.legal_moves:
                messagebox.showinfo("hahahahaha","8alat hehe😛")
                self.selected_square = None
                self.available_moves = []
                self.render_board()
            else:
                self.selected_square = None
                self.available_moves = []
                self.render_board()


    def convert_to_san(self, move_notation, board):
        # Create a chess Move object from the move notation (like 'e2e4')
        move = move_notation
        
        # Ensure the move is legal on the current board
        if move in board.legal_moves:
            # Return the SAN (Standard Algebraic Notation) of the move
            return board.san(move)
        else:
            return None  # Return None if the move is illegal

    def attempt_move(self, move, mode="game"):
        """Attempt to make a move; validate and handle promotion."""
        if move in self.board.legal_moves:
            self.execute_move(move)
        elif move.promotion:
            # Handle promotion with correct flag
            promotion_move = chess.Move(move.from_square, move.to_square, promotion=move.promotion)
            if promotion_move in self.board.legal_moves:
                self.execute_move(promotion_move)
        else:
            # Deselect if invalid move
            self.selected_square = None
            self.available_moves = []
            self.render_board()

    def execute_move(self, move):
        """Execute a move on the board."""
        captured_piece = self.board.piece_at(move.to_square)
        if captured_piece:
            self.add_captured_piece(captured_piece)

        self.board.push(move)
        self.selected_square = None
        self.available_moves = []
        self.render_board()

        # Check if the player's king is in check after the move
        if self.is_1v1:  # Corrected to self.is_1v1
            if self.board.is_check():
                self.show_king_in_check_popup()
        else:
            if self.board.is_check() and self.board.turn == chess.WHITE:  # Only show popup if it's the player's turn and their king is in check
                self.show_king_in_check_popup()

        # Check for game over
        if self.board.is_game_over():
            self.show_game_over()
            return

        if not self.is_1v1:
            self.root.after(1, self.ai_move) 


    def show_king_in_check_popup(self):
        """Display a popup informing the player their king is in check."""
        messagebox.showinfo("check!","king is in check! You must move the king or defend it.")

    def is_pawn_promotion(self, move):
        """Check if a move is a pawn promotion."""
        piece = self.board.piece_at(move.from_square)
        if piece and piece.piece_type == chess.PAWN:
            if (piece.color == chess.WHITE and chess.square_rank(move.to_square) == 7) or \
                (piece.color == chess.BLACK and chess.square_rank(move.to_square) == 0):
                return True
        return False

    def prompt_pawn_promotion(self, move):
        move = chess.Move(move.from_square, move.to_square)
        if self.is_pawn_promotion(move):
            """Prompt the user to select a piece for pawn promotion."""
            promotion_window = tk.Toplevel(self.root)
            promotion_window.title("Promote Pawn")
            promotion_window.geometry("250x200")  # Fixed size for better display
            promotion_window.resizable(False, False)  # Prevent resizing

            label = tk.Label(promotion_window, text="Promote pawn to:", font=("Arial", 14))
            label.grid(row=0, column=0, columnspan=2, pady=10)

            piece_types = [
                ('Q', chess.QUEEN),
                ('R', chess.ROOK),
                ('B', chess.BISHOP),
                ('N', chess.KNIGHT)
            ]

            def promote(piece_type):
                move.promotion = piece_type[1]  # Set the promotion type
                self.execute_move(move)  # Execute the promotion move
                promotion_window.destroy()

            # Place buttons in a 2x2 grid layout
            for idx, (piece_type) in enumerate(piece_types):
                row = (idx // 2) + 1  # Top row (1) or bottom row (2)
                col = idx % 2         # Left column (0) or right column (1)
                image_path = "w"+piece_type[0]+".png"
                try:
                    image = Image.open(image_path)
                    image_resized = image.resize((60, 60))  # Resize the image to fit the button size
                    
                    # Convert to PhotoImage
                    photo_image = ImageTk.PhotoImage(image_resized)
                    
                    # Create the button and assign the image
                    button = tk.Button(promotion_window, image=photo_image, command=lambda pt=piece_type: promote(pt), bg="#ada397")
                    button.grid(row=row, column=col, padx=10, pady=5)
                    
                    # Keep a reference to the photo_image to prevent garbage collection
                    button.image = photo_image  # This stores the image reference in the button
                    
                except FileNotFoundError:
                    print(f"Error: The file {image_path} was not found.")

            # Center the popup window
            self.center_window(promotion_window, 250, 200)
        else:
            # Deselect if invalid move
            self.selected_square = None
            self.available_moves = []
            self.render_board()


    def add_captured_piece(self, captured_piece):
        """Add captured piece to the list of captured pieces."""
        if self.board.turn == chess.WHITE:
            self.captured_pieces[self.player1_name].append(captured_piece.symbol())
        else:
            if self.is_1v1:
                self.captured_pieces[self.player2_name].append(captured_piece.symbol())
            else:
                self.captured_pieces["Computer"].append(captured_piece.symbol())

    def ai_move(self):
        """Make an AI move based on difficulty."""
        # Check for a book move first
        book_move = self.get_book_move(self.board, self.opening_book)
        

        # No book move available, use AI logic
        if self.ai_difficulty == 'easy':
            move = self.easy_move()
        elif self.ai_difficulty == 'medium':
            if book_move:
                print(f"Book move: {book_move}")
                move = chess.Move.from_uci(book_move)  # Convert UCI string to a move object
            else:
                start_time = time.time()
                move = self.minimax_move(depth=4)
                end_time = time.time()
                print(f"Minimax (medium) took {end_time - start_time:.2f} seconds")
        else:
            if book_move:
                print(f"Book move: {book_move}")
                move = chess.Move.from_uci(book_move)  # Convert UCI string to a move object
            else:
                start_time = time.time()
                move = self.minimax_move(depth=5)
                end_time = time.time()
                print(f"Minimax (hard) took {end_time - start_time:.2f} seconds")

        # Handle captured pieces
        captured_piece = self.board.piece_at(move.to_square)
        if captured_piece:
            self.add_captured_piece(captured_piece)

        # Push the move to the board
        self.board.push(move)

        self.render_board()
        if self.board.is_game_over():
            self.show_game_over()
            return


    def easy_move(self):
        """AI makes a move using a simple heuristic for easy difficulty."""
        best_move = None
        best_value = float('-inf')

        for move in self.board.legal_moves:
            self.board.push(move)
            value = self.evaluate_board_simple()
            self.board.pop()

            if value > best_value:
                best_value = value
                best_move = move

        return best_move

    def evaluate_board_simple(self):
        """Simple evaluation function for easy AI."""
        piece_values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0}
        value = 0

        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                if piece.color == chess.WHITE:  # AI favors White
                    value += piece_values[piece.symbol().upper()]
                else:
                    value -= piece_values[piece.symbol().upper()]

        return value   

    def sorting_moves(self):
        capture_moves = []
        non_capture_moves = []
        checkmate_moves = []
        for move in self.board.legal_moves:
            if self.is_checkmate_move(move):
                checkmate_moves.append(move)
            elif self.is_capture_move(move):
                capture_moves.append(move)
            else:
                non_capture_moves.append(move)

    # Combine the categorized moves
        moves = checkmate_moves + capture_moves + non_capture_moves
        return moves


    def is_capture_move(self, move):
        """
        Check if the move captures a piece.
        
        :param move: The move to be checked (of type chess.Move).
        :return: True if the move captures a piece, False otherwise.
        """     

        # If there's a piece at the destination square and it's of the opposite color, it's a capture
        if (self.board.piece_at(move.to_square) is not None and self.board.piece_at(move.to_square).color != self.board.turn):
            return True
        return False

    def is_checkmate_move(self, move):
        """
        Check if the move leads to checkmate.
        
        :param move: The move to be checked (of type chess.Move).
        :return: True if the move leads to checkmate, False otherwise.
        """
        # Push the move onto the board
        self.board.push(move)
        
        # Check if it results in checkmate
        is_checkmate = self.board.is_checkmate()
        
        # Undo the move to restore the original board state
        self.board.pop()
        
        return is_checkmate



    def minimax_move(self, depth):
        best_move = None
        best_score = -float('inf')
        alpha = -float('inf')
        beta = float('inf')

        # Adjust the search depth based on the material situation
        if self.is_low_material(self.board, 10, 2) or self.is_low_material(self.board, 2, 1):
            depth += 1  # Increase depth when the material is low to search more thoroughly'
            print(f"Adjusted depth: {depth}")

        # if self.is_low_material(self.board, 2):
        #     depth += 1  # Increase depth when the material is low to search more thoroughly'
        #     print(f"Adjusted depth: {depth}")

        
        # Categorize moves

        fen = self.board.fen()
        if fen in self.transposition_table:
            stored_score, stored_depth = self.transposition_table[fen]

            # If the stored depth is greater than or equal to the current depth, return the stored score
            if stored_depth >= depth:
                print(f"Using stored score {stored_score} for FEN {fen} at depth {depth}")
                return stored_score

        capture_moves = []
        non_capture_moves = []
        for move in self.board.legal_moves:
            if self.is_capture_move(move):
                capture_moves.append(move)
            else:
                non_capture_moves.append(move)

        # Evaluate capture moves with full depth
        for move in capture_moves :
            capturing_piece = self.board.piece_at(move.from_square)
            captured_piece = self.board.piece_at(move.to_square)

            capturing_value = self.get_piece_value(capturing_piece)
            captured_value = self.get_piece_value(captured_piece)

            # If the capturing piece is lower value than the captured piece, play it immediately
            if captured_value > capturing_value:
                print(f"Automatically playing favorable capture: {move}")
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

        # Transposition table lookup
        if fen in self.transposition_table:
            stored_score, stored_depth = self.transposition_table[fen]

            # If the stored depth is less than the current depth, continue searching deeper
            if stored_depth >= depth:
                return stored_score
            else:
                # Subtract the difference between current depth and stored depth and continue search
                print(f"Stored depth {stored_depth} is less than current depth {depth}")
                alpha = max(alpha, stored_score)
                beta = min(beta, stored_score)  # Update beta to prevent worse moves for minimizing
                new_depth = max(1, depth - stored_depth)  # Ensure positive depth
                return self.minimax(new_depth, is_maximizing, alpha, beta)

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

        # Store result in transposition table
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
                    material_score += self.get_piece_value(piece)*100
                    positional_score += self.get_positional_value(piece, square, endgame)
                else:
                    material_score -= self.get_piece_value(piece)*100
                    positional_score -= self.get_positional_value(piece, square, endgame)


        if self.board.is_check():
            material_score += 200 if self.board.turn == chess.WHITE else -200
        return material_score+positional_score

    def is_low_material(self, board, num, players=2):
        """Check if the player has low material."""
        if players == 2:
            piece_count = sum(1 for square in chess.SQUARES if board.piece_at(square))
        else:
            piece_count = sum(1 for square in chess.SQUARES if board.piece_at(square) and board.piece_at(square).color == chess.WHITE)
        # If there are fewer than a certain number of pieces left on the board, consider it low material
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

    # def is_checkmate_threat(self):
    #     """Detect if there is a checkmate threat for the opponent."""
    #     # This is a placeholder for the logic to detect checkmate threats. You can expand this.
    #     return self.board.is_check() and len(list(self.board.legal_moves)) == 1


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
    
    def show_game_over(self):
        """Handle game-over scenarios."""
        result = "Game Over!\n"
        if self.board.is_checkmate():
            winner = self.player1_name if self.board.turn == chess.BLACK else (
                self.player2_name if self.is_1v1 else "Computer"
            )
            result += f"{winner} wins by checkmate!"
        elif self.board.is_stalemate():
            result += "The game is a draw due to stalemate."
        elif self.board.is_insufficient_material():
            result += "The game is a draw due to insufficient material."
        else:
            result += "The game is a draw."
        if self.mode == "game":
            messagebox.showinfo("Game Over", result)
        self.back_to_main_page()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = ChessApp(root)
    root.mainloop()
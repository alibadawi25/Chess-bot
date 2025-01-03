


# Function to filter the dictionary
def filter_three_move_puzzles(puzzles):
    # Create a new dictionary with solutions that have exactly three moves
    filtered_puzzles = {fen: solution for fen, solution in puzzles.items() 
                        if len(solution.strip().split(" ")) == 3}
    return filtered_puzzles

# Example usage
if __name__ == "__main__":
    # Replace 'puzzles' with your actual dictionary
    puzzles = {
            "4r1rk/5K1b/7R/R7/8/8/8/8 w - - 0 1": " Rxh7+ Kxh7 Rh5# ",
            "8/1r6/8/3R4/k7/p1K5/4r3/R7 w - - 0 1": " Rxa3+ Kxa3 Ra5# ",
            "6k1/8/6K1/8/8/3r4/4r3/5R1R w - - 0 1": " Rh8+ Kxh8 Rf8# ",
            "2rkr3/2ppp3/2n1n3/R2R4/8/8/3K4/8 w - - 0 1": " Rxd7+ Kxd7 Rd5# ",
            "4rkr1/1R1R4/4bK2/8/8/8/8/8 w - - 0 1": " Rf7+ Bxf7 Rxf7# ",
            "5K1k/6pp/7R/8/8/8/8/6R1 w - - 0 1": " Rgg6 gxh6 Rg8# ",
            "2k5/1q4b1/3K4/8/7R/8/7R/8 w - - 0 1": " Rh8+ Bxh8 Rxh8# ",
            "8/8/q5b1/7k/5Kp1/1R1R4/8/8 w - - 0 1": " Rh3+ gxh3 Rxh3# ",
            "k7/3b4/1K6/8/8/5q2/2R1R3/8 w - - 0 1": " Re8+ Bxe8 Rc8# ",
            "8/1R1R4/8/p7/k1K5/r5r1/8/8 w - - 0 1": " Rb4+ axb4 Ra7# ",
            "kr6/1p6/8/1p5R/6R1/8/1r6/5K2 w - - 0 1": " Ra4+ bxa4 Ra5# ",
            "6R1/8/8/7p/5K1k/r6r/8/6R1 w - - 0 1": " R1g4+ hxg4 Rh8# ",
            "kb6/p4q2/2K5/8/8/8/8/1R1R4 w - - 0 1": " Rxb8+ Kxb8 Rd8# ",
            "8/6p1/6rk/6np/R6R/6K1/8/8 w - - 0 1": " Rxh5+ Kxh5 Rh4# ",
            "kn1R4/ppp5/2q5/8/8/8/8/3RK3 w - - 0 1": " Rxb8+ Kxb8 Rd8# ",
            "1kb4R/1npp4/8/8/8/8/8/R5K1 w - - 0 1": " Rxc8+ Kxc8 Ra8# ",
            "8/8/1b6/kr6/pp6/1n6/7R/R3K3 w Q - 0 1": " Rxa4+ Kxa4 Ra2# ",
            "5K1k/7p/8/2p5/2rp4/8/p7/1B4B1 w - - 0 1": " Bh2 axb8/Q Be5# ",
            "k7/p7/B2K4/8/8/8/3p2p1/4B3 w - - 0 1": " Kc7 dxe1/Q Bb7# ",
            "8/5n2/8/6B1/8/4K3/7p/5B1k w - - 0 1": " Kf2 Nxg5 Bg2# ",
            "8/5p2/7p/5Kpk/4BB1p/7r/8/8 w - - 0 1": " Bd5 gxf4 Bxf7# ",
            "8/6N1/8/pp6/kp6/pp5K/2N5/8 w - - 0 1": " Ne6 bxc2 Nc5# ",
            "8/8/8/7N/8/8/1p5p/N3K2k w - - 0 1": " Kf2 bxa1/Q Ng3# ",
            "4K3/8/8/4N1pr/4b1pk/4N1nr/8/8 w - - 0 1": " Ng2+ Bxg2 Ng6# ",
            "k7/ppK5/2N5/3N4/8/8/7p/8 w - - 0 1": " Kc8 bxc6 Nc7# ",
            "7k/4K1pp/6pn/6N1/6N1/8/8/8 w - - 0 1": " Kf8 Nxg4 Nf7# ",
            "8/8/7p/5K1k/7p/8/2pn1N2/3N4 w - - 0 1": " Nh3 cxd1/Q Nf4# ",
            "7k/6pp/5P1P/8/8/8/1p3K2/8 w - - 0 1": " f7 w/f8/Q# ",
            "8/4PKPk/5n1p/4b3/8/8/p7/q7 w - - 0 1": " e8/Q+ Nxe8 g8/Q# ",
            "2b5/7P/4Pp2/7p/5K1k/7p/p6n/8 w - - 0 1": " h8/N a1/Q Ng6# ",
            "1k1B4/8/1K6/1n6/q7/8/8/3R4 w - - 0 1": " Bc7+ Nxc7 Rd8# ",
            "7k/B7/6K1/8/8/2b5/7r/R7 w - - 0 1": " Bd4+ Bxd4 Ra8+ ",
            "6Bk/R4K2/8/8/8/8/8/8 w - - 0 1": " Kg6 Kxg8 Ra8# ",
            "5Knk/7b/R7/8/7B/8/8/8 w - - 0 1": " Rh6 Nxh6 Bf6# ",
            "7k/5ppr/K5p1/8/8/8/2B5/2R5 w - - 0 1": " Bxg6 fxg6 Rc8# ",
            "6B1/p1K5/k7/pp6/8/8/8/R7 w - - 0 1": " Ra4 bxa4 Bc4# ",
            "8/8/7p/5K1k/6pp/1R6/B4n1r/8 w - - 0 1": " Rh3 w/Bf7# ",
            "r7/kp6/pR1Q4/5q2/8/8/8/3K4 w - - 0 1": " Rxa6+ bxa6 Qc7# ",
            "4Q3/kr6/pp6/8/8/8/6q1/R2K4 w - - 0 1": " Rxa6+ Kxa6 Qa4# ",
            "6rk/6n1/1R1Q4/7r/8/8/8/3K4 w - - 0 1": " Qh6+ Rxh6 Rxh6# ",
            "1k4r1/ppp5/8/8/2q5/8/5Q2/3K1R2 w - - 0 1": " Qf8+ Rxf8 Rxf8# ",
            "3R4/2q5/8/rpn5/kp5Q/2n5/1K6/8 w - - 0 1": " Qxb4+ Kxb4 Rd4# ",
            "1q1r3k/7p/7K/8/4R3/2p5/8/1Q6 w - - 0 1": " Re8+ Rxe8 Qxh7# ",
            "kr6/1p6/p5R1/8/1q6/8/Q7/2K5 w - - 0 1": " Rxa6+ bxa6 Qxa6# ",
            "k7/p2bR3/Q7/8/3q4/8/8/2K5 w - - 0 1": " Re8+ Bxe8 Qc8# ",
            "k3r3/pR6/K7/2b5/8/8/1Q3q2/8 w - - 0 1": " Rxa7+ Bxa7 Qb7# ",
            "3rkr2/R3p3/8/4K3/8/7Q/5q2/8 w - - 0 1": " Rxe7+ Kxe7 Qe6# ",
            "2k5/1ppn4/1q6/8/Q7/8/5R2/4K3 w - - 0 1": " Rf8+ Nxf8 Qe8# ",
            "k1r5/p1p5/N1K5/8/3q4/8/8/1R6 w - - 0 1": " Rb8+ Rxb8 Nxc7# ",
            "8/8/6Nr/5Kbk/R7/8/8/8 w - - 0 1": " Rh4+ Bxh4 Nf4# ",
            "kr6/pp6/8/8/2N4R/8/8/3K4 w - - 0 1": " Nb6+ axb6 Ra4# ",
            "4nrkr/5pp1/8/7N/8/8/8/3K2R1 w - - 0 1": " Rxg7+ Nxg7 Nf6# ",
            "2Nnkr2/3p3R/8/5n2/8/8/8/7K w - - 0 1": " Re7+ Nxe7 Nd6# ",
            "2R5/8/pn6/k1N5/8/1K6/6q1/8 w - - 0 1": " Nb7+ Qxb7 Rc5# ",
            "5Kbk/R7/4q1P1/8/8/8/8/8 w - - 0 1": " Rh7+ Bxh7 g7# ",
            "5Kbk/6pp/6pR/5P2/8/8/8/8 w - - 0 1": " fxg6 gxh6 g7# ",
            "3k4/1P6/3K4/8/8/8/1q6/7R w - - 0 1": " Rh8+ Qh8 b8/Q# ",
            "8/8/6rp/6pk/5b1p/5K2/6P1/6R1 w - - 0 1": " g4+ hxg3 e.p. Rh1# ",
            "qkb5/4p3/1K1p4/8/5Q2/6B1/8/8 w - - 0 1": " Qxd6+ exd6 Bxd6# ",
            "B7/8/8/7K/4b3/Q7/7p/1q4bk w - - 0 1": " Qf3+ Bxf3 Bxf3# ",
            "8/8/B7/3qp3/2ppkpp1/8/4K3/3Q4 w - - 0 1": " Qd3+ cxd3+ Bxd3# ",
            "6bk/7p/7K/4N3/8/8/7B/8 w - - 0 1": " Ng6+ hxg6 Be5# ",
            "5K1k/6pp/6p1/6B1/6N1/8/8/8 w - - 0 1": " Nh6 gxh6 Bf6# ",
            "8/8/5B2/8/2pN4/K7/pp6/kb6 w - - 0 1": " Nb3+ cxb3 Bxb2# ",
            "kbK5/p7/2pN4/3p4/8/8/8/5B2 w - - 0 1": " Ba6 Bxd6 Bb7# ",
            "7B/8/pb6/kpn5/b1p5/1P6/1K6/8 w - - 0 1": " b4+ Kxb4 Bc3# ",
            "kb1n4/8/KP6/8/B7/8/8/8 w - - 0 1": " Bc6+ Nxc6 b7# ",
            "3B1K1k/6pp/4b3/7P/8/8/8/8 w - - 0 1": " h6 gxh6 Bf6# ",
            "8/8/8/6pp/5p1k/5K1b/5P1B/8 w - - 0 1": " Bg3+ fxg3 fxg3# ",
            "k1r2q2/ppQ5/N7/8/8/8/8/3K4 w - - 0 1": " Qb8+ Rxb8 Nc7# ",
            "4q2k/4N1pr/8/8/2Q5/8/4K3/8 w - - 0 1": " Qg8+ Qxg8 Ng6# ",
            "rknN4/2p5/1rQ5/8/8/8/1q6/3K4 w - - 0 1": " Qb7+ Rxb7 Nc6# ",
            "4r1kr/5b1p/5KN1/8/8/Q7/3q4/8 w - - 0 1": " Qf8+ Rxf8 Ne7# ",
            "7k/4NKpp/4Q3/8/8/2q2p2/8/6r1 w - - 0 1": " Ng6+ hxg6 Qh3# ",
            "k1b5/8/NKn5/8/4q3/8/7Q/8 w - - 0 1": " Qb8+ Nxb8 Nc7# ",
            "k4K2/p7/1bP5/8/8/8/8/6qQ w - - 0 1": " c7+ Qxh1 c8/Q# ",
            "5rkr/5ppp/8/4K3/6N1/2Q5/q7/8 w - - 0 1": " Nh6+ gxh6 Qg3# ",
            "krQ5/p7/8/4q3/N7/8/8/3K4 w - - 0 1": " Nb6+ axb6 Qa6# ",
            "8/1q6/4NQ1r/5npk/8/7K/8/6r1 w - - 0 1": " Qxg5+ Rxg5 Nf4# ",
            "k1r5/p1pq4/Qp1p4/8/3N4/8/3K4/8 w - - 0 1": " Nc6 Qxc6 Qxc8# ",
            "3q2rk/5Q1p/6bK/4N3/8/8/8/8 w - - 0 1": " Qxh7+ Bxh7 Nf7# ",
            "8/8/5Q2/2q3pk/7b/8/4K1P1/8 w - - 0 1": " g4+ Kxg4 Qf3# ",
            "8/b2Q4/kp2p3/p2q4/1P6/K7/8/8 w - - 0 1": " b5+ Qxb5 Qc8# ",
            "8/8/8/pq6/kpp5/7Q/K1P5/8 w - - 0 1": " Qb3+ cxb3+ cxb3# ",
            "5K1k/7b/8/4ppP1/8/6bQ/7q/8 w - - 0 1": " g6 Qxh3 g7# ",
            "1K2kb2/4p3/5P2/5Q1q/7r/8/8/8 w - - 0 1": " f7+ w/Qc8# ",
            "k7/p1K2n2/p7/3p1r2/8/8/8/2R5 w - - 0 1": " Rb1 ",
            "4k3/2r1p1p1/3pK3/8/8/8/8/5R2 w - - 0 1": " Rh1 ",
            "7k/6R1/6Kn/8/8/8/8/8 w - - 0 1": " Re7 ",
            "6qk/8/7K/7Q/8/8/8/8 w - - 0 1": " Qe5+ ",
            "8/p7/kPK5/p7/n7/8/8/8 w - - 0 1": " b7 Nc3 b8/N# ",
            "2b1kb2/4p3/2K5/8/8/8/8/3BB3 w - - 0 1": " Bh5+ ",
            "8/8/6nq/3p2b1/7k/7p/5Kpp/3BB3 w - - 0 1": " Kf3+ Kh5 Kg3# ",
            "8/6nk/3N2n1/8/4N3/8/8/K7 w - - 0 1": " Nf6+ ",
            "kn6/1n2N3/8/3N4/8/8/8/7K w - - 0 1": " Nc7+ ",
            "5nk1/4K1n1/8/4N3/6N1/8/8/8 w - - 0 1": " Nf6+ ",
            }


    # Get the filtered puzzles
    filtered_puzzles = filter_three_move_puzzles(puzzles)

    # Print the result in a format suitable for copy-pasting
    print("self.puzzles = {")
    for fen, solution in filtered_puzzles.items():
        print(f'    "{fen}": "{solution.strip()}",')
    print("}")

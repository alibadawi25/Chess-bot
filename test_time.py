import re


string = """a)
4r1rk/5K1b/7R/R7/8/8/8/8 w - - 0 1
[ Rxh7+ Kxh7 Rh5# ]

b) 
8/1r6/8/3R4/k7/p1K5/4r3/R7 w - - 0 1
[ Rxa3+ Kxa3 Ra5# ]

c) 
6k1/8/6K1/8/8/3r4/4r3/5R1R w - - 0 1
[ Rh8+ Kxh8 Rf8# ]

d) 
2rkr3/2ppp3/2n1n3/R2R4/8/8/3K4/8 w - - 0 1
[ Rxd7+ Kxd7 Rd5# ]

e) 
4rkr1/1R1R4/4bK2/8/8/8/8/8 w - - 0 1
[ Rf7+ Bxf7 Rxf7# ]

1b) 

Mate in 2 puzzles, Part II.
a) 
5K1k/6pp/7R/8/8/8/8/6R1 w - - 0 1
[ Rgg6 gxh6 Rg8# ]

b) 
2k5/1q4b1/3K4/8/7R/8/7R/8 w - - 0 1
[ Rh8+ Bxh8 Rxh8# ]

c) 
8/8/q5b1/7k/5Kp1/1R1R4/8/8 w - - 0 1
[ Rh3+ gxh3 Rxh3# ]

d) 
k7/3b4/1K6/8/8/5q2/2R1R3/8 w - - 0 1
[ Re8+ Bxe8 Rc8# ]

e) 
8/1R1R4/8/p7/k1K5/r5r1/8/8 w - - 0 1
[ Rb4+ axb4 Ra7# ]

2e) 

Mate in 2 puzzles, Part III.
a) 
kr6/1p6/8/1p5R/6R1/8/1r6/5K2 w - - 0 1
[ Ra4+ bxa4 Ra5# ]

b) 
6R1/8/8/7p/5K1k/r6r/8/6R1 w - - 0 1
[ R1g4+ hxg4 Rh8# ]

c) 
4R3/8/5K2/7p/R5pk/5npr/8/8 w - - 0 1
[ Rxg4+ if hxg4 Rh8# or if Kxg4 Re4# ]

d) 
kb6/p4q2/2K5/8/8/8/8/1R1R4 w - - 0 1
[ Rxb8+ Kxb8 Rd8# ]

e) 
8/6p1/6rk/6np/R6R/6K1/8/8 w - - 0 1
[ Rxh5+ Kxh5 Rh4# ]

3b) 

Mate in 2 puzzles, Part IV.
a) 
kn1R4/ppp5/2q5/8/8/8/8/3RK3 w - - 0 1
[ Rxb8+ Kxb8 Rd8# ]

b) 
1kb4R/1npp4/8/8/8/8/8/R5K1 w - - 0 1
[ Rxc8+ Kxc8 Ra8# ]

c) 
8/8/1b6/kr6/pp6/1n6/7R/R3K3 w Q - 0 1
[ Rxa4+ Kxa4 Ra2# ]

d) 
5K1k/7p/8/2p5/2rp4/8/p7/1B4B1 w - - 0 1
[ Bh2 axb8/Q Be5# ]

e) 
k7/p7/B2K4/8/8/8/3p2p1/4B3 w - - 0 1
[ Kc7 dxe1/Q Bb7# ]

4b) 

Mate in 2 puzzles, Part V.
a) 
8/5n2/8/6B1/8/4K3/7p/5B1k w - - 0 1
[ Kf2 Nxg5 Bg2# ]

b) 
8/5p2/7p/5Kpk/4BB1p/7r/8/8 w - - 0 1
[ Bd5 gxf4 Bxf7# ]

c) 
8/6N1/8/pp6/kp6/pp5K/2N5/8 w - - 0 1
[ Ne6 bxc2 Nc5# ]

d) 
8/8/8/7N/8/8/1p5p/N3K2k w - - 0 1
[ Kf2 bxa1/Q Ng3# ]

e) 
4K3/8/8/4N1pr/4b1pk/4N1nr/8/8 w - - 0 1
[ Ng2+ Bxg2 Ng6# ]

5b) 

Mate in 2 puzzles, Part VI.
a) 
k7/ppK5/2N5/3N4/8/8/7p/8 w - - 0 1
[ Kc8 bxc6 Nc7# ]

b) 
7k/4K1pp/6pn/6N1/6N1/8/8/8 w - - 0 1
[ Kf8 Nxg4 Nf7# ]

c) 
8/8/7p/5K1k/7p/8/2pn1N2/3N4 w - - 0 1
[ Nh3 cxd1/Q Nf4# ]

d) 
7k/6pp/5P1P/8/8/8/1p3K2/8 w - - 0 1
[ f7 w/f8/Q# ]

e) 
7k/5P2/4n1PK/8/8/8/8/8 w - - 0 1
[ g7+ Nxg7 f8/Q# (or f8/R#) ]

6b) 

Mate in 2 puzzles, Part VII.
a) 
k7/pn6/p1Pp4/4P3/8/8/8/6K1 w - - 0 1
[ c7 if dxe5 c8/Q# (or c8/R#) ]

b) 
8/4PKPk/5n1p/4b3/8/8/p7/q7 w - - 0 1
[ e8/Q+ Nxe8 g8/Q# ]

c) 
r1k5/P7/2K1P3/8/8/8/8/8 w - - 0 1
[ e7 Rxa7 e8/Q# (or e8/R#) ]

d) 
3k1r2/1P3P2/8/3K4/8/8/8/8 w - - 0 1
[ Kd6 Rxf7 b8/Q# (or b8/R#) ]

e) 
8/8/2P5/8/4p2p/p4Ppk/6p1/6K1 w - - 0 1
[ c7 exf3 c8/Q# (or c8/B#) ]

7a) 

Mate in 2 puzzles, Part VIII.
a) 
2b5/7P/4Pp2/7p/5K1k/7p/p6n/8 w - - 0 1
[ h8/N a1/Q Ng6# ]

b) 
1k1B4/8/1K6/1n6/q7/8/8/3R4 w - - 0 1
[ Bc7+ Nxc7 Rd8# ]

c) 
7k/B7/6K1/8/8/2b5/7r/R7 w - - 0 1
[ Bd4+ Bxd4 Ra8+ ]

d) 
6Bk/R4K2/8/8/8/8/8/8 w - - 0 1
[ Kg6 Kxg8 Ra8# ]

e) 
kb6/6n1/K7/5p2/4p3/8/8/4R2B w - - 0 1
[ Rxe4 if fxe4 Bxe4# or if f4 Rxf4# ]

8d) 

Mate in 2 puzzles, Part IX.
a) 
5Knk/7b/R7/8/7B/8/8/8 w - - 0 1
[ Rh6 Nxh6 Bf6# ]

b) 
8/8/8/6nr/4nB1k/8/6K1/5R2 w - - 0 1
[ Bg3+ if Nxg3 Rf4# or if Kg4 Rf4# ]

c) 
7k/5ppr/K5p1/8/8/8/2B5/2R5 w - - 0 1
[ Bxg6 fxg6 Rc8# ]

d) 
7k/7p/5K1b/8/6R1/8/1B6/1q6 w - - 0 1
[ Kf7+ if Qxb2 Rg8# or if Bb7 Bxg7# ]

e) 
6B1/p1K5/k7/pp6/8/8/8/R7 w - - 0 1
[ Ra4 bxa4 Bc4# ]

9a) 

Mate in 2 puzzles, Part X.
a) 
8/8/pp6/kb2B3/4n3/K1R5/8/8 w - - 0 1
[ Rc5 if Nxc5 Bc3# or if bxc5 Bc7# ]

b) 
k7/pbK5/8/1B2n3/8/8/6p1/1R6 w - - 0 1
[ Ba6 if g1/Q Bxb7# or if Bxa6 Rb8# ]

c) 
8/8/7p/5K1k/6pp/1R6/B4n1r/8 w - - 0 1
[ Rh3 w/Bf7# ]

d) 
r7/kp6/pR1Q4/5q2/8/8/8/3K4 w - - 0 1
[ Rxa6+ bxa6 Qc7# ]

e) 
4Q3/kr6/pp6/8/8/8/6q1/R2K4 w - - 0 1
[ Rxa6+ Kxa6 Qa4# ]

10e) 

Mate in 2 puzzles, Part XI.
a) 
6rk/6n1/1R1Q4/7r/8/8/8/3K4 w - - 0 1
[ Qh6+ Rxh6 Rxh6# ]

b) 
1k4r1/ppp5/8/8/2q5/8/5Q2/3K1R2 w - - 0 1
[ Qf8+ Rxf8 Rxf8# ]

c) 
3R4/2q5/8/rpn5/kp5Q/2n5/1K6/8 w - - 0 1
[ Qxb4+ Kxb4 Rd4# ]

d) 
5Q2/pp6/kp1R4/8/K7/8/4q3/8 w - - 0 1
[ Rxb6+ if Kxb6 Qd6# or if axb6 Qa8# ]

e) 
1q1r3k/7p/7K/8/4R3/2p5/8/1Q6 w - - 0 1
[ Re8+ Rxe8 Qxh7# ]

11c) 

Mate in 2 puzzles, Part XII.
a) 
kr6/1p6/p5R1/8/1q6/8/Q7/2K5 w - - 0 1
[ Rxa6+ bxa6 Qxa6# ]

b) 
k7/p2bR3/Q7/8/3q4/8/8/2K5 w - - 0 1
[ Re8+ Bxe8 Qc8# ]

c) 
k3r3/pR6/K7/2b5/8/8/1Q3q2/8 w - - 0 1
[ Rxa7+ Bxa7 Qb7# ]

d) 
3rkr2/R3p3/8/4K3/8/7Q/5q2/8 w - - 0 1
[ Rxe7+ Kxe7 Qe6# ]

e) 
2k5/1ppn4/1q6/8/Q7/8/5R2/4K3 w - - 0 1
[ Rf8+ Nxf8 Qe8# ]

12e) 

Mate in 2 puzzles, Part XIII.
a) 
k1r5/p1p5/N1K5/8/3q4/8/8/1R6 w - - 0 1
[ Rb8+ Rxb8 Nxc7# ]

b) 
8/8/6Nr/5Kbk/R7/8/8/8 w - - 0 1
[ Rh4+ Bxh4 Nf4# ]

c) 
kr6/pp6/8/8/2N4R/8/8/3K4 w - - 0 1
[ Nb6+ axb6 Ra4# ]

d) 
4nrkr/5pp1/8/7N/8/8/8/3K2R1 w - - 0 1
[ Rxg7+ Nxg7 Nf6# ]

e) 
2Nnkr2/3p3R/8/5n2/8/8/8/7K w - - 0 1
[ Re7+ Nxe7 Nd6# ]

13b) 

Mate in 2 puzzles, Part XIV.
a) 
2R5/8/pn6/k1N5/8/1K6/6q1/8 w - - 0 1
[ Nb7+ Qxb7 Rc5# ]

b) 
5Kbk/R7/4q1P1/8/8/8/8/8 w - - 0 1
[ Rh7+ Bxh7 g7# ]

c) 
5Kbk/6pp/6pR/5P2/8/8/8/8 w - - 0 1
[ fxg6 gxh6 g7# ]

d) 
3k4/1P6/3K4/8/8/8/1q6/7R w - - 0 1
[ Rh8+ Qh8 b8/Q# ]

e) 
8/8/6rp/6pk/5b1p/5K2/6P1/6R1 w - - 0 1
[ g4+ hxg3 e.p. Rh1# ]

14a) 

Mate in 2 puzzles, Part XV.
a) 
8/6kp/4r1p1/q3r3/6K1/B7/8/2Q5 w - - 0 1
[ Qh6+ if Kxh6 Bf8# or if Kf6 Qf8# ]

b) 
8/pk6/1p6/1B2r3/K7/2Q1q3/8/8 w - - 0 1
[ Ba6+ if Kxa6 Qc8# or if Kb8 Qc8# ]

c) 
kb4q1/1p1B4/pK6/8/8/8/8/5Q2 w - - 0 1
[ Qxa6+ if bxa6 Bc6# or if Ba7 Qxb7# ]

d) 
qkb5/4p3/1K1p4/8/5Q2/6B1/8/8 w - - 0 1
[ Qxd6+ exd6 Bxd6# ]

e) 
B7/8/8/7K/4b3/Q7/7p/1q4bk w - - 0 1
[ Qf3+ Bxf3 Bxf3# ]

15e) 

Mate in 2 puzzles, Part XVI.
a) 
8/8/B7/3qp3/2ppkpp1/8/4K3/3Q4 w - - 0 1
[ Qd3+ cxd3+ Bxd3# ]

b) 
6bk/7p/7K/4N3/8/8/7B/8 w - - 0 1
[ Ng6+ hxg6 Be5# ]

c) 
kB1KN3/p7/n7/8/8/8/8/8 w - - 0 1
[ Kc8 w/Nc7# or Nxc7# ]

d) 
5K1k/6pp/6p1/6B1/6N1/8/8/8 w - - 0 1
[ Nh6 gxh6 Bf6# ]

e) 
8/8/7p/5K1k/6pp/1p6/2B2N2/8 w - - 0 1
[ Nh3 if gxh3 Bd1# or if bxc2 Nf4# ]

16d) 

Mate in 2 puzzles, Part XVII.
a) 
8/8/5B2/8/2pN4/K7/pp6/kb6 w - - 0 1
[ Nb3+ cxb3 Bxb2# ]

b) 
kbK5/p7/2pN4/3p4/8/8/8/5B2 w - - 0 1
[ Ba6 Bxd6 Bb7# ]

c) 
7B/8/pb6/kpn5/b1p5/1P6/1K6/8 w - - 0 1
[ b4+ Kxb4 Bc3# ]

d) 
kb1n4/8/KP6/8/B7/8/8/8 w - - 0 1
[ Bc6+ Nxc6 b7# ]

e) 
3B1K1k/6pp/4b3/7P/8/8/8/8 w - - 0 1
[ h6 gxh6 Bf6# ]

17c) 

Mate in 2 puzzles, Part XVIII.
a) 
8/8/8/6pp/5p1k/5K1b/5P1B/8 w - - 0 1
[ Bg3+ fxg3 fxg3# ]

b) 
8/p2p4/kp6/1pP5/1K6/7B/8/8 w - - 0 1
[ c6 if dxc6 Bc8# ]

c) 
7k/2r4r/5PK1/8/8/2B5/8/8 w - - 0 1
[ f7+ if Rxc3 f8/Q# or f8/R# or if Rg7+ Bxg7# ]

d) 
k1r2q2/ppQ5/N7/8/8/8/8/3K4 w - - 0 1
[ Qb8+ Rxb8 Nc7# ]

e) 
4q2k/4N1pr/8/8/2Q5/8/4K3/8 w - - 0 1
[ Qg8+ Qxg8 Ng6# ]

18e) 

Mate in 2 puzzles, Part XIX.
a) 
rknN4/2p5/1rQ5/8/8/8/1q6/3K4 w - - 0 1
[ Qb7+ Rxb7 Nc6# ]

b) 
4r1kr/5b1p/5KN1/8/8/Q7/3q4/8 w - - 0 1
[ Qf8+ Rxf8 Ne7# ]

c) 
7k/4NKpp/4Q3/8/8/2q2p2/8/6r1 w - - 0 1
[ Ng6+ hxg6 Qh3# ]

d) 
k1b5/8/NKn5/8/4q3/8/7Q/8 w - - 0 1
[ Qb8+ Nxb8 Nc7# ]

e) 
k4K2/p7/1bP5/8/8/8/8/6qQ w - - 0 1
[ c7+ Qxh1 c8/Q# ]

19d) 

Mate in 2 puzzles, Part XX.
a) 
5rkr/5ppp/8/4K3/6N1/2Q5/q7/8 w - - 0 1
[ Nh6+ gxh6 Qg3# ]

b) 
krQ5/p7/8/4q3/N7/8/8/3K4 w - - 0 1
[ Nb6+ axb6 Qa6# ]

c) 
8/1q6/4NQ1r/5npk/8/7K/8/6r1 w - - 0 1
[ Qxg5+ Rxg5 Nf4# ]

d) 
k1r5/p1pq4/Qp1p4/8/3N4/8/3K4/8 w - - 0 1
[ Nc6 Qxc6 Qxc8# ]

e) 
3q2rk/5Q1p/6bK/4N3/8/8/8/8 w - - 0 1
[ Qxh7+ Bxh7 Nf7# ]

20c) 

Mate in 2 puzzles, Part XXI.
a) 
8/8/5Q2/2q3pk/7b/8/4K1P1/8 w - - 0 1
[ g4+ Kxg4 Qf3# ]

b) 
8/b2Q4/kp2p3/p2q4/1P6/K7/8/8 w - - 0 1
[ b5+ Qxb5 Qc8# ]

c) 
8/8/8/pq6/kpp5/7Q/K1P5/8 w - - 0 1
[ Qb3+ cxb3+ cxb3# ]

d) 
5K1k/7b/8/4ppP1/8/6bQ/7q/8 w - - 0 1
[ g6 Qxh3 g7# ]

e) 
1K2kb2/4p3/5P2/5Q1q/7r/8/8/8 w - - 0 1
[ f7+ w/Qc8# ]

21b) 

Mate in 2 puzzles, Part XXII.
a) 
k7/p1K2n2/p7/3p1r2/8/8/8/2R5 w - - 0 1
[ Rb1 ]

b) 
4k3/2r1p1p1/3pK3/8/8/8/8/5R2 w - - 0 1
[ Rh1 ]

c) 
7k/6R1/6Kn/8/8/8/8/8 w - - 0 1
[ Re7 ]

d) 
Black mates in 2.
8/8/8/8/1b6/1k6/8/KBB5 b - - 0 1
[ ...Bc3+ ]

e) 
Black mates in 2.
8/8/8/8/4bN2/5kP1/7P/7K b - - 0 1
[ ...Kf2+ ]

22e) 

Mate in 2 puzzles, Part XXIII.
a) 
Black mates in 2.
7K/b4k1P/8/8/8/8/8/6R1 b - - 0 1
[ ...Bd4+ ]

b) 
Black mates in 2.
8/8/7P/1b1Q3K/5k1B/8/8/8 b - - 0 1
[ ...Be8+ ]

c) 
Black mates in 2.
8/8/8/8/Nb6/8/P7/K1k5 b - - 0 1
[ ...Ba3 ]

d) 
Black mates in 2.
K7/P1k5/2P5/8/8/7b/8/8 b - - 0 1
[ ...Kc8 c7 Bg2# ]

e) 
6qk/8/7K/7Q/8/8/8/8 w - - 0 1
[ Qe5+ ]

23e) 

Mate in 2 puzzles, Part XXIV.
a) 
Black mates in 2.
8/8/8/8/1n6/7N/7P/5k1K b - - 0 1
[ ...Nd3 ]

b) 
Black mates in 2.
8/2n5/8/P7/KPk5/P7/8/8 b - - 0 1
[ ...Na6 ]

c) 
Black mates in 2.
KBk5/2P5/3n4/8/8/8/8/8 b - - 0 1
[ ...Nb5 ]

d) 
Black mates in 2.
8/8/p7/kpK5/p7/8/P7/8 w - - 0 1
[ ...a3 b4 axb4# ]

e) 
8/p7/kPK5/p7/n7/8/8/8 w - - 0 1
[ b7 Nc3 b8/N# ]

24d) 

Mate in 2 puzzles, Part XXV.
a) 
Black mates in 2.
7r/7r/4RP2/5RP1/7k/8/8/7K b - - 0 1
[ ...Kg3+ Kg1 Rh1# ]

b) 
Black mates in 2.
7r/r7/8/8/8/1kP5/1P1R4/1K4R1 b - - 0 1
[ ...Rha8 ]

c) 
2b1kb2/4p3/2K5/8/8/8/8/3BB3 w - - 0 1
[ Bh5+ ]

d) 
8/8/6nq/3p2b1/7k/7p/5Kpp/3BB3 w - - 0 1
[ Kf3+ Kh5 Kg3# ]

e) 
Black mates in 2.
5b2/8/2B5/2BK3b/5k2/3P4/8/8 b - - 0 1
[ ...Bf7+ ]

25c) 

Mate in 2 puzzles, Part XXVI.
a) 
Black mates in 2.
8/8/4k3/2B5/3K4/3BP1b1/b7/8 b - - 0 1
[ ...Be5+ ]

b) 
Black mates in 2.
7b/6kb/8/8/8/P7/8/KB5R b - - 0 1
[ ...Kf8+ ]

c) 
8/6nk/3N2n1/8/4N3/8/8/K7 w - - 0 1
[ Nf6+ ]

d) 
kn6/1n2N3/8/3N4/8/8/8/7K w - - 0 1
[ Nc7+ ]

e) 
5nk1/4K1n1/8/4N3/6N1/8/8/8 w - - 0 1
[ Nf6+ ]

26a)"""

# Step 1: Split the string into lines
lines = string.splitlines()

# Step 2: Filter out empty lines (lines with only spaces or tabs)
filtered_lines = [line for line in lines if line.strip()]

# Step 3: Join the non-empty lines back into a string
filtered_string = "\n".join(filtered_lines)

# Step 4: Split into lines again
lines2 = filtered_string.splitlines()

# Step 5: Filter lines that contain "- -" or "[ ]"
filtered_lines2 = [line for line in lines2 if re.search(r"(-|\[)", line)]

# Step 6: Join the matching lines back into a string
filtered_string2 = "\n".join(filtered_lines2)

# Step 7: Split lines again
lines3 = filtered_string2.strip().splitlines()

# Step 8: Identify and remove lines containing "if" or "or", and also remove the previous line (FEN)
to_remove = set()  # To store line indices that need to be removed

for i, line in enumerate(lines3):
    if "if" in line or "or" in line or "..." in line:
        # Mark the current line and the previous line (FEN) for removal
        to_remove.add(i)
        if i > 0:  # Ensure we don't go out of bounds
            to_remove.add(i - 1)

# Step 9: Filter out the lines marked for removal
filtered_lines3 = [line for i, line in enumerate(lines3) if i not in to_remove]

# Step 10: Join the filtered lines
filtered_string3 = "\n".join(filtered_lines3)

# Step 11: Split again
lines4 = filtered_string3.strip().splitlines()

# Step 12: Initialize an empty dictionary to store the FEN and solutions
fen_solution_dict = {}

# Step 13: Process the FEN and solutions
for i in range(0, len(lines4), 2):  # The FEN and solution are on alternating lines
    fen = lines4[i].strip()

    # Ensure there is a solution for the current FEN (i.e., check if the next line exists)
    if i + 1 < len(lines4):
        solution = lines4[i + 1].strip()[1:-1]  # Removing the [ and ] from the solution

        # Skip puzzles that have "if" or "or" in the solution (already filtered out above)
        fen_solution_dict[fen] = solution

# Step 14: Generate a Python-like dictionary representation
def generate_python_dict(fen_solution_dict):
    dict_str = "{\n"
    
    for fen, solution in fen_solution_dict.items():
        # Prepare the solution in a way that works with Python syntax (i.e., string representation)
        solution_str = f'"{solution}"'  # Make sure solutions are in quotes, like strings
        
        dict_str += f'    "{fen}": {solution_str},\n'
    
    dict_str += "}"
    return dict_str


# Step 15: Generate the Python-like dictionary string
python_dict_str = generate_python_dict(fen_solution_dict)

# Step 16: Output the generated string (for copying)
print(python_dict_str)



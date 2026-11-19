import sys
sys.path.insert(0, '/home/hatch/workspace/makefun/tiny-chess-v7')
import engine as E

def perft(d):
    if d == 0:
        return 1
    n = 0
    for m in E.gen(False):
        u = E.do(m)
        if E.atk(E.KS[1 - E.S], E.S == 0):
            E.undo(m, u)
            continue
        n += perft(d - 1)
        E.undo(m, u)
    return n

tests = [
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 4, 197281),
    ("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1", 3, 97862),
    ("8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1", 4, 43238),
    ("r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1", 3, 9467),
    ("rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8", 3, 62379),
]
ok = True
for fen, d, exp in tests:
    E.load(fen)
    got = perft(d)
    s = "OK" if got == exp else "FAIL"
    if got != exp:
        ok = False
    print(f"{s}: perft d{d} = {got} (expected {exp})  {fen[:30]}")
print("PERFT ALL OK" if ok else "PERFT FAILED")

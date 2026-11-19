import os, json, random, urllib.request as rq
INF = 1000000
MATE = 100000
PV = (0, 0, 1, 1, 2, 4, 0)
VV = (0, 100, 320, 330, 500, 900, 0)
KN = (33,31,18,14,-14,-18,-31,-33)
KG = (1,-1,16,-16,15,17,-15,-17)
DG = (15,17,-15,-17)
RT = (1,-1,16,-16)
AL = DG + RT
CM = {0: 13, 7: 14, 4: 12, 112: 7, 119: 11, 116: 3}
SQ = tuple(r * 16 + f for r in range(8) for f in range(8))
DR = ((), (), KN, DG, RT, AL, KG)
MV = (82, 337, 365, 477, 1025, 0)
EV = (94, 281, 297, 512, 936, 0)
TS = 'KKKKU`c_GOUWFOMQELKOGOKKCPKFKKKK)>;M@G\\SK[_]MOVVINOPFMOOECKK;FAEGM<CBOQMITWUKMRUKMNRLOQOKQOLEEGGUTPYTR[]MUSQEIQQCIILAGII=HJJEELOMQTTOIQIQOSOGGKIIIIJIMIKGIOLEEGJENIBKFHIGQLGEGGC?GB@EGD?LMH=KSIE@GKGKPROMSSOKQRQGKQQGKOQEILO?DGF'
def mk(o, v):
    t = [0] * 128
    for s in SQ:
        f = s & 7
        f = 7 - f if f > 3 else f
        t[s] = v + (ord(TS[o + ((7 - (s >> 4)) << 2) + f]) - 75) * 4
    return tuple(t)
GT = (None,) + tuple(mk((i - 1) * 32, MV[i - 1]) for i in range(1, 7))
ET = (None, GT[1], GT[2], GT[3], GT[4], GT[5], mk(192, EV[5]))
rr = random.Random(0x5EED)
ZB = [[rr.getrandbits(64) for _ in range(128)] for _ in range(13)]
ZS = rr.getrandbits(64)
ZC = [rr.getrandbits(64) for _ in range(16)]
ZE = [rr.getrandbits(64) for _ in range(8)]
B = [0] * 128
S = 0
CR = 0
EP = -1
KS = [4, 116]
MG = EG = PH = 0
KEY = 0
ND = 0
LM = 60 * 1000
TT = {}
SN = {}
HS = {}
HG = None
KL = [0] * 256
def uci(m):
    f = "abcdefgh"
    o = f[m & 7] + str(((m >> 4) & 7) + 1) + f[(m >> 7) & 7] + str(((m >> 11) & 7) + 1)
    q = (m >> 14) & 7
    return o + ("  nbrq"[q] if q else "")
def add(p, q, n=1):
    global MG, EG, PH, KEY
    t = p if p > 0 else -p
    KEY ^= ZB[p + 6][q]
    i = q if p > 0 else q ^ 112
    d = n if p > 0 else -n
    MG += d * GT[t][i]; EG += d * ET[t][i]
    PH += n * PV[t]
def rem(p, q):
    add(p, q, -1)
def load(fen):
    global B, S, CR, EP, KS, MG, EG, PH, KEY, SN
    B = [0] * 128
    MG = EG = PH = 0; KEY = 0
    ps = fen.split()
    r = 7; f = 0
    for c in ps[0]:
        if c == "/":
            r -= 1; f = 0
        elif c.isdigit():
            f += int(c)
        else:
            p = "PNBRQK".index(c.upper()) + 1
            if c.islower(): p = -p
            q = r * 16 + f
            B[q] = p
            add(p, q)
            if abs(p) == 6: KS[p < 0] = q
            f += 1
    S = ps[1] != "w"
    CR = sum(1 << "KQkq".index(c) for c in ps[2] if c != "-")
    EP = (int(ps[3][1]) - 1) * 16 + (ord(ps[3][0]) - 97) if ps[3] != "-" else -1
    if S: KEY ^= ZS
    ky()
    SN = {KEY: 1}
def atk(q, wt):
    s = 1 if wt else -1
    for d in (-15, -17) if wt else (15, 17):
        t = q + d
        if not (t & 0x88) and B[t] == s: return True
    for d in KN:
        t = q + d
        if not (t & 0x88) and B[t] == 2 * s: return True
    for d in KG:
        t = q + d
        if not (t & 0x88) and B[t] == 6 * s: return True
    for d in AL:
        t = q + d
        while not (t & 0x88):
            p = B[t]
            if p:
                if p == 5 * s or (d in DG and p == 3 * s) or (d in RT and p == 4 * s): return True
                break
            t += d
    return False
def gen(co=False):
    ms = []
    wt = S == 0
    bd = B
    def ap(x):
        if (x >> 4) == 7 * wt:
            for pr in (5, 4, 3, 2): ms.append(fr | (x << 7) | (pr << 14))
        else:
            ms.append(fr | (x << 7))
    for fr in SQ:
        p = bd[fr]
        if p == 0 or (p > 0) != wt: continue
        t = p if p > 0 else -p
        if t == 1:
            d = 32 * wt - 16
            f = fr + d
            if not (f & 0x88) and bd[f] == 0 and not co:
                ap(f)
                if (fr >> 4) == 6 - 5 * wt and bd[f + d] == 0:
                    ms.append(fr | ((f + d) << 7))
            for dd in (d - 1, d + 1):
                x = fr + dd
                if x & 0x88: continue
                q = bd[x]
                if q and (q > 0) == wt or not q and x != EP: continue
                ap(x)
        else:
            for d in DR[t]:
                x = fr + d
                while not (x & 0x88):
                    q = bd[x]
                    if q and (q > 0) == wt: break
                    if q or not co: ms.append(fr | (x << 7))
                    if q or t in (2, 6): break
                    x += d
    if not co and not atk(KS[S], not wt):
        for cb, kf, kt, es, at in ((1, 4, 6, (5, 6), (5, 6)), (2, 4, 2, (3, 2, 1), (3, 2)), (4, 116, 118, (117, 118), (117, 118)), (8, 116, 114, (115, 114, 113), (115, 114))):
            if CR & cb and all(not bd[x] for x in es) and not any(atk(x, not wt) for x in at):
                ms.append(kf | (kt << 7))
    return ms
def ky():
    global KEY
    KEY ^= ZC[CR]
    if EP >= 0: KEY ^= ZE[EP & 7]
def cr(frm, to, rev):
    if abs(to - frm) == 2:
        x, y = (frm + 3, frm + 1) if to > frm else (frm - 4, frm - 1)
        if rev: x, y = y, x
        r = B[x]
        rem(r, x); B[x] = 0
        add(r, y); B[y] = r
def do(m):
    global S, CR, EP, KEY
    frm = m & 127; to = (m >> 7) & 127; pr = (m >> 14) & 7
    p = B[frm]; t = p if p > 0 else -p
    wt = p > 0
    cp = B[to]
    u = (cp + 7) | (CR << 4) | ((EP + 1) << 8)
    ky()
    rem(p, frm)
    if cp: rem(cp, to)
    if t == 1 and to == EP and cp == 0:
        es = to - 16 if wt else to + 16
        rem(B[es], es); B[es] = 0
    if t == 6:
        KS[S] = to
        cr(frm, to, 0)
    np = p if not pr else pr if wt else -pr
    add(np, to)
    B[to] = np; B[frm] = 0
    CR &= CM.get(frm, 15) & CM.get(to, 15)
    if t == 1 and abs(to - frm) == 32: EP = (frm + to) // 2
    else: EP = -1
    ky()
    KEY ^= ZS
    S ^= 1
    SN[KEY] = SN.get(KEY, 0) + 1
    return u
def undo(m, u):
    global S, CR, EP, KEY
    SN[KEY] = SN.get(KEY, 0) - 1
    frm = m & 127; to = (m >> 7) & 127; pr = (m >> 14) & 7
    KEY ^= ZS
    ky()
    S ^= 1
    wt = S == 0
    p = B[to]
    rem(p, to)
    mp = 1 if pr else abs(p)
    mp = mp if wt else -mp
    add(mp, frm)
    B[frm] = mp; B[to] = 0
    cp = (u & 15) - 7
    if cp:
        B[to] = cp
        add(cp, to)
    elif pr == 0 and abs(mp) == 1:
        oep = ((u >> 8) & 255) - 1
        if oep >= 0 and to == oep:
            es = to - 16 if wt else to + 16
            cp = -1 if wt else 1
            B[es] = cp
            add(cp, es)
    if abs(mp) == 6:
        KS[S] = frm
        cr(frm, to, 1)
    CR = (u >> 4) & 15
    EP = ((u >> 8) & 255) - 1
    ky()
def evl():
    return (MG * PH + EG * (24 - PH)) // 24
def srt(ms, tm, ply):
    k1 = KL[ply]
    def sc(m):
        if m == tm: return 1 << 30
        q = B[(m >> 7) & 127]
        if q: return 10000 + VV[abs(q)]
        if m == k1: return 9000
        return 0
    ms.sort(key=sc, reverse=True)
    return ms
def nm(e):
    global S, EP, KEY
    if EP >= 0: KEY ^= ZE[EP & 7]
    EP = e
    KEY ^= ZS
    S ^= 1
    if EP >= 0: KEY ^= ZE[EP & 7]
class Stop(Exception):
    pass
def qs(a, b, ply):
    global ND
    ND += 1
    if (ND & 2047) == 0 and ND > LM: raise Stop
    ck = atk(KS[S], S == 1)
    if ck:
        bs = -INF
    else:
        e = evl() if S == 0 else -evl()
        if e >= b: return b
        if e > a: a = e
        bs = a
    for m in srt(gen(not ck), 0, ply):
        u = do(m)
        if atk(KS[1 - S], S == 0):
            undo(m, u); continue
        v = -qs(-b, -a, ply + 1)
        undo(m, u)
        bs = max(bs, v); a = max(a, v)
        if a >= b: break
    return -MATE + ply if bs == -INF else bs
def srch(a, b, dp, ply):
    global ND, S, EP, KEY
    if HS.get(KEY) or SN.get(KEY, 0) > 1: return 0
    if dp <= 0: return qs(a, b, ply)
    ND += 1
    if (ND & 2047) == 0 and ND > LM: raise Stop
    ck = atk(KS[S], S == 1)
    if ck: dp += 1
    te = TT.get(KEY)
    tm = 0
    if te and te[0] >= dp:
        _, v, f, tm = te
        if v > 99000: v -= ply
        elif v < -99000: v += ply
        if f == 0 or (f == 1 and v >= b) or (f == 2 and v <= a): return v
    e = evl() if S == 0 else -evl()
    if dp >= 3 and not ck and PH and e >= b:
        ep0 = EP
        nm(-1)
        v = -srch(-b, -b + 1, dp - 3, ply + 1)
        nm(ep0)
        if v >= b: return b
    ms = srt(gen(False), tm, ply)
    bs = -INF; bm = 0; fl = 2; n = 0
    for i, m in enumerate(ms):
        frm = m & 127; to = (m >> 7) & 127; pr = (m >> 14) & 7
        q = B[to]
        cp = q != 0 or pr != 0 or (abs(B[frm]) == 1 and to == EP and q == 0)
        u = do(m)
        if atk(KS[1 - S], S == 0):
            undo(m, u); continue
        n += 1
        if i == 0:
            v = -srch(-b, -a, dp - 1, ply + 1)
        else:
            rd = dp - 1 - (i > 2 and dp > 2 and not (cp or ck))
            v = -srch(-a - 1, -a, rd, ply + 1)
            if rd < dp - 1 and v > a: v = -srch(-a - 1, -a, dp - 1, ply + 1)
            if a < v < b: v = -srch(-b, -a, dp - 1, ply + 1)
        undo(m, u)
        if v > bs: bs = v; bm = m
        if v > a:
            a = v; fl = 0
        if a >= b:
            if not cp: KL[ply] = m
            fl = 1
            break
    if n == 0: return -MATE + ply if ck else 0
    if len(TT) > 200000: TT.clear()
    sv = bs + ply if bs > 99000 else bs - ply if bs < -99000 else bs
    TT[KEY] = (dp, sv, fl, bm)
    return bs
def fen():
    rs = []
    for rk in range(7, -1, -1):
        row = ""; em = 0
        for f in range(8):
            p = B[rk * 16 + f]
            if p == 0: em += 1
            else:
                if em: row += str(em); em = 0
                row += "PNBRQK"[abs(p) - 1] if p > 0 else "pnbrqk"[abs(p) - 1]
        if em: row += str(em)
        rs.append(row)
    c = ""
    if CR & 1: c += "K"
    if CR & 2: c += "Q"
    if CR & 4: c += "k"
    if CR & 8: c += "q"
    return "/".join(rs) + (" w " if S == 0 else " b ") + (c or "-") + " " + (("abcdefgh"[EP & 7] + str((EP >> 4) + 1)) if EP >= 0 else "-") + " 0 1"
def pick(f, lu, nodes, gid=None):
    global ND, LM, HS, HG, TT
    load(f)
    if gid != HG:
        HS.clear(); HG = gid
        TT.clear()
    HS[KEY] = HS.get(KEY, 0) + 1
    LM = nodes
    ND = 0
    bs = 0
    for dp in range(1, 64):
        try:
            dv = -INF; dm = 0
            for m in srt(gen(False), bs, 0):
                u = do(m)
                if atk(KS[1 - S], S == 0):
                    undo(m, u); continue
                v = -srch(-dv - 1, -dv, dp - 1, 1)
                if v > dv: v = -srch(-INF, -dv, dp - 1, 1)
                undo(m, u)
                if v > dv: dv = v; dm = m
            bs = dm
        except Stop:
            break
    load(f)
    return uci(bs) if bs else lu[0]
def loop():
    url = os.environ.get("MAKEFUN_ENV_URL") or exit("MAKEFUN_ENV_URL is not set")
    def call(path, body):
        try:
            with rq.urlopen(url + path, json.dumps(body).encode()) as r: return json.load(r)
        except Exception: return {}
    while True:
        g = call("/game", {})
        while g.get("status") == "your_move":
            g = call("/move", {"game": g["game"], "move": pick(g["fen"], g["legal_moves"], 60000, g["game"])})
        if g.get("status") == "done": break
if __name__ == "__main__":
    loop()

"""第2巡その2（2026-11-10）：双極・XYZ・FBI・回す三つの関係の検算。

確かめること：
  1. 立方体1個の数：中心1、軸3、対角線4、面6、頂点8、辺12。1+6+12+8 = 27 = 3³。
  2. XYZ = -1 の4点（正四面体 T-）と XYZ = +1 の4点（T+）を合わせると立方体の8頂点。
  3. 正四面体の回転は12通りで、回転軸は 3回軸4本 + 2回軸3本 = 7本。
     立方体の回転は24通りで、回転軸は 3 + 4 + 6 = 13本。
  4. X・Y・Z まわりの半回転（π）を3つ続けると元に戻る（回転としては +1）。
  5. 四元数では i·j·k = -1、(i·j·k)·(-1) = +1。
  6. x・y・z まわりの半回転は、正四面体の1頂点を残りの3頂点へ移す。
  7. 4頂点を2組に分ける方法は3通りで、組の和が ±X・±Y・±Z の軸になる。
  8. 立方体と正8面体の双対：立方体の面の中心6点が正8面体、
     正8面体の面の中心8点が立方体の頂点の向き。6 + 8 = 14 = 7 × 2。
  9. 8頂点の和は 0（9点目は原点）。
 10. 3つで回る足し算（1, 2, 3 で 3+1=1）：3 が何も変えない数、1-1=3、
     4 と 7 は 1、四則演算が閉じる（3 以外は割れる）。
 11. 3³+4³+5³=6³ を3で見ると 0+1+2=0。
 12. 2³ + 1 = 3²。100万までのべき乗数で隣り合うのは 8 と 9 だけ。
 13. 黄金比：φ×φ = φ+1、φ-1 = 1÷φ。
 14. 外積：I×B は I にも B にも直交。B×I = -(I×B)。
"""
import itertools
import math

ok = True


def check(name, cond):
    global ok
    ok &= bool(cond)
    print(f"{'PASS' if cond else 'FAIL'}  {name}")


# ---------- 1. 立方体1個の数 ----------
lattice = list(itertools.product((-1, 0, 1), repeat=3))
by_zeros = {k: [p for p in lattice if p.count(0) == k] for k in range(4)}
center, faces, edges, verts = by_zeros[3], by_zeros[2], by_zeros[1], by_zeros[0]
check("中心1・面6・辺12・頂点8", (len(center), len(faces), len(edges), len(verts)) == (1, 6, 12, 8))
check("1 + 6 + 12 + 8 = 27 = 3³", len(lattice) == 27 == 3 ** 3)
check("軸3（面の中心の対）", len(faces) // 2 == 3)
check("対角線4（頂点の対）", len(verts) // 2 == 4)

# ---------- 2. 二つの正四面体 ----------
t_minus = [v for v in verts if math.prod(v) == -1]
t_plus = [v for v in verts if math.prod(v) == 1]
check("XYZ=-1 が4点、XYZ=+1 が4点、合わせて8頂点",
      len(t_minus) == 4 and len(t_plus) == 4 and set(t_minus) | set(t_plus) == set(verts))
check("T+ は T- の反転", {tuple(-c for c in v) for v in t_minus} == set(t_plus))


# ---------- 3. 回転と回転軸 ----------
def matmul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)) for i in range(3))


def apply(m, v):
    return tuple(sum(m[i][k] * v[k] for k in range(3)) for i in range(3))


def det(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


IDENT = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
cube_rot = []
for perm in itertools.permutations(range(3)):
    for signs in itertools.product((1, -1), repeat=3):
        m = tuple(tuple(signs[i] if perm[i] == j else 0 for j in range(3)) for i in range(3))
        if det(m) == 1:
            cube_rot.append(m)
tet_rot = [m for m in cube_rot if {apply(m, v) for v in t_minus} == set(t_minus)]


def axis_of(m):
    """回転行列の軸（符号をそろえた向き）を返す。"""
    for p in lattice:
        if p != (0, 0, 0) and apply(m, p) == p:
            g = math.gcd(*[abs(c) for c in p])
            q = tuple(c // g for c in p)
            first = next(c for c in q if c != 0)
            return tuple(c * (1 if first > 0 else -1) for c in q)
    return None


def order(m):
    k, x = 1, m
    while x != IDENT:
        x = matmul(x, m)
        k += 1
    return k


def axes(group):
    out = {}
    for m in group:
        if m != IDENT:
            a = axis_of(m)
            out[a] = max(out.get(a, 0), order(m))
    return out


tet_axes = axes(tet_rot)
cube_axes = axes(cube_rot)
check("正四面体の回転は12通り", len(tet_rot) == 12)
check("正四面体の回転軸：3回軸4本 + 2回軸3本 = 7本",
      sorted(tet_axes.values()) == [2, 2, 2, 3, 3, 3, 3] and len(tet_axes) == 7)
check("立方体の回転は24通り", len(cube_rot) == 24)
check("立方体の回転軸：4回軸3本 + 3回軸4本 + 2回軸6本 = 13本",
      sorted(cube_axes.values()) == [2] * 6 + [3] * 4 + [4] * 3 and len(cube_axes) == 13)

# ---------- 4. 半回転3つ ----------
RX = ((1, 0, 0), (0, -1, 0), (0, 0, -1))
RY = ((-1, 0, 0), (0, 1, 0), (0, 0, -1))
RZ = ((-1, 0, 0), (0, -1, 0), (0, 0, 1))
check("X・Y・Z まわりの半回転を3つ続けると元に戻る", matmul(matmul(RX, RY), RZ) == IDENT)
check("半回転を2回で元に戻る（X・Y・Z とも）", all(matmul(r, r) == IDENT for r in (RX, RY, RZ)))


# ---------- 5. 四元数 ----------
def qmul(a, b):
    a0, a1, a2, a3 = a
    b0, b1, b2, b3 = b
    return (a0 * b0 - a1 * b1 - a2 * b2 - a3 * b3,
            a0 * b1 + a1 * b0 + a2 * b3 - a3 * b2,
            a0 * b2 - a1 * b3 + a2 * b0 + a3 * b1,
            a0 * b3 + a1 * b2 - a2 * b1 + a3 * b0)


ONE, QI, QJ, QK = (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)
MINUS = (-1, 0, 0, 0)
ijk = qmul(qmul(QI, QJ), QK)
check("i² = j² = k² = -1", qmul(QI, QI) == qmul(QJ, QJ) == qmul(QK, QK) == MINUS)
check("i·j·k = -1（XYZ = -1 と同じ形）", ijk == MINUS)
check("(i·j·k)·(-1) = +1（XYZπ = 1 と同じ形）", qmul(ijk, MINUS) == ONE)
check("i·j = k（X×Y = Z と同じ形）", qmul(QI, QJ) == QK)

# ---------- 6. 半回転が頂点を移す ----------
v1 = t_minus[0]
moved = {apply(r, v1) for r in (RX, RY, RZ)}
check("半回転3つで、1頂点が残りの3頂点へ移る", moved == set(t_minus) - {v1})

# ---------- 7. 4頂点を2組に分ける ----------
pairings = set()
for pair in itertools.combinations(t_minus, 2):
    rest = tuple(v for v in t_minus if v not in pair)
    pairings.add(frozenset([frozenset(pair), frozenset(rest)]))
sums = set()
for pg in pairings:
    for pair in pg:
        sums.add(tuple(sum(c) for c in zip(*pair)))
check("4つを2組に分ける方法は3通り", len(pairings) == 3)
check("組の和は ±X・±Y・±Z（大きさ2）の6つ",
      sums == {(2, 0, 0), (-2, 0, 0), (0, 2, 0), (0, -2, 0), (0, 0, 2), (0, 0, -2)})

# ---------- 8. 立方体と正8面体の双対 ----------
octa = faces  # 立方体の面の中心 = 正8面体の頂点
octa_faces = [t for t in itertools.combinations(octa, 3)
              if all(sum(a * b for a, b in zip(p, q)) == 0 for p, q in itertools.combinations(t, 2))]
octa_face_dirs = {tuple(sum(c) for c in zip(*t)) for t in octa_faces}
check("立方体の面の中心は6点（正8面体の頂点）", len(octa) == 6)
check("正8面体の面は8枚で、その中心の向きは立方体の8頂点", octa_face_dirs == set(verts))
check("6 + 8 = 14 = 7 × 2", len(octa) + len(verts) == 14 == 7 * 2)

# ---------- 9. 9点目 ----------
check("8頂点の和は 0（9点目は原点）", tuple(sum(c) for c in zip(*verts)) == (0, 0, 0))


# ---------- 10. 3つで回る足し算 ----------
def r3(n):
    """整数を 1, 2, 3 のどれかに直す（3 がゼロ役）。"""
    return (n - 1) % 3 + 1


check("1+1=2、2+1=3、3+1=1", (r3(1 + 1), r3(2 + 1), r3(3 + 1)) == (2, 3, 1))
check("3 は何も変えない数（3+a=a）", all(r3(3 + a) == a for a in (1, 2, 3)))
check("1-1=3（引いても無にならない）", r3(1 - 1) == 3)
check("4 は 1、7 も 1", r3(4) == 1 and r3(7) == 1)
check("2+1=3：2 は 1 の裏返し", r3(2 + 1) == 3)
check("掛け算と割り算：2×2=1、だから 1÷2=2", r3(2 * 2) == 1)
check("3 以外は必ず割れる（逆数がある）",
      all(any(r3(a * b) == 1 for b in (1, 2)) for a in (1, 2)))

# ---------- 11. 立方の等式を3で見る ----------
check("3³+4³+5³=6³", 3 ** 3 + 4 ** 3 + 5 ** 3 == 6 ** 3)
check("3で見ると 3+1+2=3（0+1+2=0）",
      (r3(3 ** 3), r3(4 ** 3), r3(5 ** 3), r3(6 ** 3)) == (3, 1, 2, 3))

# ---------- 12. 平方と立方 ----------
check("2²=4、2³=8、3²=9、3³=27", (2 ** 2, 2 ** 3, 3 ** 2, 3 ** 3) == (4, 8, 9, 27))
check("2³ + 1 = 3²", 2 ** 3 + 1 == 3 ** 2)
LIMIT = 10 ** 6
powers = set()
for base in range(2, int(LIMIT ** 0.5) + 1):
    x = base * base
    while x <= LIMIT:
        powers.add(x)
        x *= base
neighbours = sorted((p, p + 1) for p in powers if p + 1 in powers)
check(f"{LIMIT} までのべき乗数で隣り合うのは (8, 9) だけ", neighbours == [(8, 9)])
check("3²+4²=5²", 3 ** 2 + 4 ** 2 == 5 ** 2)

# ---------- 13. 黄金比 ----------
phi = (1 + math.sqrt(5)) / 2
check("φ×φ = φ+1（掛ける＝足す）", abs(phi * phi - (phi + 1)) < 1e-12)
check("φ-1 = 1÷φ（引く＝割る）", abs((phi - 1) - 1 / phi) < 1e-12)


# ---------- 14. 外積 ----------
def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


I_vec, B_vec = (2, -1, 3), (1, 4, -2)
F_vec = cross(I_vec, B_vec)
check("I×B は I にも B にも直交", dot(F_vec, I_vec) == 0 and dot(F_vec, B_vec) == 0)
check("B×I = -(I×B)", cross(B_vec, I_vec) == tuple(-c for c in F_vec))
X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
check("X×Y = Z。X＝B、Y＝I と置くと Z ＝ B×I ＝ -(I×B)",
      cross(X, Y) == Z and cross(Y, X) == tuple(-c for c in Z))

print()
print("すべて PASS" if ok else "FAIL あり")
raise SystemExit(0 if ok else 1)

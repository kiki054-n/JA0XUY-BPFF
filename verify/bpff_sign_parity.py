"""符号の交互（2026-11-09）の検証。

主張：n 個の双極要素の積を (-1)^n と置く。
  n=2: XY = 1, n=3: XYZ = -1, n=4: XYZπ = 1 （π を「包む1つ」として4番目に数える）
確かめること：
  1. 各 X_i = ±1 で積が (-1)^n になる点の数は 2^(n-1)（半超立方体）。
  2. n=3（XYZ=-1）の4点は正四面体（6本の距離がすべて等しい）。
  3. n=3 の4点の和は 0（中心が双極の0）。
  4. π を -1 （= e^{iπ}、半回転）と読むと XYZ·π = (-1)(-1) = 1。
"""
import cmath
import itertools
import math


def half_cube(n):
    target = (-1) ** n
    return [v for v in itertools.product((1, -1), repeat=n) if math.prod(v) == target]


ok = True
for n in range(2, 8):
    pts = half_cube(n)
    sign = "+1" if (-1) ** n > 0 else "-1"
    good = len(pts) == 2 ** (n - 1)
    ok &= good
    print(f"n={n}: 積={sign}  点の数={len(pts)}  (2^(n-1)={2 ** (n - 1)})  {'PASS' if good else 'FAIL'}")

tet = half_cube(3)
d = {round(math.dist(a, b), 12) for a, b in itertools.combinations(tet, 2)}
s = [sum(c) for c in zip(*tet)]
print("n=3 の点:", tet)
print("6本の辺の長さ:", d, "PASS" if len(d) == 1 else "FAIL")
print("頂点の和:", s, "PASS" if s == [0, 0, 0] else "FAIL")
ok &= len(d) == 1 and s == [0, 0, 0]

pi_as_rotation = cmath.exp(1j * math.pi)
closed = (-1) * pi_as_rotation
print("e^{iπ} =", round(pi_as_rotation.real, 12), " XYZ·e^{iπ} =", round(closed.real, 12),
      "PASS" if abs(closed - 1) < 1e-12 else "FAIL")
ok &= abs(closed - 1) < 1e-12

print("総合:", "PASS" if ok else "FAIL")

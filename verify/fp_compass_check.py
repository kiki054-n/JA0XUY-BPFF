"""Toward a First Principle 序章（2026-11-09）の数の主張の検算。

確かめること：
  1. 黄金比 φ について φ·(1/φ) = 1、φ − 1/φ = 1。
  2. 正の双極の組 (x, 1/x) で差がちょうど 1 になるのは x = φ だけ。
  3. 「1 を足して逆数で包む」x → 1 + 1/x を繰り返すと φ に収束する（連分数）。
  4. 前の二つを足す列 125, 162, ... の隣どうしの比が φ に近づく。
  5. 2, 6, 18, 54, 162 の比はちょうど 3（φ にはならない）。
  6. 3² + 4² = 5²、3³ + 4³ + 5³ = 6³。
  7. 6³ = 216 ≠ 666（666 = 6×6×6 の主張は否定）。
  8. 1 + 2 + … + 36 = 666（偶然の符合として記録）。
"""
import math

ok = True


def check(name, cond):
    global ok
    ok &= bool(cond)
    print(f"{'PASS' if cond else 'FAIL'}  {name}")


phi = (1 + math.sqrt(5)) / 2
check("φ·(1/φ) = 1", abs(phi * (1 / phi) - 1) < 1e-12)
check("φ − 1/φ = 1", abs(phi - 1 / phi - 1) < 1e-12)

# x − 1/x = 1 ⇔ x² − x − 1 = 0。正の解は φ のみ。
roots = [(1 + math.sqrt(5)) / 2, (1 - math.sqrt(5)) / 2]
positive = [r for r in roots if r > 0]
check("差が1になる正の双極の組は φ のみ", len(positive) == 1 and abs(positive[0] - phi) < 1e-12)

x = 1.0
for _ in range(60):
    x = 1 + 1 / x
check(f"1を足して逆数で包む操作の到着点 = {x:.12f}", abs(x - phi) < 1e-12)

seq = [125, 162]
while len(seq) < 30:
    seq.append(seq[-1] + seq[-2])
print("前の二つを足す列:", seq[:6], "…")
for a, b in zip(seq[:5], seq[1:6]):
    print(f"   {b}/{a} = {b / a:.4f}")
check("比が φ に近づく（30項目）", abs(seq[-1] / seq[-2] - phi) < 1e-9)

tri = [2 * 3 ** k for k in range(5)]
check(f"{tri} の比はすべて 3", all(b / a == 3 for a, b in zip(tri, tri[1:])))

check("3² + 4² = 5²", 3 ** 2 + 4 ** 2 == 5 ** 2)
check("3³ + 4³ + 5³ = 6³ (= 216)", 3 ** 3 + 4 ** 3 + 5 ** 3 == 6 ** 3 == 216)
check("6×6×6 ≠ 666（主張は否定）", 6 ** 3 != 666)
check("1 + 2 + … + 36 = 666（偶然の符合）", sum(range(1, 37)) == 666)

print("\n総合:", "ALL PASS" if ok else "FAIL あり")

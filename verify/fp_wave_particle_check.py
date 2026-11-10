"""第2巡その3（2026-11-10 夜）：波と粒子、BPFF の二つの読みの検算。

確かめること：
  1. 二つの道（二重スリット）の純粋な状態では、道の見分けやすさ D と
     縞のくっきりさ V が D² + V² = 1 を満たす（振幅の偏りによらない）。
  2. 道に目印を付けた場合（目印どうしの重なり γ）も、目印が純粋な状態なら
     D² + V² = 1。γ = 1（目印なし）で D は偏りだけ、γ = 0（完全な目印）で V = 0。
  3. 目印のほかに、読まない環境が道の情報を持ち去ると D² + V² < 1。
  4. 直交する二つの読みの合成は 3² + 4² = 5² の形（0.6² + 0.8² = 1）。
  5. 電子の位置を 0.1 Å に絞る運動エネルギーの目安 ħ²/(2mΔx²) は約 380 eV で、
     水素分子の結合エネルギー 4.48 eV を超える。
"""
import math

ok = True


def check(name, cond):
    global ok
    ok &= bool(cond)
    print(f"{'PASS' if cond else 'FAIL'}  {name}")


def trace_norm_2x2(a, b, d):
    """実対称行列 [[a, b], [b, d]] の固有値の絶対値の和"""
    tr, det = a + d, a * d - b * b
    disc = math.sqrt(max(tr * tr / 4 - det, 0.0))
    return abs(tr / 2 + disc) + abs(tr / 2 - disc)


def dv(p, gamma, lam=1.0):
    """道1の確率 p、目印の重なり gamma、読まない環境による縞の弱まり lam（1 で弱まりなし）から D と V。
    目印1 = (1, 0)、目印2 = (gamma, √(1-gamma²))。D は目印だけで道を見分ける度合い（トレース距離）。"""
    q = 1 - p
    s = math.sqrt(max(1 - gamma * gamma, 0.0))
    # p|m1><m1| - q|m2><m2|
    a = p - q * gamma * gamma
    b = -q * gamma * s
    d = -q * s * s
    D = trace_norm_2x2(a, b, d)
    V = 2 * math.sqrt(p * q) * abs(gamma) * lam
    return D, V


# ---------- 1. 目印なしの純粋な状態 ----------
worst = max(abs(sum(x * x for x in dv(p / 100, 1.0)) - 1) for p in range(0, 101))
check("目印なし：D² + V² = 1（道1の確率 0〜1 の 101 通り、最大のずれ < 1e-12）", worst < 1e-12)
D, V = dv(0.5, 1.0)
check("目印なし・半々：D = 0、V = 1（完全な縞）", abs(D) < 1e-12 and abs(V - 1) < 1e-12)

# ---------- 2. 目印つきの純粋な状態 ----------
worst = 0.0
for p in [0.1, 0.3, 0.5, 0.8]:
    for g in [0.0, 0.2, 0.5, 0.9, 1.0]:
        D, V = dv(p, g)
        worst = max(worst, abs(D * D + V * V - 1))
check("目印つき（純粋）：D² + V² = 1（20 通り、最大のずれ < 1e-12）", worst < 1e-12)
D, V = dv(0.5, 0.0)
check("完全な目印・半々：D = 1、V = 0（縞は消える）", abs(D - 1) < 1e-12 and abs(V) < 1e-12)

# ---------- 3. 読まない環境 ----------
D, V = dv(0.5, 0.5, lam=0.6)
check(f"読まない環境が道の情報を持ち去る：D² + V² = {D*D + V*V:.3f} < 1", D * D + V * V < 1)

# ---------- 4. 3² + 4² = 5² ----------
check("0.6² + 0.8² = 1（3² + 4² = 5² を 5 で割った形）", abs(0.6 ** 2 + 0.8 ** 2 - 1) < 1e-15)

# ---------- 5. 位置を絞る代償 ----------
hbar_c = 197.3269804          # eV·nm
me_c2 = 510998.95             # eV
dx = 0.01                     # nm = 0.1 Å
E = hbar_c ** 2 / (2 * me_c2 * dx ** 2)
check(f"0.1 Å に絞る運動エネルギーの目安 = {E:.0f} eV > 水素分子の結合 4.48 eV", E > 4.48 and 370 < E < 390)

print()
print("すべて PASS" if ok else "FAIL あり")
raise SystemExit(0 if ok else 1)

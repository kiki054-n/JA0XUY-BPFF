#!/usr/bin/env python3
"""
JA0XUY-BPFF 数値検証：√N の道（H6 改訂案 H6'）

主張（作業仮説）
    単位胞ごとに UM=1（H4）、総和は期待値として厳密に 0（H5）。
    崩壊・誕生の途中の単位胞（H6）は、つり合いを +1 か -1 に崩し、向きは決まっていない。
    N 個の出来事のずれは打ち消し合いきれず √N だけ残る（ランダムウォーク）。
    よって
        rho_Lambda / rho_P = kappa / sqrt(N)
    N = 観測者の過去（過去光円錐の内側）にある時空の単位胞の数
      = V4 / (l_P^3 * c t_P)   （単位胞 = OπO^3 × t_P）

このスクリプトがすること
    1. 平坦 ΛCDM（Planck 2018）で過去光円錐の 4 次元体積 V4 を数値積分する
    2. N と 1/sqrt(N) を出す
    3. 観測値に合わせたときの係数 kappa を出す（kappa は予言ではなく「導くべき数」）
    4. 比較のため、粗い見積もり N ~ (t0/t_P)^4 も出す

標準ライブラリのみ。
    python3 verify/bpff_sqrtN_lambda.py
"""

import math

# 定数（CODATA 2018）
C = 2.99792458e8
G = 6.67430e-11
HBAR = 1.054571817e-34
MPC = 3.0856775814913673e22
GYR = 3.15576e16

# 宇宙論パラメータ（Planck 2018 TT,TE,EE+lowE+lensing）
H0 = 67.4e3 / MPC          # [1/s]
OM = 0.315                 # 物質
OR = 9.1e-5                # 放射（光子＋ニュートリノ）
OL = 1.0 - OM - OR         # 暗黒エネルギー（平坦）

T_P = math.sqrt(HBAR * G / C**5)
L_P = C * T_P
RHO_P = C**5 / (HBAR * G**2)


def E(a):
    return math.sqrt(OR / a**4 + OM / a**3 + OL)


def integrate(f, x0, x1, n=200000):
    """対数格子の台形則（a は 1e-12 から 1 まで何桁も変わるため）"""
    lx0, lx1 = math.log(x0), math.log(x1)
    h = (lx1 - lx0) / n
    s = 0.0
    prev = f(x0) * x0
    for i in range(1, n + 1):
        x = math.exp(lx0 + i * h)
        cur = f(x) * x
        s += 0.5 * (prev + cur) * h
        prev = cur
    return s


def main():
    a_min = 1e-12

    # 宇宙年齢 t0 = ∫ da / (a H)
    t0 = integrate(lambda a: 1.0 / (a * H0 * E(a)), a_min, 1.0)

    # 共動距離 chi(a) = c ∫_a^1 da' / (a'^2 H)
    # 過去光円錐の 4 次元体積
    #   V4 = ∫_0^t0 dt a(t)^3 (4π/3) chi(t)^3
    #      = ∫ da/(aH) a^3 (4π/3) chi(a)^3
    # chi を表で持ってから積分する
    n = 20000
    la0 = math.log(a_min)
    h = (0.0 - la0) / n
    a_grid = [math.exp(la0 + i * h) for i in range(n + 1)]
    # chi を a=1 から逆向きに積む
    chi = [0.0] * (n + 1)
    g = lambda a: C / (a * a * H0 * E(a)) * a   # d chi / d ln a
    for i in range(n - 1, -1, -1):
        chi[i] = chi[i + 1] + 0.5 * (g(a_grid[i]) + g(a_grid[i + 1])) * h
    v4 = 0.0
    def integrand(i):
        a = a_grid[i]
        # dt = d ln a / H ;  c dt を時間方向の長さとして掛ける
        return (C / (H0 * E(a))) * a**3 * (4.0 * math.pi / 3.0) * chi[i] ** 3
    for i in range(n):
        v4 += 0.5 * (integrand(i) + integrand(i + 1)) * h

    rho_crit = 3 * H0**2 / (8 * math.pi * G)
    rho_L = OL * rho_crit
    ratio_obs = rho_L / RHO_P

    cell4 = L_P**3 * (C * T_P)           # 単位胞の 4 次元体積 = l_P^4
    N = v4 / cell4
    inv_sqrtN = 1.0 / math.sqrt(N)
    kappa = ratio_obs * math.sqrt(N)

    N_rough = (t0 / T_P) ** 4
    kappa_rough = ratio_obs * math.sqrt(N_rough)

    # Sorkin 型の表記：Lambda l_P^2 = alpha / sqrt(V4/l_P^4)
    lam_lp2 = 8 * math.pi * G * rho_L / C**2 * L_P**2
    alpha_sorkin = lam_lp2 * math.sqrt(N)

    print("=" * 64)
    print("√N の道：rho_Lambda/rho_P = kappa / sqrt(N)")
    print("=" * 64)
    print(f"  宇宙年齢 t0              {t0/GYR:12.4f} Gyr")
    print(f"  t0 / t_P                 {t0/T_P:12.4e}")
    print(f"  過去光円錐の V4          {v4:12.4e} m^4")
    print(f"  N = V4 / l_P^4           {N:12.4e}")
    print(f"  1/sqrt(N)                {inv_sqrtN:12.4e}")
    print(f"  観測 rho_L/rho_P         {ratio_obs:12.4e}")
    print(f"  必要な係数 kappa         {kappa:12.4f}")
    print()
    print("  粗い見積もり N ~ (t0/t_P)^4")
    print(f"  N_rough                  {N_rough:12.4e}")
    print(f"  kappa_rough              {kappa_rough:12.4f}")
    print()
    print("  Sorkin 型表記 Lambda l_P^2 = alpha / sqrt(N)")
    print(f"  Lambda l_P^2             {lam_lp2:12.4e}")
    print(f"  alpha (= 8π kappa)       {alpha_sorkin:12.4f}")
    print()
    print("判定")
    lg = math.log10(ratio_obs / inv_sqrtN)
    print(f"  観測 / (1/sqrt N) の桁差  {lg:+.2f} 桁")
    print("  -> 桁（10^-123）は構造から出る。係数 kappa は未導出。")
    print("  -> Λ は向きの決まらない √N のずれなので符号も大きさも揺らぐ。")
    print("     w = -1 で時間変化しない（旧 H4 の予言）は成り立たない。")


def epoch_amplitude(a_end, kappa, n=20000, a_min=1e-14):
    """時刻 a_end での揺らぎの大きさ kappa/sqrt(N) を、その時代の臨界密度で割った値"""
    la0 = math.log(a_min)
    h = (math.log(a_end) - la0) / n
    a = [math.exp(la0 + i * h) for i in range(n + 1)]
    g = lambda x: C / (x * H0 * E(x))
    chi = [0.0] * (n + 1)
    for i in range(n - 1, -1, -1):
        chi[i] = chi[i + 1] + 0.5 * (g(a[i]) + g(a[i + 1])) * h
    f = lambda i: (C / (H0 * E(a[i]))) * a[i] ** 3 * 4 * math.pi / 3 * chi[i] ** 3
    v4 = sum(0.5 * (f(i) + f(i + 1)) * h for i in range(n))
    N = v4 / L_P**4
    H = H0 * E(a_end)
    rho_c = 3 * H * H / (8 * math.pi * G)
    return kappa / math.sqrt(N) * RHO_P / rho_c


def check_epochs(kappa):
    print()
    print("=" * 64)
    print("各時代の揺らぎの大きさ（その時代の臨界密度に対する比）")
    print("=" * 64)
    for name, a in [("元素合成 (a=1e-9)", 1e-9), ("CMB (z=1100)", 1 / 1101),
                    ("z=9", 0.1), ("z=1", 0.5), ("現在", 1.0)]:
        print(f"  {name:<20} {epoch_amplitude(a, kappa):8.3f}")
    print("  -> 揺らぎは各時代で臨界密度と同じ桁（1〜2倍）。")
    print("     元素合成・CMB では暗黒エネルギーは数%以下に抑えられているため、")
    print("     典型的な揺らぎは観測と衝突する。H6' の最大の課題。")


if __name__ == "__main__":
    main()
    check_epochs(0.0287)

#!/usr/bin/env python3
"""
JA0XUY-BPFF 数値検証スクリプト

references/equations.md と logs/2026-11-05.md の数値を再計算し、
BPFF 作業仮説（hypotheses/bpff.md）に関わる判定を出力する。

標準ライブラリのみで動く。
    python3 verify/bpff_check.py

定数：CODATA 2018
宇宙論パラメータ：Planck 2018 (TT,TE,EE+lowE+lensing)
"""

import math

# ---------------------------------------------------------------
# 定数
# ---------------------------------------------------------------
C = 2.99792458e8           # 光速 [m/s]
G = 6.67430e-11            # 万有引力定数 [m^3 kg^-1 s^-2]
HBAR = 1.054571817e-34     # 換算プランク定数 [J s]
MPC = 3.0856775814913673e22  # 1 Mpc [m]

H0_KMS_MPC = 67.4          # ハッブル定数 [km/s/Mpc]
OMEGA_L = 0.6847           # 暗黒エネルギーの密度パラメータ

# 観測が示す w の許容幅の目安（constant-w 解析で -1 から 1 割程度）
W_TOLERANCE = 0.1


def header(title):
    print()
    print("=" * 64)
    print(title)
    print("=" * 64)


def row(name, value, unit=""):
    print(f"  {name:<28} {value:>12.4e} {unit}")


# ---------------------------------------------------------------
# 検証1：プランク単位と観測値（equations.md 第7節）
# ---------------------------------------------------------------
def check_units():
    header("検証1：プランク単位と観測値")

    l_p = math.sqrt(HBAR * G / C**3)
    t_p = l_p / C
    rho_p = C**5 / (HBAR * G**2)

    h0 = H0_KMS_MPC * 1e3 / MPC
    r_h = C / h0
    rho_c = 3 * h0**2 / (8 * math.pi * G)
    rho_l = OMEGA_L * rho_c

    row("l_P", l_p, "m")
    row("t_P", t_p, "s")
    row("rho_Planck", rho_p, "kg/m^3")
    row("rho_Planck (energy)", rho_p * C**2, "J/m^3")
    row("R_H = c/H0", r_h, "m")
    row("R_H / l_P", r_h / l_p)
    row("rho_c", rho_c, "kg/m^3")
    row("rho_Lambda", rho_l, "kg/m^3")
    row("rho_Lambda (energy)", rho_l * C**2, "J/m^3")
    row("rho_c / rho_Planck", rho_c / rho_p)
    row("rho_Lambda / rho_Planck", rho_l / rho_p)
    row("t_P * H0", t_p * h0)
    row("(t_P * H0)^2", (t_p * h0) ** 2)
    row("(R_H / l_P)^3", (r_h / l_p) ** 3)

    # フリードマン方程式の書き換えが一致することの確認
    rhs = 3 / (8 * math.pi) * (l_p / r_h) ** 2
    ok = math.isclose(rho_c / rho_p, rhs, rel_tol=1e-9)
    print(f"\n  rho_c/rho_P = 3/(8pi) (l_P/R_H)^2 : {'一致' if ok else '不一致'}")

    return dict(l_p=l_p, t_p=t_p, rho_p=rho_p, h0=h0, r_h=r_h,
                rho_c=rho_c, rho_l=rho_l)


# ---------------------------------------------------------------
# 検証2：文書④の式（logs 第0節）
# ---------------------------------------------------------------
def check_doc4(u):
    header("検証2：文書④の式 rho ~ 3/(R/l_P)^2 rho_P")

    pred = 3 / (u["r_h"] / u["l_p"]) ** 2
    obs = u["rho_l"] / u["rho_p"]
    row("予測（R = R_H）", pred)
    row("観測", obs)
    print(f"  {'予測/観測':<28} {pred / obs:>12.2f} 倍")
    print("  判定：係数がずれる。さらに R が膨張で増えれば a^-2 で薄まり w=-1/3（加速しない）")


# ---------------------------------------------------------------
# 検証3：宇宙全体で UM=1 とする案の矛盾（logs 第3節、H4 否定代案）
# ---------------------------------------------------------------
def check_global_xy(u):
    header("検証3：宇宙全体の質 X で rho ∝ X^-p とする案")

    n = (u["r_h"] / u["l_p"]) ** 3
    obs = u["rho_l"] / u["rho_p"]
    p_size = -math.log10(obs) / math.log10(n)
    p_w = W_TOLERANCE  # w = -1 + p

    row("X（単位胞の数）", n)
    print(f"  {'大きさから必要な p':<28} {p_size:>12.3f}")
    print(f"  {'w≈-1 から必要な p（上限）':<28} {p_w:>12.3f}")
    print(f"  {'UM=1 そのまま（p=1）の大きさ':<28} {n ** -1:>12.4e}")
    verdict = "両立しない" if p_size > p_w else "両立する"
    print(f"  判定：{verdict}")


# ---------------------------------------------------------------
# 検証4：X の数え方ごとの w（会話中の表）
# ---------------------------------------------------------------
def check_counting():
    header("検証4：張力 ∝ 1/X とした場合の w（rho ∝ a^-3(1+w)）")

    cases = [
        ("体積（単位胞の数）", 3.0),
        ("長さ（外郭の大きさ）", 1.0),
        ("有のエネルギー（張力×体積）", 1.5),
        ("単位胞ごとの UM=1（H4）", 0.0),
    ]
    for name, n in cases:
        w = -1 + n / 3
        acc = "加速する" if w < -1 / 3 else "加速しない"
        near = "w≈-1 と整合" if abs(w + 1) <= W_TOLERANCE else "観測から除外"
        print(f"  {name:<24} rho∝a^-{n:<4} w={w:+.3f}  {acc} / {near}")


# ---------------------------------------------------------------
# 検証5：崩壊と誕生（H6）に必要な一巡の長さ
# ---------------------------------------------------------------
def check_cycle(u):
    header("検証5：H6 崩壊と誕生に必要な一巡の長さ tau")

    obs = u["rho_l"] / u["rho_p"]
    tau_linear = 1 / obs
    tau_square = 1 / math.sqrt(obs)

    row("割合に比例：tau / t_P", tau_linear)
    row("割合の2乗に比例：tau / t_P", tau_square)
    row("  そのとき tau", tau_square * u["t_p"], "s")
    row("1/H0（参考：膨張の時間尺度）", 1 / u["h0"], "s")

    # 膨張で速さが決まる場合：rho ∝ H^2。観測範囲 z=0〜2 での変化
    om = 1 - OMEGA_L
    def e2(z):
        return om * (1 + z) ** 3 + OMEGA_L
    ratio = e2(2.0) / e2(0.0)
    print(f"\n  速さが膨張で決まる場合（rho ∝ H^2）")
    print(f"  {'z=2 と z=0 の密度比':<28} {ratio:>12.2f} 倍")
    print("  判定：一定（w=-1）とは整合しない。固有の寿命で決まる必要がある")


def main():
    u = check_units()
    check_doc4(u)
    check_global_xy(u)
    check_counting()
    check_cycle(u)
    print()


if __name__ == "__main__":
    main()

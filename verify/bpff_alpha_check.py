"""
JA0XUY-BPFF 検証：微細構造定数 α（H11・H12）

1. 線＝ε0、リング＝μ0 の対応：積は光速、比（真空インピーダンス）は 2α × h/e^2
2. 1/α の整数部 137 = 125 + 12 と、残り 0.036
3. V1〜V5 の補正項 (4 + 12/20)/128 の照合と、同じ形の式の数え上げ
4. 1/α が 137 になるエネルギーの目安（電子の真空偏極、1ループ）
"""
import itertools
import numpy as np
from scipy.constants import mu_0, epsilon_0, c, h, e, alpha
from scipy.optimize import brentq

INV_ALPHA = 137.035999177      # CODATA 2022
INV_ALPHA_ERR = 0.000000021


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def main():
    section("1. 線＝ε0、リング＝μ0")
    Z0 = (mu_0 / epsilon_0) ** 0.5
    RK = h / e**2
    print(f"  1/sqrt(mu0 eps0)      = {1/(mu_0*epsilon_0)**0.5:.1f} m/s   (c = {c:.0f})")
    print(f"  Z0 = sqrt(mu0/eps0)   = {Z0:.6f} ohm")
    print(f"  h/e^2                 = {RK:.6f} ohm")
    print(f"  Z0 / (h/e^2)          = {Z0/RK:.13f}")
    print(f"  2 alpha               = {2*alpha:.13f}")
    print("  判定：リングと線の強さの比 = 2α。光速は単位の決め方で 1 になる")

    section("2. 整数部 137 = 125 + 12")
    print(f"  125 + 12 = {125+12}")
    print(f"  観測 1/alpha = {INV_ALPHA} ± {INV_ALPHA_ERR}")
    print(f"  残り = {INV_ALPHA-137:.9f}（未解決）")

    section("3. V1〜V5 の補正項 (4 + 12/20)/128")
    v1 = 125 + 12 + (4 + 12 / 20) / 128
    d = v1 - INV_ALPHA
    print(f"  計算値 = {v1}")
    print(f"  ずれ   = {d:+.3e}  （測定誤差の {abs(d)/INV_ALPHA_ERR:.0f} 倍）")
    phi_inv = (5**0.5 - 1) / 2
    vphi = 137 + (4 + phi_inv) / 128
    print(f"  12/20 を 1/φ に替えると {vphi:.9f}、ずれ {vphi-INV_ALPHA:+.3e}")

    S = [1, 2, 3, 4, 5, 6, 8, 12, 20, 32, 125, 128]
    tol = abs(d)
    hits = sorted(
        (abs(137 + (a + b / cc) / dd - INV_ALPHA), a, b, cc, dd)
        for a, b, cc, dd in itertools.product(S, repeat=4)
        if abs(137 + (a + b / cc) / dd - INV_ALPHA) <= tol
    )
    print(f"  形 137+(a+b/c)/d、a〜d を {S} から選ぶ：{len(S)**4} 通り")
    print(f"  V1 と同じかそれ以上に近い式：{len(hits)} 通り")
    for x in hits[:3]:
        print(f"    137+({x[1]}+{x[2]}/{x[3]})/{x[4]}  ずれ {x[0]:.2e}")
    print("  判定：補正項は否定（ずれが大きく、同じ形の式が多数ある）")

    section("4. 1/α が 137 になるエネルギーの目安")

    def bracket(x):  # x = Q^2/m_e^2、空間的運動量での電子1ループ真空偏極
        b = np.sqrt(1 + 4 / x)
        return -5 / 3 + 4 / x + (1 - 2 / x) * b * np.log((b + 1) / (b - 1))

    target = (INV_ALPHA - 137) * 3 * np.pi
    x = brentq(lambda x: bracket(x) - target, 1e-3, 1e4)
    print(f"  Q / m_e ≈ {np.sqrt(x):.2f}、Q ≈ {np.sqrt(x)*0.51099895:.2f} MeV（電子のみ・1ループの概算）")


if __name__ == "__main__":
    main()

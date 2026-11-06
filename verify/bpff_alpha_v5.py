"""
JA0XUY-BPFF 検証：GTM v2.2 の α V5 式（2025-12、本人のメモ）

  1/α = 137 + (7·5)/(108·9) − 1/(108·128·8) = 136395767/995328

1. 個別の測定値との照合
2. 同じ形・同じ語彙で、でたらめな目標値にも当たる確率（偶然確率）
3. 108（コア）の T5 の勘定からの導出
"""
from fractions import Fraction as F
import numpy as np

V5 = F(137) + F(35, 972) - F(1, 110592)

MEAS = {
    "CODATA 2022": (137.035999177, 0.021e-6),
    "CODATA 2018": (137.035999084, 0.021e-6),
    "Rb 2020 (LKB)": (137.035999206, 0.011e-6),
    "Cs 2018 (Berkeley)": (137.035999046, 0.027e-6),
    "電子 g-2 2023 (Harvard)": (137.035999166, 0.015e-6),
}

VOCAB = [1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 20, 27, 32, 36, 108, 125, 128, 137]


def section(t):
    print()
    print("=" * 72)
    print(t)
    print("=" * 72)


def main():
    section("1. 測定値との照合")
    print(f"  V5 = {V5} = {float(V5):.13f}（分母 995328 = 2^12·3^5 : {995328 == 2**12 * 3**5}）")
    for k, (v, s) in MEAS.items():
        d = float(V5) - v
        print(f"  {k:<24} 差 {d:+.2e} = {d/s:+.1f}σ")

    section("2. 偶然確率（形 137+(a·b)/(c·d)−1/(e·f·g)、語彙18語）")
    P2 = sorted({a * b for a in VOCAB for b in VOCAB})
    P3 = sorted({a * b * c for a in VOCAB for b in VOCAB for c in VOCAB})
    xs = np.unique(np.array([p / q for p in P2 for q in P2 if p < q]))
    ys = np.array(sorted({1 / p for p in P3}))

    def count(target, sigma):
        need = target - 137
        c = 0
        for x in xs:
            t = x - need
            i = np.searchsorted(ys, t)
            for j in (i - 1, i):
                if 0 <= j < len(ys) and abs(t - ys[j]) < sigma:
                    c += 1
        return c

    cod, sig = MEAS["CODATA 2022"]
    print(f"  CODATA 2022 に 1σ 以内で当たる組：{count(cod, sig)}")
    rng = np.random.default_rng(0)
    targets = rng.uniform(137.0355, 137.0365, 2000)
    cs = np.array([count(t, sig) for t in targets])
    print(f"  でたらめな目標2000個のうち、1件以上当たる割合：{np.mean(cs > 0):.3f}")
    print("  （式の形を V1〜V5 で改めたこと、語彙の選択は含まない）")

    section("3. 108 の導出（T5 の勘定）")
    spheres = 2 * 3**4          # 段ごとに3倍：2, 6, 18, 54, 162
    lattice = 5**3              # 格子：8, 27, 64, 125
    overflow = spheres - lattice
    navel = 3                   # 臍の緒の出どころ（空間1の OπO）
    pressed = overflow - navel
    half = pressed // 2
    core = lattice - half
    print(f"  球 {spheres} − 格子 {lattice} = あふれ {overflow}")
    print(f"  あふれ {overflow} − 臍の緒 {navel} = 圧力で入る {pressed}")
    print(f"  双極の片側 {pressed}/2 = {half}")
    print(f"  コア = {lattice} − {half} = {core}")
    assert core == 108


if __name__ == "__main__":
    main()

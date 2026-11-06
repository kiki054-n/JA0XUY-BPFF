"""
JA0XUY-BPFF 検証：UMN=1 の境界 N（宇宙の外郭の層）から w0, wa を計算し DESI DR2 と比べる

仮定（作業仮説）
  境界層の破れのエネルギー密度は、境界の大きさ L に対して
      rho_N = 3 C^2 M_P^2 c^2 / L^2       （面で数える：割合 (OπO/L) の2乗）
  C は O(1) の係数（TTT の構造からはまだ決まっていない）。

  境界層の進み方を次の5通りに分けて計算する。
    A 単位胞の外郭（大きさ固定）
    B 外郭が空間と一緒に広がる（L ∝ a）
    C 外郭が誕生から光速で進む（粒子地平線）
    D 外郭＝今から光が届きうる限界（事象の地平線）
    E 外郭＝ハッブル半径 c/H

  宇宙は平坦、物質＋暗黒エネルギー（放射は z<3 では無視）。Omega_m0 = 0.31。

導出（C, D）
  Omega = C^2 / (H L)^2 ,  dlnL/dlna = 1 ± sqrt(Omega)/C  （+ : C 粒子地平線, - : D 事象の地平線）
  w = -1 + (2/3) dlnL/dlna = -1/3 ± 2 sqrt(Omega) / (3C)
  dOmega/dlna = Omega (1 - Omega) (1 ∓ 2 sqrt(Omega)/C)
"""
import numpy as np
from scipy.integrate import solve_ivp

OM0 = 0.31
ODE0 = 1.0 - OM0

# DESI DR2 Results II（arXiv:2503.14738）式(26)-(28) と、DESY5 組み合わせのピボット値
DESI = {
    "DESI+CMB+Pantheon+": (-0.838, 0.055, -0.62, 0.205),
    "DESI+CMB+Union3":    (-0.667, 0.088, -1.09, 0.29),
    "DESI+CMB+DESY5":     (-0.752, 0.057, -0.86, 0.215),
}
PIVOT_Z, PIVOT_W, PIVOT_ERR = 0.31, -0.954, 0.024  # DESI+CMB+DESY5

A_FIT = np.linspace(1 / (1 + 2.33), 1.0, 400)  # DESI の観測範囲 z<2.33


def cpl_fit(a, w):
    """w(a) = w0 + wa (1-a) を最小二乗で当てはめる"""
    X = np.vstack([np.ones_like(a), 1 - a]).T
    (w0, wa), *_ = np.linalg.lstsq(X, w, rcond=None)
    return w0, wa


def horizon_model(C, sign):
    """sign=-1: 事象の地平線（D）, sign=+1: 粒子地平線（C）"""
    def rhs(x, y):
        om = min(max(y[0], 1e-12), 1 - 1e-12)
        return [om * (1 - om) * (1 - sign * 2 * np.sqrt(om) / C)]
    x = np.log(A_FIT)
    sol = solve_ivp(rhs, [0.0, x[0]], [ODE0], t_eval=x[::-1], rtol=1e-10, atol=1e-12)
    om = sol.y[0][::-1]
    w = -1 / 3 + sign * 2 * np.sqrt(om) / (3 * C)
    return w


def w_at_z(w, z):
    return np.interp(1 / (1 + z), A_FIT, w)


def report(name, w):
    w0, wa = cpl_fit(A_FIT, w)
    wp = w_at_z(w, PIVOT_Z)
    accel = w0 < -1 / (3 * ODE0)  # 今の加速条件 q<0 ⇔ w Ω_DE < -1/3
    print(f"  {name:<34} w0={w0:+.3f}  wa={wa:+.3f}  w(z=0.31)={wp:+.3f}  "
          f"ピボットとのずれ {(wp - PIVOT_W) / PIVOT_ERR:+.1f}σ  {'加速する' if accel else '加速しない'}")
    return w0, wa, wp


def main():
    print("=" * 96)
    print("DESI DR2 の値")
    print("=" * 96)
    for k, (w0, s0, wa, sa) in DESI.items():
        print(f"  {k:<22} w0 = {w0:+.3f} ± {s0:.3f}   wa = {wa:+.2f} ± {sa:.2f}")
    print(f"  ピボット（DESY5 組）     w(z={PIVOT_Z}) = {PIVOT_W} ± {PIVOT_ERR}")
    print("  ΛCDM（BPFF の H4）       w0 = -1, wa = 0")

    print()
    print("=" * 96)
    print("境界層 N の進み方ごとの予言")
    print("=" * 96)
    report("A 単位胞の外郭（固定）", -np.ones_like(A_FIT))
    report("B 空間と一緒に広がる（L∝a）", -np.ones_like(A_FIT) / 3)
    report("C 誕生から光速（粒子地平線）C=1", horizon_model(1.0, +1))
    print("  E ハッブル半径 c/H                 rho∝H^2：物質と同じに振る舞い、加速を生まない（w=0 相当）")
    for C in (1.0, 0.8, 0.6):
        report(f"D 事象の地平線 C={C}", horizon_model(C, -1))

    print()
    print("=" * 96)
    print("D の係数 C を動かしたときの wa の符号")
    print("=" * 96)
    for C in np.arange(0.4, 1.61, 0.2):
        w = horizon_model(C, -1)
        w0, wa = cpl_fit(A_FIT, w)
        print(f"  C={C:.1f}  w0={w0:+.3f}  wa={wa:+.3f}")
    print("  判定：D は C によらず wa > 0（過去ほど w が大きい）。DESI は wa < 0 を好む")


if __name__ == "__main__":
    main()

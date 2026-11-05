# JA0XUY-BPFF
双極のFF　「有と無の双極（XY=1）と宇宙定数の記録」

# JA0XUY-BPFF

**Bipolar F-F — 有と無の双極（XY=1）と宇宙定数の記録**

日本の真ん中の地（JA0）から、双極の F（XUY）の理論を記録するリポジトリです。
TTT（Tri-Tetra Theory）の作業仮説のうち、「有と無の双極」と「宇宙定数問題」に関する部分を扱います。

- 統合リポジトリ：[kiki054-n/TTT-core](https://github.com/kiki054-n/TTT-core)
- 著者：川上真潔（Kawakami Naoyuki）
- ORCID：[0009-0009-2972-6511](https://orcid.org/0009-0009-2972-6511)
- ライセンス：MIT

---

## 名前について

| 記号 | 意味 |
|---|---|
| JA0 | 著者のアマチュア無線コールサインの地域符号（信越、日本の真ん中の地） |
| X・Y | 双極の両極。有（X）と無（Y） |
| U | 両極のあいだ。力が働く場所 |
| BPFF | Bipolar F-F。有の側の F と無の側の F が対になった双極 |

---

## 方針

1. **真理を前提にしない**：記録するのは作業仮説です。結果が出るまで、正しいとは扱いません。
2. **ベクトル方程式は参照する**：一般相対論・宇宙論の確立した方程式は、出典を明記して参照します。このリポジトリで書き換えたり、作り直したりはしません。TTT の記述は、それらの方程式の「どの項に、何が対応するか」として書きます。
3. **予言と未解決を明記する**：検証できる予言と、まだ導けていない数を、つねに分けて書きます。

---

## 参照する方程式

詳細と出典は [`references/equations.md`](references/equations.md) に置きます。

**アインシュタイン方程式（宇宙項つき）** [1, 2]

$$G_{\mu\nu} + \Lambda g_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}$$

**フリードマン方程式（平坦な宇宙）** [3]

$$H^2 = \frac{8\pi G}{3}\rho$$

**流体の密度変化（状態方程式 w が一定のとき）**

$$\rho \propto a^{-3(1+w)}$$

**暗黒エネルギーの状態方程式の時間変化（CPL 形式）** [5, 6]

$$w(a) = w_0 + w_a(1-a)$$

---

## BPFF の作業仮説（2026-11-05 時点）

| # | 仮説 | 参照方程式との対応 |
|---|---|---|
| 1 | 重力の源は「量」である。慣性も量で決まる（等価原理と整合） | $T_{\mu\nu}$ に入るのは量 |
| 2 | 空間（比重1）の内側では力は0。有と無の間にだけ力が働く | 真空の質3は $T_{\mu\nu}$ の局所的な源にならない |
| 3 | 有と無の張力は、空間のつながりを通じて一様に伝わる | 一様な負の圧力 $p=-\rho c^2$ |
| 4 | 有と無は双極で $XY=1$（$\log X + \log Y = 0$）。単位胞ごとに成り立つ | 密度一定、$w=-1$ |
| 5 | 単位胞ごとの $XY=1$ とベクトル総和0により、真空の正味の張力は厳密に0 | 120桁問題を、調整ではなく対称性で解消する |
| 6 | 崩壊と誕生の途中にある単位胞だけが、つり合いをわずかに崩す | 観測される小さな $\Lambda$ |
| 7 | 時間の単位は、0から光速に達するまでの時間 | $t_{\text{単位}} = O\pi O / c = l_P / c = t_P$ |

---

## 予言

- **w はちょうど −1 で、時間変化しない**（$w_0=-1,\ w_a=0$）。
- 暗黒エネルギーが時間とともに弱まる傾向（$w_0>-1,\ w_a<0$）が観測で確定すれば、仮説4は否定されます。観測の現状は [7, 8] を参照してください。

---

## 未解決

- 観測値 $\rho_\Lambda/\rho_{\text{Planck}} \approx 10^{-123}$ を出すには、真空の単位胞が誕生から崩壊まで一巡する長さとして、次のどちらかが必要です。TTT の構造から、この数をまだ導けていません。
  - 途中にある割合に比例する場合：約 $10^{123}$ 単位時間
  - 途中にある割合の2乗に比例する場合：約 $10^{61}$ 単位時間
- 完成した真空の単位胞が崩壊と誕生を起こすのはどんなときか、それがまれなのはなぜか。
- T1〜T5（発生期）の速い崩壊と誕生と、現在の真空のまれな崩壊と誕生との関係。

---

## 構成

```
JA0XUY-BPFF/
├── README.md
├── LICENSE
├── references/
│   └── equations.md      参照する方程式と出典
├── hypotheses/
│   └── bpff.md           作業仮説の本文と改訂履歴
├── logs/
│   └── 2026-11-05.md     検討記録（日付ごと）
└── verify/
    └── *.py              数値検証スクリプト
```

---

## 参考文献

1. A. Einstein, *Sitzungsber. Preuss. Akad. Wiss.* (1915) 844.
2. A. Einstein, *Sitzungsber. Preuss. Akad. Wiss.* (1917) 142.
3. A. Friedmann, *Z. Phys.* **10** (1922) 377.
4. S. Weinberg, "The cosmological constant problem," *Rev. Mod. Phys.* **61** (1989) 1.
5. M. Chevallier, D. Polarski, *Int. J. Mod. Phys. D* **10** (2001) 213.
6. E. V. Linder, *Phys. Rev. Lett.* **90** (2003) 091301.
7. DESI Collaboration, "DESI DR2 Results II: Measurements of Baryon Acoustic Oscillations and Cosmological Constraints," arXiv:2503.14738 (2025).
8. S. G. Turyshev, "Dark energy after DESI DR2: Observational status, reconstructions, and physical models," *Phys. Rev. D* **113** (2026) 103540.
9. Planck Collaboration, "Planck 2018 results. VI. Cosmological parameters," *A&A* **641** (2020) A6.

---

## ライセンス

[MIT License](LICENSE) — Copyright (c) 2026 Kawakami Naoyuki

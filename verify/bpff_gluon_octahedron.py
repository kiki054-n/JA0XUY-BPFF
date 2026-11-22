#!/usr/bin/env python3
"""
JA0XUY-BPFF 数値検証：H15 グルーオンと正8面体

正8面体の面の中心へ引いた F（向き (±1,±1,±1) の 8 本）について
  1. 総和が 0 になること
  2. 立方体の対角線 (1,1,1) の方向から見たとき、
     2 本が中心に重なり、6 本が等距離の正六角形に並ぶこと
を確かめる。後者はグルーオン八重項の配置（正六角形 6 ＋ 中心 2）と同じ。

    python3 verify/bpff_gluon_octahedron.py
"""
import itertools
import math

vecs = list(itertools.product([1, -1], repeat=3))
total = [sum(v[i] for v in vecs) for i in range(3)]
print("F の本数:", len(vecs), " 総和:", total)

n = [1 / math.sqrt(3)] * 3
e1 = [1 / math.sqrt(2), -1 / math.sqrt(2), 0.0]
e2 = [1 / math.sqrt(6), 1 / math.sqrt(6), -2 / math.sqrt(6)]
center, ring = [], []
for v in vecs:
    x = sum(a * b for a, b in zip(v, e1))
    y = sum(a * b for a, b in zip(v, e2))
    r = math.hypot(x, y)
    (center if r < 1e-9 else ring).append((v, x, y, r))
print("中心に重なる:", [c[0] for c in center])
angles = sorted(round(math.degrees(math.atan2(y, x)) % 360, 1) for _, x, y, _ in ring)
radii = sorted({round(r, 6) for *_, r in ring})
print("正六角形の点の数:", len(ring), " 半径:", radii, " 角度:", angles)
ok = total == [0, 0, 0] and len(center) == 2 and len(ring) == 6 and len(radii) == 1 \
    and all(abs((angles[i + 1] - angles[i]) - 60) < 0.2 for i in range(5))
print("判定:", "一致（正六角形 6 ＋ 中心 2）" if ok else "不一致")

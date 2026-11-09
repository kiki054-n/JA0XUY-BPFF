"""「前の二つを足す」の導出（toward-a-first-principle/03-derivation.md）の検算。

確かめること：
  1. 条件1・2のみ（全要素が毎段2に分かれる）：2, 4, 8, … 比は2で φ にならない。
  2. 全要素が残り毎段2つ生む（1→3）：2, 6, 18, 54, 162 … 比は3。
  3. 条件3（閉じた M は残って開いた N を1つ生む、N は一段後に閉じる）：
     M' = M + N, N' = M から T(n+1) = T(n) + T(n-1) が毎段成り立つ。
  4. 開いた2本から始めると 2, 2, 4, 6, 10, 16, 26, … 比は φ に収束する。
  5. 出発点によらず（M, N の初期値を変えても）比は φ に収束する。
"""
import math

phi = (1 + math.sqrt(5)) / 2
ok = True


def check(name, cond):
    global ok
    ok &= bool(cond)
    print(f"{'PASS' if cond else 'FAIL'}  {name}")


a = [2]
for _ in range(10):
    a.append(a[-1] * 2)
check(f"条件1・2のみ {a[:6]} … 比は 2（φ ではない）", all(y / x == 2 for x, y in zip(a, a[1:])))

b = [2]
for _ in range(10):
    b.append(b[-1] * 3)
check(f"1→3 の列 {b[:5]} … 比は 3", all(y / x == 3 for x, y in zip(b, b[1:])))


def run(M, N, steps=40):
    t = []
    for _ in range(steps):
        t.append(M + N)
        M, N = M + N, M
    return t


t = run(0, 2)
print("条件3の列（線の数）:", t[:10], "…")
print("   比:", [round(t[i + 1] / t[i], 4) for i in range(1, 9)])
check("毎段 T(n+1) = T(n) + T(n-1)", all(t[i + 1] == t[i] + t[i - 1] for i in range(1, len(t) - 1)))
check("比が φ に収束", abs(t[-1] / t[-2] - phi) < 1e-12)

starts = [(0, 2), (2, 0), (1, 1), (5, 3), (125, 37)]
check(f"出発点 {starts} のどれでも比は φ",
      all(abs(r[-1] / r[-2] - phi) < 1e-10 for r in (run(m, n) for m, n in starts)))

print("\n総合:", "ALL PASS" if ok else "FAIL あり")

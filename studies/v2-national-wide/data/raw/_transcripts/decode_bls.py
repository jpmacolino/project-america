"""Rebuild bls/BLS_pr.data.1.AllData__PRS85006092_093_annual.txt from values copied out of the browser.
Lines are rebuilt in BLS's fixed layout (series_id padded to 17, value right-aligned to 12, CRLF) and the
file's SHA-256 must equal the hash the browser computed on the verbatim extract."""
import hashlib, sys
g = "2.5 3.2 6.7 2.5 1.9 2.5 2.0 4.3 -0.6 2.6 2.3 3.5 1.2 3.3 4.5 3.4 2.6 3.2 3.6 1.9 3.5 0.2 1.4 3.9 3.5 3.1 -1.7 2.7 3.5 1.7 1.4 -0.2 0.0 1.5 -0.8 4.1 2.2 1.7 3.0 0.5 1.6 0.9 1.7 1.6 4.5 0.1 0.7 1.1 2.1 1.9 3.3 3.9 3.0 2.6 4.3 3.7 3.0 2.2 1.0 1.7 1.4 4.0 3.3 -0.1 0.8 0.8 0.9 1.3 0.8 1.3 1.4 2.2 5.2 2.4 -1.6 2.0 3.2 2.3".split()
ix = ("22.481 23.050 23.783 25.377 26.023 26.519 27.170 27.701 28.887 28.719 29.455 30.133 31.199 31.563 32.596 34.074 "
      "35.231 36.156 37.311 38.652 39.372 40.747 40.816 41.398 43.019 44.514 45.879 45.116 46.328 47.940 48.770 49.466 "
      "49.360 49.338 50.058 49.647 51.684 52.838 53.754 55.352 55.654 56.569 57.069 58.026 58.975 61.605 61.677 62.103 "
      "62.772 64.092 65.329 67.516 70.162 72.256 74.115 77.292 80.143 82.528 84.332 85.163 86.642 87.891 91.425 94.428 "
      "94.303 95.075 95.790 96.685 97.930 98.685 100.000 101.372 103.631 109.071 111.717 109.964 112.188 115.787 118.434").split()
assert len(g) == 78 and len(ix) == 79
out = ["series_id        \tyear\tperiod\t       value\tfootnote_codes\r\n"]
for sid, start, vals in (("PRS85006092", 1948, g), ("PRS85006093", 1947, ix)):
    for i, v in enumerate(vals):
        y = start + i
        out.append(f"{sid:<17}\t{y}\tQ05\t{v:>12}\t{'R' if y >= 2021 else ''}\r\n")
b = "".join(out).encode()
want = "52bff8544f4c419891422ba37bb4a765912e1149dee3e6cb98e80329cfc59bf5"
got = hashlib.sha256(b).hexdigest()
print(len(b), got, "MATCH" if got == want else "MISMATCH")
if got == want:
    open(sys.argv[1], "wb").write(b)

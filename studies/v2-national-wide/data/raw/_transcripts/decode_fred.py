"""Rebuild FRED CSVs from the compact transcript and verify each against the browser's SHA-256.
Transcript format: '### ID URL sha256=H bytes=N endsWithNewline=B' then one line 'header YYYY,val YYYY,val ...'
(annual: date = YYYY-01-01; quarterly/monthly tokens carry the full date)."""
import sys, hashlib, pathlib, re
src, outdir = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); outdir.mkdir(parents=True, exist_ok=True)
lines = src.read_text().splitlines(); ok = True
for i in range(0, len(lines), 2):
    m = re.match(r'### (\S+) (\S+) sha256=(\w+) bytes=(\d+)', lines[i]); sid, url, h, n = m.groups()
    head, *toks = lines[i+1].split(' ')
    rows = [t if re.match(r'\d{4}-\d{2}-\d{2},', t) else t[:4] + '-01-01' + t[4:] for t in toks]
    text = head + '\n' + '\n'.join(rows) + '\n'
    got = hashlib.sha256(text.encode()).hexdigest()
    good = got == h and len(text) == int(n); ok &= good
    (outdir / f'FRED_{sid}.csv').write_text(text, newline='\n')
    print(f'{sid:18s} rows={len(rows):4d} bytes={len(text)} sha_match={good}')
sys.exit(0 if ok else 1)

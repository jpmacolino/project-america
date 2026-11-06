"""Rebuild OWID entity extracts from the compact transcript and verify against the browser's SHA-256.
Block: '### slug URL full_sha256=.. full_bytes=.. crlf=.. entity=NAME sha256=H bytes=N' / '# citation ...' / 'header tok tok ...'
Each token is 'CODE,Year,value' with the entity name prefix stripped."""
import sys, hashlib, pathlib, re, json
src, outdir = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); outdir.mkdir(parents=True, exist_ok=True)
lines = src.read_text().splitlines(); ok = True; meta = {}
for i in range(0, len(lines), 3):
    m = re.match(r'### (\S+) (\S+) full_sha256=(\w+) full_bytes=(\d+) crlf=\w+ entity=(.+?) sha256=(\w+) bytes=(\d+)', lines[i])
    slug, url, fsha, fbytes, ent, h, n = m.groups()
    body = lines[i+2]; code = 'OWID_WRL' if ent == 'World' else 'USA'
    k = body.index(' ' + code + ',')
    head, toks = body[:k], body[k+1:].split(' ')
    text = head + '\n' + '\n'.join(ent + ',' + t for t in toks) + '\n'
    good = hashlib.sha256(text.encode()).hexdigest() == h and len(text) == int(n); ok &= good
    fn = outdir / f'OWID_{slug}__{code}.csv'; fn.write_text(text, newline='\n')
    meta[fn.name] = dict(url=url, full_file_sha256=fsha, full_file_bytes=int(fbytes), entity=ent, extract_sha256=h,
                         citation=lines[i+1][len('# citation: '):])
    print(f'{slug:40s} rows={len(toks):4d} sha_match={good}')
p = outdir / 'owid_provenance.json'
old = json.loads(p.read_text()) if p.exists() else {}
old.update(meta); p.write_text(json.dumps(old, indent=1))
sys.exit(0 if ok else 1)

"""Write each extract in a JSON transcript (name -> {sha, ext}) to OUTDIR/name, only if the UTF-8 bytes'
SHA-256 equals the hash the browser computed. usage: decode_json_extracts.py TRANSCRIPT.json OUTDIR"""
import hashlib, json, os, sys
d = json.load(open(sys.argv[1], encoding="utf-8")); bad = 0
for name, v in d.items():
    b = v["ext"].encode("utf-8"); got = hashlib.sha256(b).hexdigest(); ok = got == v["sha"]
    print(("MATCH   " if ok else "MISMATCH"), len(b), name)
    if ok: open(os.path.join(sys.argv[2], name), "wb").write(b)
    else: bad += 1
sys.exit(1 if bad else 0)

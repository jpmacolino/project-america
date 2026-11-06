"""Rebuild an extract from lines copied out of the browser (LF in the transcript), restoring the source's
line ending, and write it only if its SHA-256 equals the hash the browser computed on the verbatim extract.
usage: decode_lines.py TRANSCRIPT OUT SHA256 [crlf|lf]"""
import hashlib, sys
src, out, want = sys.argv[1:4]
eol = "\r\n" if (sys.argv[4] if len(sys.argv) > 4 else "lf") == "crlf" else "\n"
lines = open(src, encoding="utf-8").read().split("\n")
if lines and lines[-1] == "": lines = lines[:-1]
b = "".join(l + eol for l in lines).encode("utf-8")
got = hashlib.sha256(b).hexdigest()
print(len(b), got, "MATCH" if got == want else "MISMATCH")
if got == want: open(out, "wb").write(b)
else: sys.exit(1)

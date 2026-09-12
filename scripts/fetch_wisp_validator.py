"""Fetch pinned upstream validation sources; this is a maintainer action, not skill loading."""
from pathlib import Path
import hashlib
import json
import urllib.request

root = Path(__file__).resolve().parents[1]
lock = json.loads((root / "validation/upstream-lock.json").read_text(encoding="utf-8"))
for path, expected in lock["files"].items():
    target = root / ".wisp-upstream" / path
    if target.is_file() and hashlib.sha256(target.read_bytes()).hexdigest() == expected:
        continue
    url = f'https://raw.githubusercontent.com/{lock["repository"]}/{lock["commit"]}/{path}'
    with urllib.request.urlopen(url, timeout=60) as response:
        data = response.read()
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError(f"Upstream checksum mismatch: {path}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
print(f'Upstream validators ready at {lock["commit"]}; hashes verified.')

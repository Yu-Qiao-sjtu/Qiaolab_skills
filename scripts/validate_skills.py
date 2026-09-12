"""Check discoverable names and local Markdown links without external dependencies."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
skills = sorted((root / "skills").glob("*/SKILL.md"))
assert skills, "No skills found"
for path in skills:
    text = path.read_text(encoding="utf-8-sig")
    assert text.startswith("---\n"), f"Missing frontmatter: {path}"
    frontmatter = text.split("---", 2)[1]
    name = re.search(r"^name: (.+)$", frontmatter, re.M)
    assert name and name.group(1).strip() == path.parent.name, f"Name mismatch: {path}"
    assert re.fullmatch(r"[a-z0-9-]+", name.group(1).strip()), f"Invalid name: {path}"
    assert re.search(r"^description: .+", frontmatter, re.M), f"Missing description: {path}"
    for target in re.findall(r"\]\(([^)]+)\)", text):
        if "://" in target or target.startswith("#"):
            continue
        local = target.split("#", 1)[0]
        assert (path.parent / local).exists(), f"Missing reference: {path}: {local}"
print(f"Validated {len(skills)} skills and their entrypoint links.")

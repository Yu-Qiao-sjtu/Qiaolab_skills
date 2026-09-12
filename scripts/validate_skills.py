"""Offline package checks for our Wisp skills; upstream Rust checks are separate."""
from pathlib import Path
import re
import sys
from urllib.parse import unquote

RESERVED = {"CON", "PRN", "AUX", "NUL"} | {f"{p}{n}" for p in ("COM", "LPT") for n in range(1, 10)}

def portable(path):
    return (len(path.encode("utf-8")) <= 1024 and len(path.split("/")) <= 64 and
            all(part and part not in (".", "..") and not part.endswith((" ", ".")) and
                part.split(".")[0].upper() not in RESERVED and
                not any(ord(c) < 32 or c in '\\:<>"|?*' for c in part) for part in path.split("/")))

def prose(text):
    marker = None
    lines = []
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            char = stripped[0]
            marker = None if marker == char else char if marker is None else marker
        elif marker is None:
            lines.append(line)
    return "\n".join(lines)

def check_skill_package(skill):
    skill = Path(skill)
    problems = []
    entry = skill / "SKILL.md"
    if not entry.is_file():
        return ["Missing SKILL.md"]
    text = entry.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not match:
        problems.append("Missing closed YAML frontmatter")
    else:
        name = re.search(r"^name: (.+)$", match[1], re.M)
        if not name or name[1].strip() != skill.name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name[1].strip()):
            problems.append("Folder/name mismatch or nonportable name")
    files = list(skill.rglob("*"))
    size = 0
    for path in files:
        relative = path.relative_to(skill).as_posix()
        if path.is_symlink() or not portable(relative):
            problems.append(f"Unsafe package path: {relative}")
            continue
        if not path.is_file():
            continue
        data = path.read_bytes()
        size += len(data)
        if len(data) > 8 * 1024 * 1024:
            problems.append(f"Resource exceeds store limit: {relative}")
        if data.startswith(b"version https://git-lfs.github.com/spec/v1"):
            problems.append(f"Unresolved LFS resource: {relative}")
        if path.suffix.lower() != ".md":
            continue
        links = re.findall(r"\]\(([^\s)]+)(?:\s+[^)]*)?\)|`((?:references|scripts|assets)/[^`]+)`", prose(data.decode("utf-8")))
        for markdown, inline in links:
            target = markdown or inline
            if "://" in target or target.startswith(("#", "mailto:")):
                continue
            target = unquote(target.split("#", 1)[0]).removeprefix("./")
            if not target:
                continue
            if not portable(target) or not (path.parent / target).exists():
                problems.append(f"Missing or unsafe reference: {relative}: {target}")
    if len(files) > 4000 or size > 128 * 1024 * 1024:
        problems.append("Package exceeds archive extraction limits")
    return problems

def main():
    root = Path(__file__).resolve().parents[1]
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    problems = []
    for entry in skills:
        problems.extend(f"{entry.parent.name}: {item}" for item in check_skill_package(entry.parent))
    if not skills:
        problems.append("No skills found")
    if problems:
        print("\n".join(problems))
        return 1
    print(f"Validated {len(skills)} complete packages and all Markdown resource links.")
    return 0

if __name__ == "__main__":
    sys.exit(main())

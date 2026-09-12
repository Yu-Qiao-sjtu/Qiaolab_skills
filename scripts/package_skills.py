"""Build complete .skill archives with the pinned upstream packager and verify bytes."""
from pathlib import Path
import subprocess
import sys
import zipfile
from validate_skills import check_skill_package

root = Path(__file__).resolve().parents[1]
packager = root / ".wisp-upstream/skills/skill-creator/scripts/package_skill.py"
for entry in sorted((root / "skills").glob("*/SKILL.md")):
    skill = entry.parent
    errors = check_skill_package(skill)
    if errors:
        raise ValueError("; ".join(errors))
    subprocess.run([sys.executable, "-X", "utf8", str(packager), str(skill), str(root / "dist")], check=True, capture_output=True)
    with zipfile.ZipFile(root / "dist" / f"{skill.name}.skill") as archive:
        assert archive.testzip() is None
        for source in skill.rglob("*"):
            if source.is_file():
                path = f"{skill.name}/{source.relative_to(skill).as_posix()}"
                assert archive.read(path) == source.read_bytes(), path
    print(f"Verified complete archive: dist/{skill.name}.skill")

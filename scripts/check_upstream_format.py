"""Run the pinned upstream skill-creator validator on each package."""
from pathlib import Path
import subprocess
import sys
root = Path(__file__).resolve().parents[1]
validator = root / ".wisp-upstream/skills/skill-creator/scripts/quick_validate.py"
for entry in sorted((root / "skills").glob("*/SKILL.md")):
    subprocess.run([sys.executable, "-X", "utf8", str(validator), str(entry.parent)], check=True)

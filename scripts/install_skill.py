"""Install one complete local package into a Wisp project; never overwrite a package."""
from pathlib import Path
import argparse
import shutil
import tempfile
from validate_skills import check_skill_package

def install(source, project):
    source = Path(source).resolve()
    project = Path(project).resolve(strict=True)
    errors = check_skill_package(source)
    if errors:
        raise ValueError("; ".join(errors))
    discovery = project / ".wisp" / "skills"
    destination = discovery / source.name
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f"Keep existing package: {destination}. Back up and review it before replacing.")
    # Refuse paths redirected outside the user's selected project.
    if not discovery.resolve().is_relative_to(project):
        raise ValueError("Skill discovery directory escapes the selected project")
    staging_root = project / ".wisp" / "skill-staging"
    if not staging_root.resolve().is_relative_to(project):
        raise ValueError("Staging directory escapes the selected project")
    staging_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="install-", dir=staging_root) as temp:
        staged = Path(temp) / source.name
        shutil.copytree(source, staged)
        errors = check_skill_package(staged)
        if errors:
            raise ValueError("; ".join(errors))
        discovery.mkdir(parents=True, exist_ok=True)
        if destination.exists() or destination.is_symlink():
            raise FileExistsError(f"Keep existing package: {destination}")
        staged.rename(destination)
    return destination

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--skill", required=True)
    args = parser.parse_args()
    source_root = Path(__file__).resolve().parents[1] / "skills"
    source = source_root / args.skill
    if source.parent != source_root or not source.is_dir():
        parser.error("Choose one skill folder name in this repository")
    print(f"Installed complete package: {install(source, args.project)}")
    print("Refresh/reopen the Wisp project, then find and load the skill. No model task was executed.")

if __name__ == "__main__":
    main()

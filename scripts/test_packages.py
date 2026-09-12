"""Real fixture tests: isolated complete install, no overwrite, missing resources."""
from pathlib import Path
import tempfile
import unittest
from install_skill import install
from validate_skills import check_skill_package

class Packages(unittest.TestCase):
    def test_all_packages_install_completely_and_refuse_overwrite(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            for entry in (root / "skills").glob("*/SKILL.md"):
                with self.subTest(skill=entry.parent.name):
                    installed = install(entry.parent, project)
                    for source in entry.parent.rglob("*"):
                        if source.is_file():
                            self.assertEqual(source.read_bytes(), (installed / source.relative_to(entry.parent)).read_bytes())
                    before = (installed / "SKILL.md").read_bytes()
                    with self.assertRaises(FileExistsError):
                        install(entry.parent, project)
                    self.assertEqual(before, (installed / "SKILL.md").read_bytes())

    def test_rejects_missing_or_escaping_reference_without_partial_install(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package = root / "broken"
            package.mkdir()
            project = root / "project"
            project.mkdir()
            for target in ("references/missing.md", "../outside.md"):
                (package / "SKILL.md").write_text(f"---\nname: broken\ndescription: test\n---\n[resource]({target})\n", encoding="utf-8")
                self.assertTrue(check_skill_package(package))
                with self.assertRaises(ValueError):
                    install(package, project)
                self.assertFalse((project / ".wisp/skills/broken").exists())

if __name__ == "__main__":
    unittest.main()

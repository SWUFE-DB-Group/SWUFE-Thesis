"""Validate release ZIP contents without TeX or network access."""

from pathlib import Path
import subprocess
import tempfile
import unittest
from zipfile import ZipFile

from scripts.package_release import FONT_FILES, ROOT_FILES, package_release


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="swufe-release-test-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        # Real Git tracking keeps untracked files and build outputs out of ZIPs.
        self.inputs = ROOT_FILES | {f"font/{name}" for name in FONT_FILES} | {
            "contents/绪论.tex", "figures/declaration.pdf", "figures/last-page.pdf",
            "img/swufe_logo.jpg", "docs/layout-audit.md",
            ".github/workflows/release.yml", "scripts/package_release.py",
            "tests/test_release.py", "example.pdf",
        }
        for name in self.inputs:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("test " + name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        for name in ("main.pdf", "main.aux", "contents/绪论.aux", "font/untracked.ttf",
                     ".aws/credentials"):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("must not be packaged")
        self.output = self.root / "build" / "release"

    def test_two_archives_have_only_template_inputs(self):
        archives = package_release(self.root, "v1.0.0", self.output)
        self.assertEqual([p.name for p in archives], [
            "SWUFE-Thesis-v1.0.0-with-font.zip",
            "SWUFE-Thesis-v1.0.0-without-font.zip",
        ])
        expected = ROOT_FILES | {"contents/绪论.tex", "figures/declaration.pdf",
                                 "figures/last-page.pdf", "img/swufe_logo.jpg",
                                 "docs/layout-audit.md"}
        for archive in archives:
            with ZipFile(archive) as package:
                self.assertIsNone(package.testzip())
                names = set(package.namelist())
                if archive.name.endswith("-with-font.zip"):
                    self.assertEqual(names, expected | {f"font/{n}" for n in FONT_FILES})
                else:
                    self.assertEqual(names, expected)
                self.assertEqual(package.read("contents/绪论.tex").decode(),
                                 "test contents/绪论.tex")

    def test_missing_required_font_fails_before_creating_archives(self):
        (self.root / "font" / "Times New Roman Bold.ttf").unlink()
        with self.assertRaisesRegex(ValueError, "Times New Roman Bold.ttf"):
            package_release(self.root, "v1.0.0", self.output)
        self.assertFalse(self.output.exists())

    def test_missing_image_directory_fails_before_creating_archives(self):
        subprocess.run(["git", "update-index", "--force-remove", "img/swufe_logo.jpg"],
                       cwd=self.root, check=True)
        with self.assertRaisesRegex(ValueError, "Missing release directory: img"):
            package_release(self.root, "v1.0.0", self.output)
        self.assertFalse(self.output.exists())

    def test_tag_with_slash_stays_inside_output_directory(self):
        archives = package_release(self.root, "release/v1.0.0", self.output)
        for archive in archives:
            self.assertEqual(archive.parent, self.output)
            self.assertIn("release-v1.0.0", archive.name)


if __name__ == "__main__":
    unittest.main()
